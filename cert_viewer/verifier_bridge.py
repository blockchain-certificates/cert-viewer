from cert_verifier import verifier as verify_tool

class CertificateVerifierBridge(object):
    def __init__(self, cert_store):
        self.cert_store = cert_store

    def verify(self, certificate_uid):
        certificate_model = self.cert_store.get_certificate(certificate_uid)
        return verify_tool.verify_certificate(certificate_model)


def verify(uid):
    from . import verifier
    verify_response = verifier.verify(uid)
    return verify_response
