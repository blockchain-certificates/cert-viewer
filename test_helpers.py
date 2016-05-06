import unittest


# TODO: mock out mongo client; otherwise can't use helpers.py
class TestHelpers(unittest.TestCase):

    def test_find_user_by_txid_or_uid_both_none(self):
        self.assertFalse(True)

    def test_find_user_by_txid_or_uid_both_missing(self):
        self.assertFalse(True)

if __name__ == '__main__':
    unittest.main()
