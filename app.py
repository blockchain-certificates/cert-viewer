import json
import os
from urllib.parse import urlencode

import config
import gridfs
import secrets
from certificates import helpers
from certificates.service import Service
from certificates.service import UserData
from flask import Flask, render_template, request, flash, redirect, url_for
from forms import RegistrationForm, BitcoinForm
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = secrets.SECRET_KEY
client = MongoClient(host=secrets.MONGO_URI)

gfs = gridfs.GridFS(client['admin'])
service = Service(client, gfs)

# TODO (kim): global exception handling
# TODO (kim): ensure verify display is same after refactor (async)
# TODO (kim): load recent txids
# TODO (kim): fix config location
# TODO (kim): fix all static file location


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
    key = helpers.get_keys(key_name)
    if key:
        return key
    return 'Sorry, this page does not exist.'


@app.route('/issuer/<issuer_name>')
def issuer_page(issuer_name=None):
    """Shows issuer in the /issuer folder"""
    if issuer_name in os.listdir(config.ISSUER_PATH):
        content = helpers.read_file(os.path.join(config.ISSUER_PATH, issuer_name))
        return content
    else:
        return 'Sorry, this page does not exist.'


# Shows issuer in the /issuer folder
@app.route('/criteria/<year>/<month>/<criteria_name>')
def criteria_page(year, month, criteria_name):
    filename = year + '-' + month + '-' + criteria_name
    if filename in os.listdir(config.CRITERIA_PATH):
        content = helpers.read_file(os.path.join(config.CRITERIA_PATH, filename))
        return content
    else:
        return 'Sorry, this page does not exist.'


@app.route('/<identifier>')
def get_award(identifier=None):
    """
    Render user's certificates or individual certificate based on search query
    :param identifier:
    :return:
    """

    format = request.args.get("format", None)
    award, verification_info = service.get_formatted_certificate(identifier=identifier, format=format)
    if award and format == "json":
        return award
    if award:
        return render_template('award.html', award=award, verification_info=urlencode(verification_info))

    return "Sorry, this page does not exist."


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

            service.get_or_create_certificate(user_data)

            # TODO (Juliana): what is hidden email? This formatting seems to convert kim@kim.com to ki*@kim.com (see
            # test_helpers.py
            hidden_email = helpers.format_email(user_data.email)
            flash('We just sent a confirmation email to %s.' % hidden_email)
            return redirect(url_for('home_page'))
        except:
            flash('There seems to be an error with our system. Please try again later.')
    return render_template('request.html', form=form, registered=False, bitcoin=bitcoin)


@app.route("/verify")
def verify():
    uid = request.args.get('uid')
    transaction_id = request.args.get('transactionID')
    verify_response = service.get_verify_response(transaction_id, uid)
    return json.dumps(verify_response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
