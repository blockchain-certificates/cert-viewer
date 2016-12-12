import logging

from flask import flash
from flask import request
from flask import (url_for, redirect)
from flask.views import MethodView

from cert_viewer import helpers
from cert_viewer.forms import BitcoinForm, SimpleRegistrationForm
from cert_viewer.notifier import Notifier
from cert_viewer.views.__init__ import render

TEMPLATE = 'request.html'

class RequestView(MethodView):
    def post(self):
        recipient_form = SimpleRegistrationForm(request.form)
        if recipient_form.validate():
            user_data = recipient_form.to_user_data()
            from cert_viewer import introduction_store_bridge
            introduction_store_bridge.insert_introduction(user_data)
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
            return redirect(url_for('index'))
        else:
            bitcoin_form = BitcoinForm(request.form)
            return render(TEMPLATE, form=recipient_form, registered=False, bitcoin=bitcoin_form)

    def get(self):
        """Request an introduction. Forwarding to intro endpoint for backcompat"""

        recipient_form = SimpleRegistrationForm(request.form)
        bitcoin_form = BitcoinForm(request.form)

        return render(TEMPLATE, form=recipient_form, registered=False, bitcoin=bitcoin_form)
