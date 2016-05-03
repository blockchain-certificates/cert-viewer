import unittest
import helpers
import mock

# TODO: mock out mongo client
class TestHelpers(unittest.TestCase):

    def test_find_user_by_txid_or_uid_both_none(self):
        self.assertFalse(True)
        #self.assertIsNone(helpers.find_user_by_txid_or_uid(None, None))

    def test_find_user_by_txid_or_uid_both_missing(self):
        self.assertFalse(True)
        #self.assertIsNone(helpers.find_user_by_txid_or_uid('missing_txid', 'missing_id'))




if __name__ == '__main__':
    unittest.main()
