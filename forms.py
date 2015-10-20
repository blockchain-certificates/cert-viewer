from wtforms import Form, TextField, validators

class RegistrationForm(Form):
	first = TextField('First Name', [validators.required(), validators.length(max=200)])
	last = TextField('Last Name', [validators.required(), validators.length(max=200)])

class AddressForm(Form):
	address = TextField('Mailing Address', [validators.required(), validators.length(max=200)])
	city = TextField('City', [validators.required(), validators.length(max=200)])
	state = TextField('State/Province/Region', [validators.required(), validators.length(max=200)])
	zipcode = TextField('ZIP/Postal Code', [validators.required(), validators.length(max=200)])
	country = TextField('Country', [validators.required(), validators.length(max=200)])