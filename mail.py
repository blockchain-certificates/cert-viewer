import secrets

import mandrill


def send_reciept_email(email, name):
    mandrill_client = mandrill.Mandrill(secrets.MANDRILL_API_KEY)
    template_content = None
    message = {
        "subject": "Your request for a Media Lab coin is being processed",
        "from_email": "coins@media.mit.edu",
        "from_name": "Media Lab Coins",
        "to": [{
            "email": email,
            "name": name['givenName'] + " " + name['familyName']
        }],
        "headers": {"Reply-To": "coins@media.mit.edu"},
        "important": False,
        "track_opens": True,
        "track_clicks": True,
        "auto_text": True,
        "inline_css": True,
        "merge_language": "handlebars",
        "global_merge_vars": [{'name': 'first_name', 'content': name['givenName']}]
    }
    try:
        result = mandrill_client.messages.send_template(template_name='receipt-template',
                                                        template_content=template_content, message=message, async=False)
        return result
    except mandrill.Error, e:
        # Mandrill errors are thrown as exceptions
        print
        'A mandrill error occurred: %s - %s' % (e.__class__, e)
        # A mandrill error occurred: <class 'mandrill.InvalidKeyError'> - Invalid API key
        raise
