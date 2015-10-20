import mandrill
import secrets
from itsdangerous import URLSafeSerializer

def generate_confirm_token(email):
	serializer = URLSafeSerializer(secrets.SECRET_KEY)
	return serializer.dumps(email)

def check_token(token):
	serializer = URLSafeSerializer(secrets.SECRET_KEY)
	try:
		email = serializer.loads(token)
	except:
		return False
	return email

def send_confirm_email(email, name):
	mandrill_client = mandrill.Mandrill(secrets.MANDRILL_API_KEY)
	template_content = None
	confirm_token = generate_confirm_token(email)
	confirm_link = "http://coins.media.mit.edu/confirm/"+ confirm_token
	message = {
			"subject": "Claim your ML Coin",
			"from_email": "coins@media.mit.edu",
			"from_name": "ML Coins",
			"to": [{
				"email": email,
				"name": name
			}],
			"headers": {"Reply-To": "coins@media.mit.edu"},
			"important": False,
			"track_opens": True,
			"track_clicks": True,
			"auto_text": True,
			"merge_language": "handlebars",
			"global_merge_vars" : [{'name': 'confirm_link','content': confirm_link},
								   {'name': 'secret_msg','content': 'This is the secret message!'}]
		}
	try:
		result = mandrill_client.messages.send_template(template_name='test-template', template_content=template_content, message=message, async=False)
		print result

	except mandrill.Error, e:
	    # Mandrill errors are thrown as exceptions
	    print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
	    # A mandrill error occurred: <class 'mandrill.InvalidKeyError'> - Invalid API key    
	    raise