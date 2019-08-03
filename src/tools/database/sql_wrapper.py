import logging
import mysql.connector

from creds import MYSQL_PARAMS
from settings.settings import MESSAGES


class SqlWrapper:
    """
    Wrapper for SQL Database
    """
    def __init__(self):
        """
        Creates the connection with the DB, and recreates the initial connection for a clean execution
        """
        self.host = MYSQL_PARAMS['host']
        self.user = MYSQL_PARAMS['user']
        self.password = MYSQL_PARAMS['pass']
        self.db_n = MYSQL_PARAMS['database']
        self.tb_n = MYSQL_PARAMS['table']

        self.connect()
        self.tables = {}

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                      user=self.user,
                                                      password=self.password,
                                                      database=self.db_n,
                                                      auth_plugin='mysql_native_password')
            logging.info(MESSAGES['MYSQL_CONN_SUCC'])
        except Exception as exc:
            logging.ERROR(MESSAGES['MYSQL_CONN_ERR'].format(exc))
            raise exc

    def create_database(self, db_name):
        logging.debug("Database {} created".format(db_name))

    def delete_database(self, db_name):
        logging.debug("Database {} deleted".format(db_name))

    def create_table(self, collection_name):
        logging.debug("Collection {} created".format(collection_name))

    def delete_table(self, collection_name):
        logging.debug("Collection {} deleted".format(collection_name))

    def insert_entry(self, collection_name, document):
        pass

    def insert_entries(self, collection_name, documents):
        pass

    def obtain_all_entries(self, collection_name):
        pass

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, collection_name):
        pass

    def __delitem__(self, key):
        pass


class SqlTableWrapper:
    """
    Wrapper for MongoDB collection
    """
    def __init__(self, name, table):
        self.name = name
        self.table = table

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, item):
        pass

    def remove(self, key):
        pass

    def pop(self, key=None):
        pass

    def append(self, item):
        pass

    def extend(self, item):
        pass

    def sort(self, key, reverse):
        pass

    def limit(self, max_to_return):
        pass

    def insert_many(self, documents):
        pass

    def insert_one(self, document):
        pass

    def find(self, my_dict=None, sort=None, limit=None):
        pass

    def drop(self):
        pass

    def __iter__(self):
        pass
