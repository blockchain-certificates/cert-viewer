import unittest

from certificates import helpers


class TestHelpers(unittest.TestCase):
    def test_format_email(self):
        """this test fails. Adding it because I can't figure out the point of format_email, so I want to track it"""
        res = helpers.format_email('kim@kim.com')
        self.assertEqual(res, 'kim@kim.com')


if __name__ == '__main__':
    unittest.main()
