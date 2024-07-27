from variables import ID, THERAPEUTIC_AREA, CREATED_AT, SITE_NAME, SITE_CATEGORY, TABLE_NAME
from utils.mysql import table_exists, initialise_schema
from mysql.connector import Error
import logging


def insert_logs(db_connection, log):
    """
    Inserts logs in the target table.
    :param db_connection: MySQL connector
    :param log: dict
        formatted logs in a dict format
    """
    if not table_exists(db_connection, TABLE_NAME):
        logging.info("Table doesn't exist yet. Creating it.")
        initialise_schema(db_connection)

    query = f"""
    INSERT INTO {TABLE_NAME}({ID}, {THERAPEUTIC_AREA}, {CREATED_AT}, {SITE_NAME}, {SITE_CATEGORY})
    VALUES (%s, %s, %s, %s, %s);
    """
    # we want to make sure values are in the expected order, so we avoid the use of logs.values()
    values = [
        log.get('id', None),
        log.get('therapeutic_area', None),
        log.get('created_at', None),
        log.get('site', {}).get('site_name', None),
        log.get('site', {}).get('site_category', None)
    ]

    nb_row_inserted = 0
    try:
        cursor = db_connection.cursor()
        cursor.execute(query, values)
        db_connection.commit()
        nb_row_inserted += 1
    except Error as e:
        logging.error(f"Not possible insert log {log}: {e}")
    if db_connection.is_connected():
        cursor.close()
    return nb_row_inserted
