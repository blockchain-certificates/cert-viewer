import unittest

import mock
import mongomock
from mock import Mock
from pymongo.results import InsertOneResult

from cert_viewer.certificate_store import CertificateStore

# mongo mock doesn't support insert_one, so we patch that with insert
def mock_insert_workaround(collection, document):
    inserted_id = collection.insert(document)
    return InsertOneResult(inserted_id, True)


class TestCertificateStore(unittest.TestCase):
    def setUp(self):
        self.client = mongomock.MongoClient()
        self.fs = Mock(name='mockGridFS')

        # see mock_insert_workaround comment. We need to use this workaround for the scope of this entire test.
        self.patcher = mock.patch.object(CertificateStore, 'insert_shim', side_effect=mock_insert_workaround)
        self.patcher.start()

        self.certificate_store = CertificateStore(client=self.client, gfs=self.fs)
        self.test_doc_id = self.certificate_store.insert_certificate({'aa': 'bb', 'issued': True, 'pubkey': 'K1'})

    def tearDown(self):
        self.patcher.stop()

    def test_find_certificate_by_uid_no_match(self):
        res = self.certificate_store.find_certificate_by_uid('111111111111111111111111')

        self.assertIsNone(res)


if __name__ == '__main__':
    unittest.main()
