from cert_viewer import helpers


def certificate_to_award(displayable_certificate):
    tx_url = helpers.get_tx_lookup_chain(displayable_certificate.chain, displayable_certificate.txid)

    award = {
        'logoImg': displayable_certificate.issuer.image,
        'name': displayable_certificate.recipient_name,
        'title': displayable_certificate.title,
        'organization': displayable_certificate.issuer.name,
        'text': displayable_certificate.description,
        'issuerID': displayable_certificate.issuer.id,
        'transactionID': displayable_certificate.txid,
        'transactionIDURL': tx_url,
        'issuedOn': displayable_certificate.issued_on.strftime('%Y-%m-%d')
    }
    if displayable_certificate.signature_image:
        # TODO: format images and titles for all signers
        award['signatureImg'] = displayable_certificate.signature_image[0].image

    if displayable_certificate.subtitle:
        award['subtitle'] = displayable_certificate.subtitle

    return award


def get_formatted_award_and_verification_info(cert_store, certificate_uid):
    """
    Propagates KeyError if not found
    :param certificate_uid:
    :return:
    """
    certificate_model = cert_store.get_certificate(certificate_uid)
    award = certificate_to_award(certificate_model)
    verification_info = {
        'uid': str(certificate_uid)
    }
    return award, verification_info
