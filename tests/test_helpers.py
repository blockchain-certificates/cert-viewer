import unittest

from cert_viewer import helpers


class TestHelpers(unittest.TestCase):
    def test_format_email_short(self):
        res = helpers.obfuscate_email_display('kim@kim.com')
        self.assertEqual(res, 'ki*@kim.com')

    def test_format_email_long(self):
        res = helpers.obfuscate_email_display('kimlongeremail@kim.com')
        self.assertEqual(res, 'ki************@kim.com')


if __name__ == '__main__':
    unittest.main()
