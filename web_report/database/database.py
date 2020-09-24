from peewee import (CharField, IntegerField, Model, SqliteDatabase, TextField,
                    TimeField)
from reporter.reporter import build_report


def create_report_database():
    db = SqliteDatabase('report.db')

    class Racers(Model):
        position = IntegerField(index=True, primary_key=True)
        ABR = CharField()
        racer_name = TextField(null=False)
        team = TextField()
        time = TimeField()

        class Meta:
            database = db

    Racers.create_table()
    report_dict = build_report(
        '/home/user/Desktop/task-9-convert-and-store-data-to-the-database/web_report/log_files/', 
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

if __name__ == "__main__"::
    create_report_database()
