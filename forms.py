from wtforms import Form, TextField, TextAreaField, validators, RadioField


class RegistrationForm(Form):
    first_name = TextField('First Name', [validators.required(), validators.length(max=200)])
    last_name = TextField('Last Name', [validators.required(), validators.length(max=200)])
    email = TextField('Email', [validators.required(), validators.length(max=200)])
    pubkey = TextField('Bitcoin Public Address', [validators.required(), validators.length(max=35)])
    address = TextField('Mailing Address', [validators.required(), validators.length(max=200)])
    city = TextField('City', [validators.required(), validators.length(max=200)])
    state = TextField('State/Province/Region', [validators.required(), validators.length(max=200)])
    zipcode = TextField('ZIP/Postal Code', [validators.required(), validators.length(max=200)])
    country = TextField('Country', [validators.required(), validators.length(max=200)])
    degree = RadioField('Degree',
                        choices=[('mas-ms', 'MAS MS'), ('mas-phd', 'MAS PhD'), ('other', 'It\'s complicated')],
                        coerce=unicode)
    comments = TextAreaField('Comments', [validators.optional()])


class AddressForm(Form):
    address = TextField('Mailing Address', [validators.required(), validators.length(max=200)])
    city = TextField('City', [validators.required(), validators.length(max=200)])
    state = TextField('State/Province/Region', [validators.required(), validators.length(max=200)])
    zipcode = TextField('ZIP/Postal Code', [validators.required(), validators.length(max=200)])
    country = TextField('Country', [validators.required(), validators.length(max=200)])


class BitcoinForm(Form):
    identity = RadioField('Identity', choices=[
        ('yes', 'Yes, I have a Bitcoin identity'),
        ('no', 'No, I don\'t have a Bitcoin identity')], coerce=unicode)
