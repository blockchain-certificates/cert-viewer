import unittest

import verify as v
from helpers import hexlify


class TestVerify(unittest.TestCase):
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
