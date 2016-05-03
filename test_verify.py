import unittest

import verify as v


class TestVerify(unittest.TestCase):

    # TODO: get a script
    def test_get_hash_from_bc_op(self):
        tx_json = {u'out': [{u'addr': u'ADDR1', u'spent': False, u'value': 0, u'script': b''}]}
        hashed_json = v.get_hash_from_bc_op(tx_json=tx_json)
        #self.assertEqual(hashed_json, '')
        self.assertEqual(True, False)

    # TODO: get a script
    def test_get_hash_from_chain(self):
        tx_json = {u'out': [{u'addr': u'ADDR1', u'spent': False, u'value': 0, u'script': b''}]}
        #hashed_json = v.fetchHashFromChain(tx_json=tx_json)
        #self.assertEqual(hashed_json, '')
        self.assertEqual(True, False)

    def test_computeHash(self):
        hash_result = v.computeHash('abc123'.encode('utf-8'))
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
