"""The logic for the views."""

from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
from functools import lru_cache
from json import dumps
from database import convert_database_to_dict
from reporter.reporter import (
    BEST_RESULTS_NUMBER,
    build_report,
    print_driver_statistic,
    read_logfiles,
    )

BORDERLINE_LENGHT = 72
PROJECT_PATH = '/home/user/Desktop/task-9-convert-and-store-data-to-the-database'


@lru_cache()
def build_common_statistic(order: str) -> str:
    """Build the template renderer parameters...
    For the endpoints /report
                      /report/?order=[asc/desc]

    Args:
        order (str): the URL parameter

    Returns:
        [str]: The table of statistic
    """
    try:
        if order not in {'asc', 'desc', None}:
            raise ValueError('Value of argument will be asc or desc')
    except ValueError:
        return f'<font color="red">Sort order "{order}" not exist.</font>'
    try:
        report = build_report(f'{PROJECT_PATH}/web_report/log_files/')
    except Exception:
        return '<font color="red">report can not be build.</font>'
    # Insert the borderline between the best results and rest
    report.insert(BEST_RESULTS_NUMBER, '-' * BORDERLINE_LENGHT)
    if order == 'desc':  # For descending order
        report.reverse()
    return '<p>'.join(report)


@lru_cache()
def build_driver(driver_id: str) -> dict:
    """Build the template renderer parameters...
    For the endpoint /report/drivers/?driver_id=[something]

    Args:
        driver_id (str): the URL patameter

    Returns:
        [dict]: dictkeys are:
                'name' is driver name str
                'driver_statistic' is driver statistic str
    """
    try:
        # Get the structure contains abbriviations and names
        codes_drivers_teems = read_logfiles(
            f'{PROJECT_PATH}/web_report/log_files/',
            'abbreviations.txt',
            )
        # If driver_id passed
        name = codes_drivers_teems[driver_id][0]
        driver_statistic = print_driver_statistic(
            f'{PROJECT_PATH}/web_report/log_files/', name)
    except Exception:
        name = '<font color="red">This driver does not exist</font>'
        driver_statistic = ''
    return {'name': name, 'driver_statistic': driver_statistic}


@lru_cache()
def build_drivers_and_codes() -> str:
    """Build the template renderer parameter...
    For the endpoint /report/drivers

    Returns:
        str: the drivers and their codes-links table
    """
    try:
        # Get the structure contains abbriviations and names
        codes_drivers_teems = read_logfiles(
            f'{PROJECT_PATH}/web_report/log_files/',
            'abbreviations.txt',
            )
    except Exception:
        return '<font color="red">Drivers list can not be build.</font>'
    # If driver_id not passedd
    drivers_codes = []
    for code, driver_teem in codes_drivers_teems.items():
        # Convert to the link a code (a.k.a abbreviation, driver_id)
        html_link = f'<a href="/report/drivers/?driver_id={code}">{code}</a>'
        drivers_codes.append(f'{driver_teem[0]} {html_link}')
    return '<p>'.join(drivers_codes)


def build_common_statistic_json() -> str:
    """Convert the report to json format.
    For the endpoint /api/v1/report/?format=json

    Returns:
        str: json formated report
    """
    return dumps(
        convert_database_to_dict(),
        indent=4,
        separators=[', ', ' = '],
        ensure_ascii=False,
        )


def build_common_statistic_xml() -> str:
    """Convert the report to xml format.
    For the endpoint /api/v1/report/?format=xml

    Returns:
        str: xml formated report
    """
    return parseString(
        dicttoxml(
            convert_database_to_dict(),
            custom_root='report',
            attr_type=False,
            ),
            ).toprettyxml()
