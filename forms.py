from wtforms import Form, TextField, validators, RadioField

class RegistrationForm(Form):
	first_name = TextField('First Name', [validators.required(), validators.length(max=200)])
	last_name = TextField('Last Name', [validators.required(), validators.length(max=200)])
	email = TextField('Email', [validators.required(), validators.length(max=200)])
	address = TextField('Mailing Address', [validators.required(), validators.length(max=200)])
	city = TextField('City', [validators.required(), validators.length(max=200)])
	state = TextField('State/Province/Region', [validators.required(), validators.length(max=200)])
	zipcode = TextField('ZIP/Postal Code', [validators.required(), validators.length(max=200)])
	country = TextField('Country', [validators.required(), validators.length(max=200)])
	degree = RadioField('Degree', choices=[('mas-ms','MAS MS'),('mas-phd','MAS PhD'), ('other','It\'s complicated')], coerce=unicode)
	comments = TextField('Comments', [validators.optional()])
	# name = TextField('Name', [validators.required(), validators.length(max=200)])

class AddressForm(Form):
	address = TextField('Mailing Address', [validators.required(), validators.length(max=200)])
	city = TextField('City', [validators.required(), validators.length(max=200)])
	state = TextField('State/Province/Region', [validators.required(), validators.length(max=200)])
	zipcode = TextField('ZIP/Postal Code', [validators.required(), validators.length(max=200)])
	country = TextField('Country', [validators.required(), validators.length(max=200)])