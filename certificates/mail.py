import logging

import config
import mandrill

CONFIG_SECTION = 'certificate_service'


class Mail:
    def __init__(self):
        self.api_key = config.get_config().get(CONFIG_SECTION, 'MANDRILL_API_KEY') # TODO make names consistent
        self.email_subject = config.get_config().get(CONFIG_SECTION, 'SUBJECT')
        self.from_email = config.get_config().get(CONFIG_SECTION, 'FROM_EMAIL')
        self.from_name = config.get_config().get(CONFIG_SECTION, 'FROM_NAME')

    def send_receipt_email(self, recipient_email, name):
        mandrill_client = mandrill.Mandrill(self.api_key)
        template_content = None
        message = {
            'subject': self.email_subject,
            'from_email': self.from_email,
            'from_name': self.from_name,
            'to': [{
                'email': recipient_email,
                'name': name['givenName'] + ' ' + name['familyName']
            }],
            'headers': {'Reply-To': self.from_email},
            'headers': {'Reply-To': self.from_email},
            'important': False,
            'track_opens': True,
            'track_clicks': True,
            'auto_text': True,
            'inline_css': True,
            'merge_language': 'handlebars',
            'global_merge_vars': [{'name': 'first_name', 'content': name['givenName']}]
        }
        try:
            logging.trace('sending mandrill receipt template')
            result = mandrill_client.messages.send_template(template_name='receipt-template',
                                                            template_content=template_content, message=message, async=False)
            # TODO (kim): determine if result needs to be inspected
            return result
        except mandrill.Error as e:
            error_message = 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            logging.error(error_message)
            # A mandrill error occurred: <class 'mandrill.InvalidKeyError'> - Invalid API key
            raise
