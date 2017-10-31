import logging
import os

from os import listdir
from os.path import isfile, join
from flask import jsonify, redirect
from flask_themes2 import render_theme_template, static_file_url
from werkzeug.routing import BaseConverter

from cert_viewer import certificate_store_bridge
from cert_viewer import introduction_store_bridge
from cert_viewer import verifier_bridge

DEFAULT_THEME = 'default'

def update_app_config(app, config):
    app.config.update(
        SECRET_KEY=config.secret_key,
        ISSUER_NAME=config.issuer_name,
        SITE_DESCRIPTION=config.site_description,
        ISSUER_LOGO_PATH=config.issuer_logo_path,
        ISSUER_EMAIL=config.issuer_email,
        THEME=config.theme,
    )
    recent_certs = update_recent_certs()
    app.config['RECENT_CERT_IDS'] = recent_certs[-10:]

def update_recent_certs():
    cert_path = "cert_data"
    certs_folder = []
    for file in listdir(cert_path):
        if file[len(file) - 4:] == "json":
            certs_folder.append(file[:len(file) - 5])
    
    return certs_folder

def render(template, **context):
    from cert_viewer import app
    return render_theme_template(app.config['THEME'], template, **context)


def configure_views(app, config):
    update_app_config(app, config)
    add_rules(app, config)


from flask.views import View


class GenericView(View):
    def __init__(self, template):
        self.template = template

        super(GenericView, self).__init__()

    def dispatch_request(self):
        return render(self.template)


def add_rules(app, config):
    from cert_viewer.views.award_view import AwardView
    from cert_viewer.views.json_award_view import JsonAwardView
    from cert_viewer.views.renderable_view import RenderableView
    from cert_viewer.views.issuer_view import IssuerView
    from cert_viewer.views.verify_view import VerifyView
    from cert_viewer.views.request_view import RequestView

    update_app_config(app, config)
    app.url_map.converters['regex'] = RegexConverter

    app.add_url_rule('/', view_func=GenericView.as_view('index', template='index.html'))

    app.add_url_rule(rule='/<certificate_uid>', endpoint='award',
                     view_func=AwardView.as_view(name='award', template='award.html',
                     view=certificate_store_bridge.award))

    app.add_url_rule('/certificate/<certificate_uid>',
                     view_func=JsonAwardView.as_view('certificate', view=certificate_store_bridge.get_award_json))

    app.add_url_rule('/verify/<certificate_uid>',
                     view_func=VerifyView.as_view('verify', view=verifier_bridge.verify))

    app.add_url_rule('/intro/', view_func=introduction_store_bridge.insert_introduction, methods=['POST', ])
    app.add_url_rule('/request', view_func=RequestView.as_view(name='request'))
    app.add_url_rule('/faq', view_func=GenericView.as_view('faq', template='faq.html'))
    app.add_url_rule('/bitcoinkeys', view_func=GenericView.as_view('bitcoinkeys', template='bitcoinkeys.html'))
    app.add_url_rule('/issuer/<issuer_file>', view_func=issuer_page)
    app.add_url_rule('/spec', view_func=spec)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(KeyError, key_error)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(Exception, unhandled_exception)


from flasgger import Swagger

def spec():
    from cert_viewer import app

    return jsonify(Swagger(app))


def issuer_page(issuer_file):
    from cert_viewer import app
    the_url = static_file_url(theme=app.config['THEME'], filename = (os.path.join('issuer/', issuer_file)))
    return redirect(the_url, code=302)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


# Errors
def page_not_found(error):
    logging.error('Page not found: %s', error, exc_info=True)
    return 'This page does not exist', 404


def key_error(error):
    key = error.args[0]
    logging.error('Key not found not found: %s, error: ', key)

    message = 'Key not found: ' + key
    return message, 404

def internal_server_error(error):
    logging.error('Server Error: %s', error, exc_info=True)
    return 'Server error: {0}'.format(error), 500


def unhandled_exception(e):
    logging.exception('Unhandled Exception: %s', e, exc_info=True)
    return 'Unhandled exception: {0}'.format(e), 500
