import logging

import mandrill
from . import config


class Notifier(object):
    def factory():
        notifier = config.get_config().NOTIFIER_TYPE
        if notifier == 'mail':
            return Mail()
        if notifier == 'noop':
            return NoOp()
        assert 0, "Unrecognized notifier type: " + notifier

    factory = staticmethod(factory)


class NoOp(Notifier):
    def notify(self, recipient_email, first_name, last_name):
        logging.warning(
            'A notification would have been sent to first_name=%s,last_name=%s,email=%s, but no notifier is configured',
            first_name, last_name, recipient_email)
        return False


class Mail(Notifier):
    def __init__(self):
        self.mandrill_api_key = config.get_config().MANDRILL_API_KEY
        self.subject = config.get_config().SUBJECT
        self.from_email = config.get_config().FROM_EMAIL
        self.from_name = config.get_config().FROM_NAME

    def notify(self, recipient_email, first_name, last_name):
        mandrill_client = mandrill.Mandrill(self.mandrill_api_key)
        template_content = None
        message = {
            'subject': self.subject,
            'from_email': self.from_email,
            'from_name': self.from_name,
            'to': [{
                'email': recipient_email,
                'name': first_name + ' ' + last_name
            }],
            'headers': {'Reply-To': self.from_email},
            'important': False,
            'track_opens': True,
            'track_clicks': True,
            'auto_text': True,
            'inline_css': True,
            'merge_language': 'handlebars',
            'global_merge_vars': [{'name': 'first_name', 'content': first_name}]
        }
        try:
            logging.debug('sending mandrill receipt template')
            result = mandrill_client.messages.send_template(template_name='receipt-template',
                                                            template_content=template_content, message=message,
                                                            async=False)
            return result
        except mandrill.Error as e:
            error_message = 'A mandrill error occurred: %s - %s' % (
                e.__class__, e)
            logging.exception(error_message, e)
            # A mandrill error occurred: <class 'mandrill.InvalidKeyError'> -
            # Invalid API key
            raise
