import json
import logging
import sys

if sys.version > '3':
    from urllib.parse import urlencode
else:
    from urllib import urlencode


from flask import render_template, request, flash, redirect, url_for, send_from_directory, safe_join
from werkzeug.routing import BaseConverter
from . import app
from . import certificate_service
from . import config
from . import ui_helpers
from .models import UserData
from .forms import RegistrationForm, BitcoinForm


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route('/', methods=['GET', 'POST'])
def home_page():
    """Home page"""
    recent_txids = ['56aa4c9bf3a6a0125aaf24bf',
                    '56aa4c9bf3a6a0125aaf24c7']
    return render_template('index.html', recent_txids=recent_txids)


@app.route('/faq', methods=['GET'])
def faq_page():
    """FAQs"""
    return render_template('faq.html')


@app.route('/keys/<key_name>')
def key_page(key_name=None):
    """Shows keys in the /keys folder"""
    key = config.get_key_by_name(key_name)
    if key:
        return key
    return 'Sorry, this page does not exist.', 404


@app.route('/issuer/<path:issuer_filename>')
def issuer_page(issuer_filename=None):
    """Shows issuer in the /issuer folder, e.g. http://0.0.0.0:5000/issuer/ml-issuer.json"""
    return send_from_directory(safe_join(app.root_path, 'issuer'), issuer_filename, as_attachment=False)

@app.route('/criteria/<regex("[0-9]{4}"):year>/<regex("[0-9]{2}"):month>/<regex("[a-zA-Z0-9.]+"):criteria_name>')
def criteria_page(year, month, criteria_name):
    """Shows criteria, e.g. https://coins.media.mit.edu/criteria/2016/01/alumni.json"""
    criteria_filename = '-'.join([year, month, criteria_name])
    return send_from_directory(safe_join(app.root_path, 'criteria'), criteria_filename, as_attachment=False)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(safe_join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<regex("[a-zA-Z0-9]{12,24}"):identifier>')
def get_award(identifier=None):
    """
    Render user's certificates or individual certificate based on certificate uid
    :param identifier:
    :return:
    """

    format = request.args.get("format", None)
    award, verification_info = certificate_service.get_formatted_certificate(certificate_uid=identifier, format=format)
    if award and format == "json":
        return award
    if award:
        return render_template('award.html', award=award, verification_info=urlencode(verification_info))

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
    """Request a certificate"""
    form = RegistrationForm(request.form)
    bitcoin = BitcoinForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            user_data = UserData(form.pubkey.data, form.email.data, form.degree.data, form.comments.data,
                                 form.first_name.data, form.last_name.data, form.address.data, form.city.data,
                                 form.state.data, form.zipcode.data, form.country.data)

            certificate_service.request_certificate(user_data)

            hidden_email = ui_helpers.obfuscate_email_display(user_data.email)
            flash('We just sent a confirmation email to %s.' % hidden_email)
            return redirect(url_for('home_page'))
        except:
            flash('There seems to be an error with our system. Please try again later.')
    return render_template('request.html', form=form, registered=False, bitcoin=bitcoin)


@app.route("/verify")
def verify():
    uid = request.args.get('uid')
    transaction_id = request.args.get('transactionID')
    verify_response = certificate_service.verify(transaction_id, uid)
    return json.dumps(verify_response)


@app.errorhandler(404)
def page_not_found(error):
    logging.error('Page not found: %s', request.path)
    return 'This page does not exist', 404


@app.errorhandler(500)
def internal_server_error(error):
    logging.error('Server Error: %s', error, exc_info=True)
    return 'Server error: {0}'.format(error), 500


@app.errorhandler(Exception)
def unhandled_exception(e):
    logging.exception('Unhandled Exception: %s', e, exc_info=True)
    return 'Unhandled exception: {0}'.format(e), 500
