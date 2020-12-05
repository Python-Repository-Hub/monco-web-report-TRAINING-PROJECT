"""The unit tests for the reporter module."""

from unittest import TestCase, main
from web_report.view import app


class TestReporterMethods(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_report_formated(self):
        response = self.client.get('/api/v1/report/').get_data(as_text=True)
        response_json = self.client.get('/api/v1/report/?format=json').get_data(as_text=True)
        self.assertEqual(115, response_json.count('\n'))
        response_xml = self.client.get('/api/v1/report/?format=xml').get_data(as_text=True)
        self.assertIn('<report>', response_xml)
        self.assertEqual(response, response_json)

    def test_show_report(self):
        response = self.client.get('/report/').get_data(as_text=True)
        response_asc = self.client.get('/report/?order=asc').get_data(as_text=True)
        sample = "<p>15 |Kevin Magnussen |HAAS FERRARI |0:01:13.393000</p>\n        \n          <p>------------------------------------------------------------------------</p>"
        self.assertIn(sample, response_asc)

        response_desc = self.client.get('/report/?order=desc').get_data(as_text=True)
        sample_desc = "<p>16 |Daniel Ricciardo |RED BULL RACING TAG HEUER |0:02:47.987000</p>\n        \n          <p>------------------------------------------------------------------------</p>"
        self.assertIn(sample_desc, response_desc)

        self.assertEqual(response, response_asc)

    def test_show_report_drivers(self):
        response_drivers = self.client.get('/report/drivers/').get_data(as_text=True)
        sample = 'Valtteri Bottas <a href="/report/drivers/?driver_id=VBM">VBM</a>'
        self.assertIn(sample, response_drivers)

        response_spf = self.client.get('/report/drivers/?driver_id=SPF').get_data(as_text=True)
        self.assertIn('7 |FORCE INDIA MERCEDES |0:01:12.848000', response_spf)
        self.assertIn('Sergio Perez', response_spf)


if __name__ == '__main__':
    main()
