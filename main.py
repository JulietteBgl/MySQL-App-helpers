import os

from utils.clean_logs import format_log, is_expected_format
from utils.get_args import args
from utils.mysql import connect_to_database, delete_rows
from save_logs import insert_logs
from variables import DATABASE_NAME, LOGS_FOLDER_NAME
import logging

# logger settings
logging.basicConfig(level=logging.INFO, format='%(levelname)-5s [%(module)s - %(funcName)s: %(message)s')


def main(connection, files):
    if args.clean_table:
        delete_rows(connection)
    nb_rows_inserted = 0
    for file_path in files:
        with open(f'applications/{file_path}', 'r') as f:
            log = f.read()
        formatted_log = format_log(log)
        if is_expected_format(formatted_log):
            nb_rows_inserted += insert_logs(connection, formatted_log)
        else:
            logging.error(f"log {formatted_log} doesn't follow the expected format and can't be added to the database")
    return nb_rows_inserted


if __name__ == "__main__":
    logging.info('Opening MYSQL connection...')

    try:
        db_connection = connect_to_database(DATABASE_NAME)
        if db_connection.is_connected():
            logging.info('MYSQL connection established.')
        else:
            logging.error('Failed to connect to MYSQL.')
            exit(1)  # RAISE ERROR
    except Exception as e:
        logging.error(f"Exception occurred while connecting to the database: {e}")
        exit(1)

    logging.info('Reading logs...')
    json_files = [pos_json for pos_json in os.listdir(LOGS_FOLDER_NAME) if pos_json.endswith('.json')]
    logging.info('Starting main...')
    try:
        nb_rows = main(db_connection, json_files)
        logging.info(f'Inserted {nb_rows} rows out of {len(json_files)}.')
    except Exception as e:
        logging.error(f"Exception occurred in main function: {e}")
    finally:
        logging.info('Closing MYSQL connection...')
        if db_connection.is_connected():
            db_connection.close()
            logging.info('MYSQL connection closed.')
        else:
            logging.error('MYSQL connection was already closed.')
