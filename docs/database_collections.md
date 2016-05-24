Database Collections
====================
This webapp uses MongoDB. There are two collections, one for recipients and one for certificates. GridFs is used to store the certificates themselves.

Recipient
---------
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

Certificate
-----------
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
