from argparse import ArgumentParser

from peewee import SqliteDatabase

from models import Racers
from reporter.reporter import build_report


def send_report_to_database(log_files_path: str, db_path: str):
    """Put the logfiles data to the database."""
    database = SqliteDatabase(db_path)
    Racers.bind(database)
    Racers.create_table()
    report_dict = build_report(log_files_path, return_type='dict_dict')
    for abb, data in report_dict.items():
        Racers.create(
            position=data['position'],
            ABR=abb,
            racer_name=data['racer_name'],
            team=data['team'],
            time=data['time'],
            )


if __name__ == "__main__":
    # CLI
    parser = ArgumentParser(
        description='Migrate the logfiles data to the database',
        )
    parser.add_argument(
        '--logfiles',
        action='store',
        dest='path',
        help='the .log files folder path',
        )
    parser.add_argument(
        '--database',
        action='store',
        dest='db',
        help='the database file path',
        )
    args = parser.parse_args()
    send_report_to_database(args.path, args.db)
