import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home_page():
	return render_template('index.html')

@app.route('/hierarchy')
def test():
	return "trial"

@app.route('/<id>')
def award(id=None):
	if id:
		try:
			with open('jsons/'+id+'.json') as json_data:
				recipient = json.load(json_data)
				json_data.close()
		except IOError:
			return 'Invalid URL'
		if recipient:
			award = {
				"logoImg": recipient["certificate"]["issuer"]["image"],
				"signatureImg": recipient["assertion"]["image:signature"],
				"name": recipient["recipient"]["givenName"]+' '+recipient["recipient"]["familyName"],
				"title": recipient["certificate"]["title"],
				"subtitle": recipient["certificate"]["subtitle"]["content"],
				"display": recipient["certificate"]["subtitle"]["display"],
				"organization":recipient["certificate"]["issuer"]["name"],
				"text": recipient["certificate"]["description"],
				"mlPublicKey": 'asdkfiawufelajwnflajsdfuhwaefjafasdfasdkfiawufelajwnflajsdfuhwaefjafasdfasdkfiawufelajwnflajsdfuhwaefjafasdfasdkfiawufelajwnflajsdfuhwaefjafasdf',
				"signature": recipient["signature"]
			}
			if award['display'] == 'FALSE':
				award['subtitle'] = '';
			return render_template('award.html', award=award)
	else:
		return "Error, please try again."

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)