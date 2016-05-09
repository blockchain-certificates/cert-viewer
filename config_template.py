MANDRILL_API_KEY = '<Mandrill API key>'
MONGO_URI = '<Mongo connection string, e.g. mongodb://host:port>'
SECRET_KEY = '<Flask secret key, to enable cryptographically signed sessions>'

CERTIFICATES_DB = 'Mongo db to store certificates and recipients'

KEYS_PATH = 'keys/'
ISSUER_PATH = 'issuer/'
CRITERIA_PATH = 'criteria/'

MLISSUER_PATH = ISSUER_PATH + 'ml-issuer.json'

ML_PUBKEY = 'ml-certs-public-key.asc'
ML_REVOKEKEY = 'ml-certs-revoke-key.asc'

FROM_EMAIL = 'coins@media.mit.edu'
FROM_NAME = 'Media Lab Coins'
SUBJECT = 'Your request for a Media Lab coin is being processed'
