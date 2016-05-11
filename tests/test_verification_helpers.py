import codecs
import unittest

from certificates import verification_helpers as v
from certificates.ui_helpers import hexlify
from certificates.verification_helpers import Verifier
from mock import Mock


def mock_json():
    return {
        "out": [
            {
                "spent": False,
                "tx_index": 145158287,
                "type": 0,
                "addr": "1C1iqyXbk2rXVzGKyvs8HrFH79RMzTQQxA",
                "value": 2750,
                "n": 0,
                "script": "76a91478cc504569ea233a1fc9873aaefbedd03f40a30d88ac"
            },
            {
                "spent": False,
                "tx_index": 145158287,
                "type": 0,
                "addr": "14X6w2V5GGxwFui5EuK6cydWAji461LMre",
                "value": 2750,
                "n": 1,
                "script": "76a9142699cebbb24a29fda62de03b2faa14eac4b5f85c88ac"
            },
            {
                "spent": False,
                "tx_index": 145158287,
                "type": 0,
                "value": 0,
                "n": 2,
                "script": "6a20ddd7a9da081bf39bec8a049968010c0b429e969ea4b1b0f9badf9360d9d8886c"
            }
        ]
    }


def mock_transaction_lookup(transaction_id):
    m = Mock(status_code=200)
    m.json = mock_json
    return m


class TestVerify(unittest.TestCase):
    def test_verify(self):
        verifier = Verifier(mock_transaction_lookup)
        f = codecs.open('66a00099a2b165359bd9ac2c.json', "r", "utf-8")
        data = f.read()
        response = verifier.verify('1111', data)
        print(response)

    def test_get_hash_from_bc_op(self):
        script_input = b'eed3a6da081df36ded8a046668010d0d426e666ea4d1d0f6dadf6360d6d8886d'
        script = hexlify(script_input)
        tx_json = {u'out': [{u'addr': u'ADDR1', u'spent': False, u'value': 0, u'script': script}]}
        hashed_json = v.get_hash_from_bc_op(tx_json=tx_json)
        self.assertEqual(hashed_json, script_input)

    def test_get_hash_from_chain(self):
        script_input = b'eed3a6da081df36ded8a046668010d0d426e666ea4d1d0f6dadf6360d6d8886d'
        script = hexlify(script_input)
        tx_json = {'out': [{'spent': False, 'tx_index': 142155247, 'type': 0, 'value': 0, 'n': 2, 'script': script}]}
        hashed_json = v.fetch_hash_from_chain(tx_json=tx_json)
        self.assertEqual(hashed_json,
                         '65656433613664613038316466333664656438613034363636383031306430643432366536363665613464316430663664616466363336306436643838383664')

    def test_compute_hash(self):
        hash_result = v.compute_hash('abc123'.encode('utf-8'))
        self.assertEqual(hash_result, '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090')

    def test_check_revocation_not_revoked(self):
        not_revoked = v.check_revocation(tx_json={u'out': [{u'addr': u'ADDR1', u'spent': False}]},
                                         revoke_address='ADDR1')
        self.assertEqual(not_revoked, True)

    def test_check_revocation_is_spent(self):
        not_revoked = v.check_revocation(tx_json={u'out': [{u'addr': u'ADDR1', u'spent': True}]},
                                         revoke_address='ADDR1')
        self.assertEqual(not_revoked, False)

    def test_check_revocation_address_mismatch(self):
        not_revoked = v.check_revocation(tx_json={u'out': [{u'addr': u'ADDR1', u'spent': False}]},
                                         revoke_address='ADDR2')
        self.assertEqual(not_revoked, False)

    def test_check_revocation_multiple_txs_not_revoked(self):
        not_revoked = v.check_revocation(tx_json={u'out': [{u'addr': u'ADDR1', u'spent': False},
                                                           {u'addr': u'ADDR2', u'spent': True}]},
                                         revoke_address='ADDR1')
        self.assertEqual(not_revoked, True)

    def test_check_revocation_multiple_txs_revoked(self):
        not_revoked = v.check_revocation(tx_json={u'out': [{u'addr': u'ADDR1', u'spent': False},
                                                           {u'addr': u'ADDR2', u'spent': True}]},
                                         revoke_address='ADDR2')
        self.assertEqual(not_revoked, False)


if __name__ == '__main__':
    unittest.main()
