"""The unit tests for the reporter module."""

from unittest import TestCase, main
from sys import path
from os.path import dirname

path.append(dirname(dirname(__file__)))

from web_report.models import get_driver_statistic

class TestReporterMethods(TestCase):
    def test_get_driver_statistic_invalid_arg(self):
        with self.assertRaises(Exception):
            driver = get_driver_statistic(
'/home/user/Desktop/task-9-convert-and-store-data-to-the-database/report.db',
'AAA',
)


if __name__ == '__main__':
    main()
