# Certificate format
Show below is the certificate format for the ML alumni coins. To see a rendered certificate, please go to [coins.media.mit.edu](https://coins.media.mit.edu).

```json

{
  "verify": {
    "signer": "http://coins.media.mit.edu/keys/ml-certs-public-key.asc",
    "attribute-signed": "uid",
    "type": "ECDSA(secp256k1)"
  },
  "recipient": {
    "type": "email",
    "hashed": false,
    "familyName": "Joe",
    "givenName": "Schmoe",
    "pubkey": "<unique recipient bitcoin address>",
    "identity": "johndeere@email.com"
  },
  "assertion": {
    "issuedOn": "2016-01-26",
    "image:signature": "data:image/png;base64,<base64 encoded image of Joi's signature>",
    "evidence": "",
    "uid": "<string of bson objectid()>",
    "id": "http://coins.media.mit.edu/<uid>"
  },
  "certificate": {
    "subtitle": {
      "content": "",
      "display": false
    },
    "description": "This certificate honors you as a member of the Media Lab's alumni community on the occasion of the Lab's 30th anniversary. The Lab places special value on the many ways our alumni have contributed\u2014and continue to contribute\u2014to the intellectual vitality both at the Lab and throughout the world.",
    "language": "en-US",
    "title": "Alum",
    "image": "data:image/png;base64,<base64 encoded image of ML alum logo>",
    "id": "http://coins.media.mit.edu/criteria/2016/01/alumni.json",
    "issuer": {
      "url": "http://media.mit.edu",
      "image": "data:image/png;base64,<base64 encoded image of ML logo>",
      "id": "https://coins.media.mit.edu/issuer/ml-issuer.json",
      "email": "certs@media.mit.edu",
      "name": "MIT Media Lab"
    }
  }
}

```