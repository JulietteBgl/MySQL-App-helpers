import os

from queries import oncology_specialisation_rate, list_of_sites
from utils.format_logs import format_log, is_expected_format
from utils.get_args import args
from utils.mysql import connect_to_database, delete_rows, run_query
from utils.save_logs import insert_logs
from variables import DATABASE_NAME, LOGS_FOLDER_NAME
import logging

# logger settings
logging.basicConfig(level=logging.INFO, format='%(levelname)-5s [%(module)s - %(funcName)s: %(message)s')


def main(connection, files):
    if args.clean_table == 'True':
        logging.info('Deleting all rows in the table.')
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
        if not db_connection.is_connected():
            logging.error('Failed to connect to MYSQL.')
            exit(1)
    except Exception as e:
        logging.error(f"Exception occurred while connecting to the database: {e}")
        exit(1)

    json_files = [pos_json for pos_json in os.listdir(LOGS_FOLDER_NAME) if pos_json.endswith('.json')]
    logging.info('Starting main...')
    try:
        nb_rows = main(db_connection, json_files)
        logging.info(f'Inserted {nb_rows} rows out of {len(json_files)}.')
        logging.info('### Oncology specialisation rate per Academic site: ###')
        run_query(db_connection, oncology_specialisation_rate)
        logging.info('### List of sites with at least 10 trials during the 14 days: ###')
        run_query(db_connection, list_of_sites)
    except Exception as e:
        logging.error(f"Exception occurred in main function: {e}")
    finally:
        if db_connection.is_connected():
            logging.info('Closing MYSQL connection...')
            db_connection.close()
            logging.info('MYSQL connection closed.')
