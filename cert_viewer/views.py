import json
import logging
import sys

from flask import render_template, request, flash, redirect, url_for, send_from_directory, safe_join, jsonify
from werkzeug.routing import BaseConverter

from . import app, config
from . import certificate_formatter
from . import helpers
from .forms import SimpleRegistrationForm, BitcoinForm
from .notifier import Notifier

if sys.version > '3':
    from urllib.parse import urlencode
else:
    from urllib import urlencode


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(safe_join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET', 'POST'])
def home_page():
    recent_certs_from_config = config.get_config().recent_certids
    if recent_certs_from_config:
        recent_certs = str.split(recent_certs_from_config, ',')
    else:
        recent_certs = []
    return render_template('index.html', recent_certids=recent_certs)


@app.route('/faq', methods=['GET'])
def faq_page():
    return render_template('faq.html')


@app.route('/issuer/<path:issuer_filename>')
def issuer_page(issuer_filename=None):
    """
    Returns identifying information for a Blockchain Certificate issuer.
    ---
    tags:
      - issuer
    parameters:
      - name: username
        in: path
        type: string
        required: true
    responses:
      200:
        description: The issuer identification at the specified path
        schema:
          id: issuer_response
          properties:
            issuerKeys:
              type: string
              description: The username
              default: some_username
            revocationKeys:
              type: string
              description: The username
              default: some_username
            id:
              type: string
              description: The username
              default: some_username
            name:
              type: string
              description: The username
              default: some_username
            email:
              type: string
              description: The username
              default: some_username
            url:
              type: string
              description: The username
              default: some_username
            introductionURL:
              type: string
              description: The username
              default: some_username
            image:
              type: string
              description: The username
              default: some_username
    """
    issuer_path = safe_join(app.root_path, 'issuer')
    return send_from_directory(issuer_path, filename=issuer_filename, as_attachment=False)


@app.route('/certificate/<uid>')
def get_certificate(certificate_uid=None):
    """
    Returns a certificate based on a certificate UID
    ---
    tags:
      - certificate
    parameters:

      - name: username
        in: path
        type: string
        required: true
        pattern: ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$
    responses:
      200:
        description: The issuer identification at the specified path

    :param certificate_uid:
    :return:
    """
    try:
        from . import cert_store
        certificate_json = cert_store.get_certificate_json(certificate_uid)
        if not certificate_json:
            logging.error('Could not find certificate with id: %s', certificate_uid)
            return 'Could not find certificate', 500
        return jsonify(certificate_json)
    except KeyError:
        logging.warning('Could not find certificate with id: %s', certificate_uid)
        return 'Could not find certificate', 404
    except Exception as e:
        logging.error(e)
        return 'Internal error', 500


# regex("[a-zA-Z0-9]{12,24}"):
@app.route('/<identifier>')
def get_award(identifier=None):
    """
    Render user's certificates or individual certificate based on certificate uid
    :param identifier:
    :return:
    """
    requested_format = request.args.get('format', None)
    if requested_format == 'json':
        return get_certificate(identifier)
    else:
        try:
            from . import cert_store
            award, verification_info = certificate_formatter.get_formatted_award_and_verification_info(cert_store,
                                                                                                       identifier)
            return render_template('award.html', award=award,
                                   verification_info=urlencode(verification_info))
        except KeyError:
            logging.warning('Could not find certificate with id: %s', identifier)
            return 'Could not find certificate', 404
        except Exception as e:
            logging.error(e)
            return 'Internal error', 500


@app.route('/bitcoinkeys', methods=['GET'])
def generate_keys():
    """
    Create Bitcoin identity for a user so they can request a certificate
    :return:
    """

    return render_template('bitcoinkeys.html')


@app.route('/intro', methods=['POST'])
def intro(introduction):
    """
    Returns identifying information for a Blockchain Certificate issuer.
    ---
    tags:
      - introduction
    parameters:
      - in: body
        name: introduction
        required: true
        description: Introduce yourself to a Blockchain Certificate issuer
        schema:
          id: User
          required:
            - bitcoinAddress
            - email
            - firstName
            - lastName
          properties:
            firstName:
              type: string
            lastName:
              type: string
            bitcoinAddress:
              type: string
              description: bitcoin public address
              pattern: ^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$
            email:
              type: string
              format: email
    responses:
      200:
        description: Introduction was successful
      400:
        description: Invalid introduction json payload


    :return:
    """
    from cert_viewer import intro_store
    intro_store.insert(introduction)


@app.route('/request', methods=['GET', 'POST'])
def request_page():
    """Request an introduction. Forwarding to intro endpoint for backcompat"""
    recipient_form = SimpleRegistrationForm(request.form)
    bitcoin_form = BitcoinForm(request.form)

    if request.method == 'POST' and recipient_form.validate():
        user_data = recipient_form.to_user_data()
        intro(user_data)
        succeeded = True
        if not succeeded:
            # error_message = str(r.content)
            # logging.error('Problem processing introduction, %s', error_message)
            return 'Problem processing introduction', 500

        sent = Notifier.factory().notify(
            recipient_form.email.data,
            recipient_form.first_name.data,
            recipient_form.last_name.data)

        logging.debug('finished requesting certificate')
        hidden_email = helpers.obfuscate_email_display(recipient_form.email.data)
        if sent:
            flash('We just sent a confirmation email to %s.' % hidden_email)
        else:
            flash('We received your request and will respond to %s.' % hidden_email)
        return redirect(url_for('home_page'))
    else:
        return render_template('request.html', form=recipient_form, registered=False, bitcoin=bitcoin_form)


@app.route("/verify")
def verify():
    try:
        uid = request.args.get('uid')
        # transaction_id = request.args.get('transactionID')
        from . import verifier
        verify_response = verifier.verify(uid)
        return json.dumps(verify_response)
    except Exception as e:
        logging.error(e)
        return 'Problem verifying certificate', 500


@app.errorhandler(404)
def page_not_found(error):
    logging.error('Page not found: %s, error: ', request.path, error)
    return 'This page does not exist', 404


@app.errorhandler(500)
def internal_server_error(error):
    logging.error('Server Error: %s', error, exc_info=True)
    return 'Server error: {0}'.format(error), 500


@app.errorhandler(Exception)
def unhandled_exception(e):
    logging.exception('Unhandled Exception: %s', e, exc_info=True)
    return 'Unhandled exception: {0}'.format(e), 500
