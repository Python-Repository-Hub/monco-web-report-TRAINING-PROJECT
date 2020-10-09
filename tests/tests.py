"""The unit tests for the reporter module."""

from unittest import TestCase, main
from sys import path

path.append(
    '/home/user/Desktop/Task_7_-_Web_report_of_Monaco_2018_Racing/web_report',
    )
from web_report.view import build_common_statistic, build_driver


class TestReporterMethods(TestCase):
    def test_build_common_statistic_invalid_arg(self):
        with self.assertRaises(ValueError):
            common_statistic = build_common_statistic('anyorder')

    def test_build_driver_invalid_arg(self):
        with self.assertRaises(ValueError):
            driver = build_driver('AAA')


if __name__ == '__main__':
    main()
