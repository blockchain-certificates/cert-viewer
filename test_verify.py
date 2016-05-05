import sys
import unittest
import binascii
import json

import verify as v

# todo: can refactor?
unhexlify = binascii.unhexlify
hexlify = binascii.hexlify
if sys.version > '3':
    unhexlify = lambda h: binascii.unhexlify(h.encode('utf8'))
    hexlify = lambda b: binascii.hexlify(b).decode('utf8')


class TestVerify(unittest.TestCase):

    def test_get_hash_from_bc_op(self):
        script = hexlify(b'ddd7a9da081bf39bec8a049968010c0b429e969ea4b1b0f9badf9360d9d8886c')
        tx_json = {u'out': [{u'addr': u'ADDR1', u'spent': False, u'value': 0, u'script': script}]}
        hashed_json = v.get_hash_from_bc_op(tx_json=tx_json)
        self.assertEqual(hashed_json, b'ddd7a9da081bf39bec8a049968010c0b429e969ea4b1b0f9badf9360d9d8886c')

    def test_get_hash_from_chain(self):
        script = hexlify(b'6a20ddd7a9da081bf39bec8a049968010c0b429e969ea4b1b0f9badf9360d9d8886c')
        tx_json = {'out': [{ 'spent': False, 'tx_index': 145158287, 'type': 0, 'value': 0, 'n': 2, 'script': script}]}
        hashed_json = v.fetchHashFromChain(tx_json=tx_json)
        self.assertEqual(hashed_json, '3661323064646437613964613038316266333962656338613034393936383031306330623432396539363965613462316230663962616466393336306439643838383663')

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
