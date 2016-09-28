import json
import logging
import os
import sys

import requests
from cert_verifier import verifier
from flask import render_template, request, flash, redirect, url_for, send_from_directory, safe_join
from werkzeug.routing import BaseConverter

from . import app
from . import config
from . import helpers
from .forms import RegistrationForm, BitcoinForm
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


@app.route('/', methods=['GET', 'POST'])
def home_page():
    """Home page"""
    recent_certids_from_config = config.get_config().recent_certids

    if recent_certids_from_config:
        recent_certids = str.split(recent_certids_from_config, ',')
    else:
        # keeping for backcompat; either way we should update this from mongo
        recent_certids = [
            '56aa4c9bf3a6a0125aaf24bf',
            '56aa4c9bf3a6a0125aaf24c7']
    return render_template('index.html', recent_certids=recent_certids)


@app.route('/faq', methods=['GET'])
def faq_page():
    """FAQs"""
    return render_template('faq.html')


@app.route('/keys/<key_name>')
def key_page(key_name=None):
    """Redirect to identity endpoint for backcompat"""
    redirect_url = os.path.join(config.get_config().id_endpoint, 'keys', key_name)
    return redirect(redirect_url)


@app.route('/issuer/<path:issuer_filename>')
def issuer_page(issuer_filename=None):
    """Redirect to identity endpoint for backcompat"""
    redirect_url = os.path.join(config.get_config().id_endpoint, 'issuer', issuer_filename)
    return redirect(redirect_url)


@app.route(
    '/criteria/<regex("[0-9]{4}"):year>/<regex("[0-9]{2}"):month>/<regex("[a-zA-Z0-9.]+"):criteria_name>')
def criteria_page(year, month, criteria_name):
    """Redirect to identity endpoint for backcompat"""
    criteria_filename = '-'.join([year, month, criteria_name])
    redirect_url = os.path.join(config.get_config().id_endpoint, 'criteria', criteria_filename)
    return redirect(redirect_url)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(safe_join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#regex("[a-zA-Z0-9]{12,24}"):
@app.route('/<identifier>')
def get_award(identifier=None):
    """
    Render user's certificates or individual certificate based on certificate uid
    :param identifier:
    :return:
    """

    requested_format = request.args.get("format", None)
    from . import cert_store_connection

    cert_raw = cert_store_connection.get_certificate(identifier)
    if not cert_raw:
        logging.error('Could not find certificate with id, %s', identifier)
        return 'Problem getting certificate', 500

    cert_string = cert_raw.decode('utf-8')
    cert_json = json.loads(cert_string)
    award, verification_info = helpers.get_award_and_verification_for_certificate(cert_json, 'txid')
    if award and requested_format == "json":
        return award
    if award:
        return render_template('award.html', award=award,
                               verification_info=urlencode(verification_info))

    return "Sorry, this page does not exist.", 404


@app.route('/bitcoinkeys', methods=['GET'])
def generate_keys():
    """
    Create Bitcoin identity for a user so they can request a certificate
    :return:
    """

    return render_template('bitcoinkeys.html')


@app.route('/request', methods=['GET', 'POST'])
def request_page():
    """Request an introduction. Forwarding to intro endpoint for backcompat"""
    form = RegistrationForm(request.form)
    bitcoin = BitcoinForm(request.form)

    if request.method == 'POST' and form.validate():

        intro_endpoint = config.get_config().intro_endpoint
        if not intro_endpoint:
            return "Sorry, introductions are not supported", 404

        user_data = {
            'bitcoinAddress': form.pubkey.data,
            'comments': form.comments.data,
            'email': form.email.data,
            'firstName': form.first_name.data,
            'lastName': form.last_name.data,
            'degree': form.degree.data,
            'address': form.address.data,
            'city': form.city.data,
            'state': form.state.data,
            'zipCode': form.zipcode.data,
            'country': form.country.data
        }

        headers = {'Content-type': 'application/json',
                   'Accept': 'application/json'}
        r = requests.post(intro_endpoint, json=user_data, headers=headers)
        succeeded = r.status_code == 200
        if not succeeded:
            error_message = str(r.content)
            logging.error('Problem processing introduction, %s', error_message)
            return 'Problem processing introduction', 500

        sent = Notifier.factory().notify(
            form.email.data,
            form.first_name.data,
            form.last_name.data)

        logging.debug('finished requesting certificate')
        hidden_email = helpers.obfuscate_email_display(form.email.data)
        if sent:
            flash('We just sent a confirmation email to %s.' % hidden_email)
        else:
            flash(
                'We received your request and will respond to %s.' % hidden_email)
        return redirect(url_for('home_page'))
    else:
        return render_template('request.html', form=form, registered=False, bitcoin=bitcoin)


@app.route("/verify")
def verify():
    uid = request.args.get('uid')
    #transaction_id = request.args.get('transactionID')
    from . import cert_store_connection
    cert_raw = cert_store_connection.get_certificate(uid)

    if not cert_raw:
        logging.error('Could not find certificate with uid, %s', uid)
        return 'Problem getting certificate', 500
    verify_response = verifier.verify_cert_contents(cert_raw)
    if verify_response:
        return json.dumps(verify_response)
    return 'problem rendering response'  # TODO!!!


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
