import unittest

import mock
import mongomock
from cert_viewer.certificate_store import CertificateStore
from cert_viewer.models import UserData
from mock import Mock
from pymongo.results import InsertOneResult


# mongo mock doesn't support insert_one, so we patch that with insert
def mock_insert_workaround(collection, document):
    inserted_id = collection.insert(document)
    return InsertOneResult(inserted_id, True)


class TestCertificates(unittest.TestCase):

    def setUp(self):
        self.client = mongomock.MongoClient()
        self.fs = Mock(name='mockGridFS')

        # see mock_insert_workaround comment. We need to use this workaround for the scope of this entire test.
        self.patcher = mock.patch.object(CertificateStore, 'insert_shim', side_effect=mock_insert_workaround)
        self.patcher.start()

        self.certificate_store = CertificateStore(client=self.client, gfs=self.fs)
        self.test_doc_id = self.certificate_store.insert_certificate({'aa': 'bb', 'issued': True, 'pubkey': 'K1'})
        self.certificate_store.insert_user({'pubkey': 'K1'})

    def tearDown(self):
        self.patcher.stop()

    def test_find_user_by_uid(self):
        self.test_doc_id = self.certificate_store.insert_certificate({'aa': 'bb', 'issued': True, 'pubkey': 'K1'})
        self.certificate_store.insert_user({'pubkey': 'K1'})

        res = self.certificate_store.find_certificate_by_certificate_uid(self.test_doc_id)

        self.assertEqual(res['_id'], self.test_doc_id)
        self.assertEqual(res['aa'], 'bb')
        self.assertEqual(res['issued'], True)

    def test_find_user_by_uid_none(self):
        res = self.certificate_store.find_certificate_by_certificate_uid(None)

        self.assertIsNone(res)

    def test_find_user_by_uid_no_match(self):
        res = self.certificate_store.find_certificate_by_certificate_uid('111111111111111111111111')

        self.assertIsNone(res)

    def test_find_user_by_pubkey_none(self):
        res1, res2 = self.certificate_store.find_user_and_certificate_by_pubkey(None)

        self.assertIsNone(res1)
        self.assertIsNone(res2)

    def test_find_user_by_pubkey_none(self):
        res1, res2 = self.certificate_store.find_user_and_certificate_by_pubkey('K1')
        self.assertIsNotNone(res1)
        self.assertIsNotNone(res2)
        self.assertEqual(res1['pubkey'], 'K1')
        self.assertEqual(res2[0]['pubkey'], 'K1')

    def test_create_certificate(self):
        res = self.certificate_store.create_certificate_request('K2')
        self.assertIsNotNone(res)

    def test_create_user(self):
        user_data = UserData('K3', 'r@r.com', 'a.b.s', 'some comments', 'satoshi', 'nakamoto', '111 main st',
                             'seattle', 'wa', '96666', 'usa')
        user_object = self.certificate_store.create_user(user_data)
        self.assertEqual(user_object['info']['name']['givenName'], 'satoshi')


if __name__ == '__main__':
    unittest.main()
