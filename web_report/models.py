"""The database works logic."""

from peewee import IntegerField, Model, SqliteDatabase, TextField
from playhouse.shortcuts import model_to_dict


class Racers(Model):
    """The database model implementing class.

    Args:
        Model (class): The class Racers inherit
    """
    position = IntegerField(null=False)
    ABR = TextField(primary_key=True)
    racer_name = TextField(null=False)
    team = TextField(null=False)
    time = TextField(null=False)


def db_to_dict_for_json_xml(database_path: str) -> dict:
    """Convert report database to dict.

    Returns:
        dict: usable dictionary of report
    """
    Racers.bind(SqliteDatabase(database_path))
    racers = Racers.select()
    result = {}
    for item in racers.execute():
        record = model_to_dict(item)
        result[record.pop('ABR')] = record
    return result


def db_to_list_for_html(database_path: str) -> list:
    Racers.bind(SqliteDatabase(database_path))
    racers = Racers.select()
    result = []
    for item in racers.execute():
        record = model_to_dict(item, exclude=[Racers.ABR])
        record['position'] = str(record['position'])
        result.append(' |'.join(list(record.values())))
    return result


def get_drivers_and_codes(database_path: str) -> dict:
    Racers.bind(SqliteDatabase(database_path))
    racers = Racers.select(Racers.racer_name, Racers.ABR)
    result = {}
    for item in racers.execute():
        record = model_to_dict(item, only=[Racers.racer_name, Racers.ABR])
        result[record['ABR']] = record['racer_name']
    return result


def get_driver_statistic(database_path: str, code: str) -> dict:
    Racers.bind(SqliteDatabase(database_path))
    driver = Racers.get_by_id(code)
    name = driver.racer_name
    record = model_to_dict(driver, exclude=[Racers.ABR, Racers.racer_name])
    record['position'] = str(record['position'])
    return {
        'name': name,
        'driver_statistic': ' |'.join(list(record.values())),
        }
