import logging
import pymongo.errors
import sys
from pymongo import MongoClient

from creds import MONGODB_PARAMS


class MongoDBWrapper:
    def __init__(self):
        self.client = MongoClient(
            host=MONGODB_PARAMS['host'],
            port=MONGODB_PARAMS['port'],
            connect=True
        )
        self.db = None
        self.collections = {}
        self.check_database()

    def check_database(self):
        try:
            if MONGODB_PARAMS['database'] in self.client.list_database_names():
                self.delete_database(MONGODB_PARAMS['database'])
            self.create_database(MONGODB_PARAMS['database'])
        except pymongo.errors.ServerSelectionTimeoutError:
            logging.error("MongoDB parameters not correct. Check the creds.py file, or create it from creds_dummy.py." +
                          "If you don't want to use MongoDB, don't activate the --db flag.")
            sys.exit()

    def create_database(self, db_name):
        logging.debug("Database {} created".format(db_name))
        self.db = self.client[db_name]

    def delete_database(self, db_name):
        logging.debug("Database {} deleted".format(db_name))
        self.client.drop_database(db_name)

    def create_collection(self, collection_name, iteration):
        logging.debug("Collection {}{} created".format(collection_name, iteration))
        self.collections['{}{}'.format(collection_name, iteration)] = self.db['{}{}'.format(collection_name, iteration)]

    def delete_collection(self, collection_name, iteration):
        logging.debug("Collection {}{} deleted".format(collection_name, iteration))
        my_col = self.collections['{}{}'.format(collection_name, iteration)]
        my_col.drop()

    def insert_document_into_collection(self, collection_name, iteration, document):
        self.collections['{}{}'.format(collection_name, iteration)].insert_one(document)

    def insert_documents_into_collection(self, collection_name, iteration, documents):
        self.collections['{}{}'.format(collection_name, iteration)].insert_many(documents)

    def obtain_all_documents(self, collection_name, iteration):
        return self.collections['{}{}'.format(collection_name, iteration)].find({})
