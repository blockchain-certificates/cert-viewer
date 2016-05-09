import unittest

import mongomock
from certificates import Certificates
from mock import Mock
from service import UserData
import mock
from mock import patch
import certificates

def lame_insert(collection, document):
    inserted_id = collection.insert(document)
    return inserted_id


class TestCertificates(unittest.TestCase):

    def setUp(self):
        self.client = mongomock.MongoClient()
        self.fs = Mock(name='mockGridFS')

        with mock.patch.object(Certificates, 'insert_shim', side_effect=lame_insert):
            self.cert = Certificates(client=self.client, gfs=self.fs)
            self.db = self.client['admin']

            self.test_doc_id = self.cert.insert_shim(self.client['admin']['certificates'], {'aa': 'bb', 'issued': True, 'pubkey': 'K1'})
            self.cert.insert_shim(self.client['admin']['recipients'], {'pubkey': 'K1'})

    #@patch.object('certificates.Certificates', 'insert_shim')
    def test_find_user_by_uid(self):

        with mock.patch.object(Certificates, 'insert_shim', side_effect=lame_insert):
            #mock_method = lame_insert

            self.cert = Certificates(client=self.client, gfs=self.fs)
            self.db = self.client['admin']

            self.test_doc_id = self.cert.insert_shim(self.client['admin']['certificates'],
                                                     {'aa': 'bb', 'issued': True, 'pubkey': 'K1'})
            self.cert.insert_shim(self.client['admin']['recipients'], {'pubkey': 'K1'})

            res = self.cert.find_user_by_uid(self.test_doc_id)

            self.assertEqual(res['_id'], self.test_doc_id)
            self.assertEqual(res['aa'], 'bb')
            self.assertEqual(res['issued'], True)

    def test_find_user_by_uid_none(self):
        res = self.cert.find_user_by_uid(None)

        self.assertIsNone(res)

    def test_find_user_by_uid_no_match(self):
        res = self.cert.find_user_by_uid('111111111111111111111111')

        self.assertIsNone(res)

    def test_find_user_by_pubkey_none(self):
        res1, res2 = self.cert.find_user_by_pubkey(None)

        self.assertIsNone(res1)
        self.assertIsNone(res2)

    def test_find_user_by_pubkey_none(self):
        res1, res2 = self.cert.find_user_by_pubkey('K1')
        self.assertIsNotNone(res1)
        self.assertIsNotNone(res2)
        self.assertEqual(res1['pubkey'], 'K1')
        self.assertEqual(res2[0]['pubkey'], 'K1')

    def test_create_certificate(self):
        res = self.cert.create_cert('K2')
        self.assertIsNotNone(res)

    def test_create_user(self):
        user_data = UserData('K3', 'r@r.com', 'a.b.s', 'some comments', 'satoshi', 'nakamoto', '111 main st',
                             'seattle', 'wa', '96666', 'usa')
        user_object = self.cert.create_user(user_data)
        self.assertEqual(user_object['info']['name']['givenName'], 'satoshi')


if __name__ == '__main__':
    unittest.main()
