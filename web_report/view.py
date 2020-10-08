"""Monaco 2018 Racing Web-Report module."""

from functools import lru_cache
from json import dumps
from xml.dom.minidom import parseString

from dicttoxml import dicttoxml
from flask import Flask, render_template, request

from models import (db_to_dict_for_json_xml, db_to_list_for_html,
                     get_driver_statistic, get_drivers_and_codes)

BEST_RESULTS_NUMBER = 15
BORDERLINE_LENGHT = 72
DATABASE_PATH = '/home/user/Desktop/task-9-convert-and-store-data-to-the-database/report.db'


@lru_cache()
def build_common_statistic_json() -> str:
    """Convert the report to json format.
    For the endpoint /api/v1/report/?format=json

    Returns:
        str: json formated report
    """
    return dumps(
        db_to_dict_for_json_xml(DATABASE_PATH),
        indent=4,
        separators=[', ', ' = '],
        ensure_ascii=False,
        )


@lru_cache()
def build_common_statistic_xml() -> str:
    """Convert the report to xml format.
    For the endpoint /api/v1/report/?format=xml

    Returns:
        str: xml formated report
    """
    return parseString(
        dicttoxml(
            db_to_dict_for_json_xml(DATABASE_PATH),
            custom_root='report',
            attr_type=False,
            ),
            ).toprettyxml()


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
    report = db_to_list_for_html(DATABASE_PATH)
    # Insert the borderline between the best results and rest
    report.insert(BEST_RESULTS_NUMBER, '-' * BORDERLINE_LENGHT)
    if order == 'desc':  # For descending order
        report.reverse()
    return '<p>'.join(report)


@lru_cache()
def build_drivers_and_codes() -> str:
    """Build the template renderer parameter...
    For the endpoint /report/drivers

    Returns:
        str: the drivers and their codes-links table
    """
    try:
        # Get the structure contains abbriviations and names
        report = get_drivers_and_codes(DATABASE_PATH)
    except Exception:
        return '<font color="red">Drivers list can not be build.</font>'
    # If driver_id not passedd
    drivers_codes = []
    for code, driver_name in report.items():
        # Convert to the link a code (a.k.a abbreviation, driver_id)
        html_link = f'<a href="/report/drivers/?driver_id={code}">{code}</a>'
        drivers_codes.append(f'{driver_name} {html_link}')
    return '<p>'.join(drivers_codes)


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
        return get_driver_statistic(DATABASE_PATH, driver_id)
    except Exception:
        name = '<font color="red">This driver does not exist</font>'
        driver_statistic = ''
    return {'name': name, 'driver_statistic': driver_statistic}


app = Flask(__name__)  # Init the flask application


@app.route('/api/v1/report/', methods=['GET'])
def get_report_formated():
    """Return formated statistic of Monaco 2018 Racing.

    Returns:
        [type]: Response in json or xml format
    """
    if request.args.get('format') not in {'json', 'xml'}:
        return {
            "status": 400,
            "message": "Bad Request",
            }
    elif request.args.get('format') == 'json':
        return build_common_statistic_json()
    elif request.args.get('format') == 'xml':
        return build_common_statistic_xml()


@app.route('/report/')
def show_report():
    """Show common statistic of Monaco 2018 Racing.

    Returns:
        Render the template
    """
    common_statistic = build_common_statistic(request.args.get('order'))
    return render_template(
        'web_report.html',
        title='Common Statistic:',
        report=common_statistic,
        )


@app.route('/report/drivers/')
def show_report_drivers():
    """Show drivers and codes of them or some driver statistic.

    Returns:
        Render the template
    """
    driver_id = request.args.get('driver_id')
    if driver_id:
        driver = build_driver(driver_id)
        return render_template(
            'web_report.html',
            title=driver['name'],
            report=driver['driver_statistic'],
            )
    return render_template(
        'web_report.html',
        title='Drivers and codes of them:',
        report=build_drivers_and_codes(),
        )


if __name__ == '__main__':
    app.run()
