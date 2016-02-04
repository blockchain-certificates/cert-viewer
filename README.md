About
===
Check out the web application at [https://coins.media.mit.edu](https://coins.media.mit.edu).


Example Certificate
===
Check out documentation of the certificate itself [here](https://github.com/ml-learning/coins.media.mit.edu/blob/development/CERTIFICATE.md).


Installation
===

* Git clone the repository
* Set up a virtual environment and install the dependencies from requirements.txt
* Create a `secrets.py` file with the following structure

```python
MONGO_URI = "mongodb://<username>:<password>@<domain>:<mongo_port>"
SECRET_KEY = "<random string>"

# Setup your mandrill account at https://www.mandrill.com/
MANDRILL_API_KEY = "<mandrill_api_key>"
```

* Run the flask server `python app.py`
* Open http://localhost:5000


Database Configuration
===
This webapp uses MongoDB. There are two collections, one for recipients and one for certificates. GridFs is used to store the certificates themselves.

Example of a recipient object:
```
{
  "_id": ObjectId(),
  "pubkey": "<recipient public key>",
  "info": {
    "email": "",
    "name": {
      "givenName": "",
      "familyName": ""
    },
    "degree": "<mas-ms/mas-phd/other>",
    "address": {
      "streetAddress": "",
      "city": "",
      "state": "",
      "zipcode": "",
      "country": ""
    }
  }
}
```

Example of a certificate object:
```
{
  "_id": "<uid string of certificate file>",
  "issued": <true/false>,
  "pubkey": "<recipient public key>",
  "txid": "<certificate transaction id>"
}
```

A recipient object can have multiple certificate objects. The objects are linked together by the "pubkey" field.


Contact
===
Contact [coins@media.mit.edu](mailto:coins@media.mit.edu) with questions
