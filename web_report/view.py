"""Monaco 2018 Racing Web-Report module."""

from json import dumps
from xml.dom.minidom import parseString

from dicttoxml import dicttoxml
from flask import Flask, render_template, request

from models import (
    db_to_dict_for_json_xml,
    db_to_list_for_html,
    get_driver_statistic,
    get_drivers_and_codes,
    )

BEST_RESULTS_NUMBER = 15
BORDERLINE_LENGHT = 72
DATABASE_PATH = __file__.replace('web_report/view.py', 'report.db')


app = Flask(__name__)  # Init the flask application


@app.route('/api/v1/report/', methods=['GET'])
def get_report_formated():
    """Return formated statistic of Monaco 2018 Racing.

    Returns:
        [type]: Response in json or xml format
    """
    report_format = request.args.get('format')
    if report_format is None:
        report_format = 'json'
    if report_format not in {'json', 'xml'}:
        return {
            "status": 400,
            "message": "Bad Request",
            }
    elif report_format == 'json':
        return dumps(
            db_to_dict_for_json_xml(DATABASE_PATH),
            indent=4,
            separators=[', ', ' = '],
            ensure_ascii=False,
            )
    elif report_format == 'xml':
        return parseString(
            dicttoxml(
                db_to_dict_for_json_xml(DATABASE_PATH),
                custom_root='report',
                attr_type=False,
                ),
                ).toprettyxml()


@app.route('/report/')
def show_report():
    """Show common statistic of Monaco 2018 Racing.

    Returns:
        Render the template
    """
    order = request.args.get('order')
    template = 'common_statistic.html'
    try:
        if order not in {'asc', 'desc', None}:
            raise ValueError('An order value must be ´asc´ or ´desc´')
    except ValueError:
        return render_template(template, error='invalid_order')
    try:
        data = db_to_list_for_html(DATABASE_PATH, ' |')
        data.insert(BEST_RESULTS_NUMBER, '-' * BORDERLINE_LENGHT)
        if order == 'desc':
            data.reverse()
        return render_template(template, data=data)
    except Exception:
        return render_template(template, error='data_unevalable')


@app.route('/report/drivers/')
def show_report_drivers():
    """Show drivers and codes of them or some driver statistic.

    Returns:
        Render the template
    """
    driver_id = request.args.get('driver_id')
    if driver_id:
        template = 'driver_statistic.html'
        try:
            return render_template(
                template,
                data=get_driver_statistic(DATABASE_PATH, driver_id),
                )
        except Exception:
            return render_template(template, error='unknown_code')
    template = 'drivers_and_codes.html'
    try:
        return render_template(
            template,
            data=get_drivers_and_codes(DATABASE_PATH),
            )
    except Exception:
        return render_template(template, error='data_unevalable')


if __name__ == '__main__':
    app.run()
