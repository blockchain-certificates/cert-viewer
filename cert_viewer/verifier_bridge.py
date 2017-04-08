from cert_verifier import verifier


def verify(certificate_uid):
    from . import cert_store
    certificate = cert_store.get_certificate(certificate_uid)
    if certificate:
        verify_response = verifier.verify_certificate(certificate)
        return verify_response
    else:
        raise Exception('Cannot find certificate with uid=%s', certificate_uid)


