import sys

from wtforms import Form, TextAreaField, validators, RadioField, StringField


def get_coerce_val():
    if sys.version_info.major < 3:
        coerce_val = unicode
    else:
        coerce_val = str
    return coerce_val


class BitcoinForm(Form):
    identity = RadioField('Identity', choices=[
        ('yes', 'Yes, I have a Bitcoin identity'),
        ('no', 'No, I don\'t have a Bitcoin identity')], coerce=get_coerce_val())


class SimpleRegistrationForm(Form):
    first_name = StringField(
        'First Name', [
            validators.required(), validators.length(
                max=200)])
    last_name = StringField(
        'Last Name', [
            validators.required(), validators.length(
                max=200)])
    email = StringField(
        'Email', [
            validators.required(), validators.length(
                max=200)])
    pubkey = StringField(
        'Bitcoin Public Address', [
            validators.required(), validators.length(
                max=35)])

    def to_user_data(self):
        user_data = {
            'bitcoinAddress': self.pubkey.data,
            'email': self.email.data,
            'firstName': self.first_name.data,
            'lastName': self.last_name.data
        }
        return user_data


class ExtendedRegistrationForm(Form):
    """Example of a registration form with additional fields. Corresponds to request_extended.html."""
    first_name = StringField(
        'First Name', [
            validators.required(), validators.length(
                max=200)])
    last_name = StringField(
        'Last Name', [
            validators.required(), validators.length(
                max=200)])
    email = StringField(
        'Email', [
            validators.required(), validators.length(
                max=200)])
    pubkey = StringField(
        'Bitcoin Public Address', [
            validators.required(), validators.length(
                max=35)])

    address = StringField(
        'Mailing Address', [
            validators.required(), validators.length(
                max=200)])
    city = StringField(
        'City', [
            validators.required(), validators.length(
                max=200)])
    state = StringField('State/Province/Region',
                        [validators.required(), validators.length(max=200)])
    zipcode = StringField('ZIP/Postal Code',
                          [validators.required(),
                           validators.length(max=200)])
    country = StringField(
        'Country', [
            validators.required(), validators.length(
                max=200)])
    degree = RadioField('Degree',
                        choices=[('option1', 'Option 1'), ('option2',
                                                           'Option 2'), ('other', 'It\'s complicated')],
                        coerce=get_coerce_val())
    comments = TextAreaField('Comments', [validators.optional()])

    def to_user_data(self):
        user_data = {
            'bitcoinAddress': self.pubkey.data,
            'email': self.email.data,
            'firstName': self.first_name.data,
            'lastName': self.last_name.data,
            'comments': self.comments.data,
            'degree': self.degree.data,
            'address': self.address.data,
            'city': self.city.data,
            'state': self.state.data,
            'zipCode': self.zipcode.data,
            'country': self.country.data
        }
        return user_data

    def to_user_data_legacy(self):
        user_json = {'pubkey': self.pubkey.data, 'info': {}}
        user_json['info']['email'] = self.email.data
        user_json['info']['degree'] = self.degree.data
        user_json['info']['comments'] = self.comments.data
        user_json['info']['name'] = {'familyName': self.last_name.data, 'givenName': self.first_name.data}
        user_json['info']['address'] = {
            'streetAddress': self.address.data,
            'city': self.city.data,
            'state': self.state.data,
            'zipcode': "\'" + self.zipcode.data,  # TODO: per discussion, ' was added to help export. Find another way
            'country': self.country.data
        }
        return user_json
