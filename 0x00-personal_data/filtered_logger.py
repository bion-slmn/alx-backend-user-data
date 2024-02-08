#!/usr/bin/env python3
'''Defines a function that obfuscates user data'''
import re
from typing import List
import logging
import mysql.connector
import os


PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'name')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''function log message obfuscated'''
    for item in fields:
        message = re.sub(rf'{item}=.*?{separator}',
                         f'{item}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' formatting and removing senstive information'''
        msg = super().format(record)
        msg = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return msg


def get_logger() -> logging.Logger:
    '''create a logger object and display the log message to the
    console'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(console_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''connect to the database using mysql connector

    Return:
    mysql.connector.connection.MySQLConnection object'''
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    connector = mysql.connector.connect(host=db_host,
                                        database=db_name,
                                        user=db_username,
                                        password=db_pwd)
    return connector


def main() -> None:
    ''' connection using get_db and retrieve all
    rows in the users table and display each row under a filtered format'''
    logger = get_logger()
    column_name = ['name', 'email', 'phone', 'ssn', 'password',
                   'ip', 'last_login', 'user_agent']
    connector = get_db()
    cursor = connector.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        msg = [f"{name}={value}" for name, value in zip(column_name, row)]
        msg = '; '.join(msg) + ';'
        logger.info(msg)


if __name__ == '__main__':
    main()
