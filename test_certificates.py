import unittest

import mongomock
from mock import Mock

from certificates import Certificates


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.client = mongomock.MongoClient()
        self.fs = Mock(name='mockGridFS')
        self.test_doc_id = self.client.admin.certificates.insert({'aa': 'bb', 'issued': True, 'pubkey': 'K1'})
        self.client.admin.recipients.insert({'pubkey': 'K1'})

    def test_find_user_by_uid(self):
        cert = Certificates(client=self.client, fs=self.fs)
        res = cert.find_user_by_uid(self.test_doc_id)

        self.assertEqual(res['_id'], self.test_doc_id)
        self.assertEqual(res['aa'], 'bb')
        self.assertEqual(res['issued'], True)

    def test_find_user_by_uid_none(self):
        cert = Certificates(client=self.client, fs=self.fs)
        res = cert.find_user_by_uid(None)

        self.assertIsNone(res)

    def test_find_user_by_uid_no_match(self):
        cert = Certificates(client=self.client, fs=self.fs)
        res = cert.find_user_by_uid('SomeIdThatDoesntExist')

        self.assertIsNone(res)

    def test_find_user_by_pubkey_none(self):
        cert = Certificates(client=self.client, fs=self.fs)
        res1, res2 = cert.find_user_by_pubkey(None)

        self.assertIsNone(res1)
        self.assertIsNone(res2)

    def test_find_user_by_pubkey_none(self):
        cert = Certificates(client=self.client, fs=self.fs)
        res1, res2 = cert.find_user_by_pubkey('K1')
        self.assertIsNotNone(res1)
        self.assertIsNotNone(res2)
        self.assertEqual(res1['pubkey'], 'K1')
        self.assertEqual(res2[0]['pubkey'], 'K1')

if __name__ == '__main__':
    unittest.main()
