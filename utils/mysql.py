import os
import mysql.connector
from mysql.connector import Error
import logging

from variables import ID, THERAPEUTIC_AREA, CREATED_AT, SITE_NAME, SITE_CATEGORY, TABLE_NAME


def connect_to_database(database):
    """
    Create the connection to the MySQL Database. Host, user and password come from environment variables.
    :param database: str
        Name of the database
    :return: MySQL connector
    """
    host = os.getenv('HOST')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')

    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            buffered=True
        )
        return connection

    except Error as e:
        logging.error(f"Error: {e}")
        return None


def table_exists(connection, table_name):
    """
    Checks if a table exists.
    :param connection: MySQL connector
    :param table_name: str
        Name of the table we want to check the existence
    :return: bool
        True if the table exists, False otherwise
    """

    if connection is None:
        logging.info("Database connection is not established")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute(f"SHOW TABLES;")
        result = cursor.fetchall()
        tables = [table[0] for table in result]

        if table_name in tables:
            return True
        else:
            return False

    except Error as e:
        logging.error(f"Error: {e}")
        return False

    finally:
        if connection.is_connected():
            cursor.close()


def initialise_schema(connection):
    """
    Create an empty table with the provided schema.
    """
    query = f"""CREATE TABLE {TABLE_NAME}(
       {ID} varchar(100),
       {THERAPEUTIC_AREA} varchar(25),
       {CREATED_AT} timestamp,
       {SITE_NAME} varchar(50),
       {SITE_CATEGORY} varchar(20)
    )"""

    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Error as e:
        logging.error(f"Not possible to initialize schema: {e}")
    if connection.is_connected():
        cursor.close()
    return


def delete_rows(connection):
    """
    Clean the table before inserting new data.
    """
    query = f"""DELETE FROM {TABLE_NAME}"""
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Error as e:
        logging.error(f"Not possible to delete rows from table {TABLE_NAME}: {e}")
    if connection.is_connected():
        cursor.close()
    return
