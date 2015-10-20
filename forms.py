from wtforms import Form, TextField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])

class AddressForm(Form):
	address = TextAreaField('Mailing Address', [validators.required(), validators.length(max=200)])
	city = TextAreaField('City', [validators.required(), validators.length(max=200)])
	state = TextAreaField('State/Province/Region', [validators.required(), validators.length(max=200)])
	zipcode = TextAreaField('ZIP/Postal Code', [validators.required(), validators.length(max=200)])
	country = TextAreaField('Country', [validators.required(), validators.length(max=200)])