from flask import request


def award(certificate_uid):
    requested_format = request.args.get('format', None)
    if requested_format == 'json':
        return get_award_json(certificate_uid)
    from . import cert_store, certificate_formatter
    award, verification_info = certificate_formatter.get_formatted_award_and_verification_info(cert_store,
                                                                                               certificate_uid)
    return {'award': award,
            'verification_info': verification_info}


def get_award_json(certificate_uid):
    from . import cert_store
    certificate_json = cert_store.get_certificate_json(certificate_uid)
    return certificate_json
