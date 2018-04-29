from cert_verifier import verifier


def verify(certificate_uid):
    from . import cert_store
    certificate = cert_store.get_certificate(certificate_uid)
    if certificate:
        # A walk around to set default etherscan api token as '' to avoid
        # TypeError in composing ethesan URL. The options can be removed
        # when https://github.com/blockchain-certificates/cert-verifier/pull/21
        # is deployed. 
        options={'etherscan_api_token':''}
        verify_response = verifier.verify_certificate(certificate, options=options)
        return verify_response
    else:
        raise Exception('Cannot find certificate with uid=%s', certificate_uid)
