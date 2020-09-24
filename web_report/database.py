from peewee import IntegerField, Model, SqliteDatabase, TextField

from reporter.reporter import build_report

PROJECT_PATH = '/home/user/Desktop/task-9-convert-and-store-data-to-the-database'

db = SqliteDatabase('report.db')


class Racers(Model):
    """The database model implementing class.

    Args:
        Model (class): The class Racers inherit
    """
    position = IntegerField(index=True)
    ABR = TextField(primary_key=True)
    racer_name = TextField(null=False)
    team = TextField()
    time = TextField()

    class Meta:
        database = db


def create_report_database():
    """Create the report database file."""
    Racers.create_table()
    report_dict = build_report(
        f'{PROJECT_PATH}/web_report/log_files/', 
        return_type='dict_dict',
        )
    for abb, data in report_dict.items():
        Racers.create(
            position=data['position'],
            ABR=abb,
            racer_name=data['racer_name'],
            team=data['team'],
            time=data['time'],
        )


def convert_database_to_dict() -> dict:
    """Convert report database to dict.

    Returns:
        dict: usable dictionary of report
    """
    query = Racers.select()
    racers_selected = query.dicts().execute()
    result = {}
    for item in racers_selected:
        result[item.pop('ABR')] = item
    return result


if __name__ == "__main__":
    create_report_database()
