import logging
import pymongo.errors
import sys
from pymongo import MongoClient

from creds import MONGODB_PARAMS


class DBWrapper:
    """
    Wrapper for MongoDB
    """
    def __init__(self):
        """
        Creates the connection with the DB, and recreates the initial connection for a clean execution
        """
        if 'user' in MONGODB_PARAMS:
            self.client = MongoClient(
                username=MONGODB_PARAMS['user'],
                password=MONGODB_PARAMS['pass'],
                host=MONGODB_PARAMS['host'],
                port=MONGODB_PARAMS['port'],
                connect=True
            )
        else:
            self.client = MongoClient(
                host=MONGODB_PARAMS['host'],
                port=MONGODB_PARAMS['port'],
                connect=True
            )
        self.db = None
        self.collections = {}
        self.check_database()
        self.current_collection = None

    def check_database(self):
        """
        Checks if the database exists in Mongo, deletes it if exists, and then creates a clean DB.
        :return:
        :rtype:
        """
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

    def create_collection(self, collection_name):
        logging.debug("Collection {} created".format(collection_name))
        self.collections['{}'.format(collection_name)] = \
            MongoCollectionWrapper('{}'.format(collection_name),
                                   self.db['{}'.format(collection_name)])

    def set_current_collection(self, collection_name):
        self.current_collection = MongoCollectionWrapper('{}'.format(collection_name),
                                                         self.db['{}'.format(collection_name)])

    def create_collection_and_set(self, collection_name):
        logging.debug("Collection {} created".format(collection_name))
        self.collections['{}'.format(collection_name)] = \
            MongoCollectionWrapper('{}'.format(collection_name),
                                   self.db['{}'.format(collection_name)])
        self.current_collection = MongoCollectionWrapper('{}'.format(collection_name),
                                                         self.db['{}'.format(collection_name)])

    def delete_collection(self, collection_name):
        logging.debug("Collection {} deleted".format(collection_name))
        my_col = self.collections['{}'.format(collection_name)]
        my_col.drop()

    def insert_document(self, collection_name, document):
        self.collections['{}'.format(collection_name)].insert_one(document)

    def insert_documents(self, collection_name, documents):
        self.collections['{}'.format(collection_name)].insert_many(documents)

    def obtain_all_documents(self, collection_name):
        return self.collections['{}'.format(collection_name)].find({})

    def clean_old_collections(self, base_collection_name):
        """
        Deletes the collections used in the previous iteration
        :param base_collection_name: name of collection in the previous iteration
        :type base_collection_name: str
        :return:
        :rtype:
        """
        self.delete_collection(
            '{}'.format('_'.join(base_collection_name.split('_')[:-1]))
        )
        self.delete_collection(
            '{}_{}'.format('_'.join(base_collection_name.split('_')[:-1]), 'filtered')
        )
        self.delete_collection(
            base_collection_name
        )

    def __iter__(self):
        return self.current_collection.__iter__()


class MongoCollectionWrapper:
    """
    Wrapper for MongoDB collection
    """
    def __init__(self, name, collection):
        self.name = name
        self.collection = collection

    def __setitem__(self, key, value):
        result = self.collection.replace_one({'_id': key}, value)
        if result.matched_count == 0:
            value['_id'] = key
            self.collection.insert_one(value)

    def __getitem__(self, item):
        return self.collection.find_one({'_id': item})

    def sort(self, field, order):
        return self.collection.sort(field, order)

    def limit(self, max_to_return):
        return self.collection.limit(max_to_return)

    def insert_many(self, documents):
        self.collection.insert_many(documents)

    def insert_one(self, document):
        self.collection.insert_one(document)

    def find(self, my_dict=None, sort=None, limit=None):
        if sort:
            if limit:
                return self.collection.find(my_dict).sort(sort[0], sort[1]).limit(limit)
            else:
                return self.collection.find(my_dict).sort(sort[0], sort[1])
        else:
                return self.collection.find(my_dict)

    def drop(self):
        self.collection.drop()

    def __iter__(self):
        for value in self.collection.find({}):
            yield value
        return
