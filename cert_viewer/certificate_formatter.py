import os

from cert_schema import is_mainnet_address, Chain, UnknownChainError
from cert_schema.model import TransactionSignature
from cert_viewer import helpers

def get_chain(certificate_model):
    """
    Converts the anchor type in the Blockcert signature to a Chain. In next version of Blockcerts schema we will be able
    to write XTNOpReturn for testnet
    :param chain:
    :return:
    """

    anchor = next(sig for sig in certificate_model.signatures if isinstance(sig, TransactionSignature))
    if anchor and anchor.merkle_proof:
        # choose first anchor type because there is only 1
        anchor_type = anchor.merkle_proof.proof_json['anchors'][0]['type']
    else:
        # pre-v1.2 backcompat
        anchor_type = "BTCOpReturn"

    address = certificate_model.recipient_public_key

    if anchor_type == 'REGOpReturn':
        return Chain.regtest
    elif anchor_type == 'MockOpReturn':
        return Chain.mocknet
    elif anchor_type == "BTCOpReturn":
        is_mainnet = is_mainnet_address(address)
        if is_mainnet:
            return Chain.mainnet
        else:
            return Chain.testnet
    else:
        raise UnknownChainError('Chain not recognized from anchor type: ' + anchor_type)


def certificate_to_award(displayable_certificate):
    chain = get_chain(displayable_certificate)
    tx_url = helpers.get_tx_lookup_chain(chain, displayable_certificate.txid)

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
