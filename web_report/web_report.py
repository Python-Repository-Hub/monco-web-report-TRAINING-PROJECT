"""Monaco 2018 Racing Web-Report module."""

from flask import Flask, render_template, request
from logic import (
    build_common_statistic,
    build_driver,
    build_drivers_and_codes,
    build_common_statistic_json,
    build_common_statistic_xml,
    )

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
