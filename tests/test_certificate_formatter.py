import unittest
import json

from cert_viewer import certificate_formatter
from cert_core import to_certificate_model


class TestCertificateFormatter(unittest.TestCase):
    def test_certificate_to_award(self):
        with open('data/1.2/sample-cert.json') as cert_file:
            certificate_json = json.load(cert_file)
            certificate_model = to_certificate_model(certificate_json)
            award = certificate_formatter.certificate_to_award(certificate_model)
            self.assertEquals(award['title'], 'Game of Thrones Character')
            self.assertEquals(award['issuedOn'], '2016-09-29')
            self.assertEquals(award['name'], 'Arya Stark')




if __name__ == '__main__':
    unittest.main()
