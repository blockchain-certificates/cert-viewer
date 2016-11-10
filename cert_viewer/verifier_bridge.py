import json

from cert_verifier import verifier
from cert_store.model import BlockcertVersion


class CertificateVerifierBridge(object):
    def __init__(self, cert_store):
        self.cert_store = cert_store

    def verify(self, certificate_uid):
        return self.verify_json(certificate_uid)

    def verify_json(self, certificate_uid):
        cert_json = self.cert_store.get_certificate_json(certificate_uid)
        return verifier.verify_json(cert_json)


class V1AwareCertificateVerifierBridge(CertificateVerifierBridge):
    def __init__(self, cert_store):
        self.cert_store = cert_store

    def verify(self, certificate_uid):
        certificate = self.cert_store.get_certificate_model(certificate_uid)
        if certificate.version == BlockcertVersion.V1_1:
            return verifier.verify_v1_1(certificate.certificate_bytes, certificate.transaction_id)
        elif certificate.version == BlockcertVersion.V1_2:
            return self.verify_json(certificate.certificate_json)
        else:
            raise Exception('Unknown Blockchain Certificate version')

