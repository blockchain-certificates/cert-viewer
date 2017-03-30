import os

from cert_core import parse_chain_from_address

from cert_viewer import helpers


def format_verification_info(displayable_certificate):
    return {
        'uid': displayable_certificate.uid,
        'transactionID': displayable_certificate.get_transaction_id()
    }


def certificate_to_award(displayable_certificate):
    chain = parse_chain_from_address(displayable_certificate.recipient_public_key)
    tx_url = helpers.get_tx_lookup_prefix_for_chain(chain)

    award = {
        'logoImg': displayable_certificate.logo_image,
        'name': displayable_certificate.recipient_name,
        'title': displayable_certificate.title,
        'organization': displayable_certificate.organization,
        'text': displayable_certificate.description,
        'issuerID': displayable_certificate.issuer_id,
        'transactionID': displayable_certificate.get_transaction_id(),
        'transactionIDURL': os.path.join(tx_url, displayable_certificate.get_transaction_id()),
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
    verification_info = format_verification_info(certificate_model)
    return award, verification_info
