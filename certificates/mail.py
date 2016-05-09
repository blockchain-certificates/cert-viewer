import config
import mandrill
import secrets


def send_receipt_email(recipient_email, name):
    mandrill_client = mandrill.Mandrill(secrets.MANDRILL_API_KEY)
    template_content = None
    message = {
        'subject': config.SUBJECT,
        'from_email': config.FROM_EMAIL,
        'from_name': config.FROM_NAME,
        'to': [{
            'email': recipient_email,
            'name': name['givenName'] + ' ' + name['familyName']
        }],
        'headers': {'Reply-To': config.FROM_EMAIL},
        'important': False,
        'track_opens': True,
        'track_clicks': True,
        'auto_text': True,
        'inline_css': True,
        'merge_language': 'handlebars',
        'global_merge_vars': [{'name': 'first_name', 'content': name['givenName']}]
    }
    try:
        result = mandrill_client.messages.send_template(template_name='receipt-template',
                                                        template_content=template_content, message=message, async=False)
        return result
    except mandrill.Error as e:
        # Mandrill errors are thrown as exceptions
        print
        'A mandrill error occurred: %s - %s' % (e.__class__, e)
        # A mandrill error occurred: <class 'mandrill.InvalidKeyError'> - Invalid API key
        raise
