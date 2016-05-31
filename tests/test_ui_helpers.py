import unittest

from cert_viewer import ui_helpers


class TestUIHelpers(unittest.TestCase):
    def test_format_email_short(self):
        res = ui_helpers.obfuscate_email_display('kim@kim.com')
        self.assertEqual(res, 'ki*@kim.com')

    def test_format_email_long(self):
        res = ui_helpers.obfuscate_email_display('kimlongeremail@kim.com')
        self.assertEqual(res, 'ki************@kim.com')


if __name__ == '__main__':
    unittest.main()
