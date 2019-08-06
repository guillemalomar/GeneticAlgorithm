import logging
import pymongo.errors
import sys
from pymongo import MongoClient

from src.tools.database.settings import MONGO_MESSAGES


class MongodbDbWrapper:
    """
    Wrapper for Mongo Database
    """
    def __init__(self, params):
        """
        Creates the connection with the DB, and recreates the initial connection for a clean execution
        """
        self.params = params
        if 'user' in self.params:
            self.client = MongoClient(
                username=self.params['user'],
                password=self.params['pass'],
                host=self.params['host'],
                port=self.params['port'],
                connect=True
            )
        else:
            self.client = MongoClient(
                host=self.params['host'],
                port=self.params['port'],
                connect=True
            )
        self.db = None
        self.collections = {}
        self.check_database()

    def check_database(self):
        """
        Checks if the database exists in Mongo, deletes it if exists, and then creates a clean DB.
        """
        try:
            if self.params['database'] in self.client.list_database_names():
                self.delete_database(self.params['database'])
            self.create_database(self.params['database'])
            logging.debug(MONGO_MESSAGES["MONGODB_CONN_SUCC"])
        except pymongo.errors.ServerSelectionTimeoutError as exc:
            logging.error(MONGO_MESSAGES["MONGODB_CONN_ERR".format(exc)])
            sys.exit()

    def create_database(self, db_name):
        try:
            self.db = self.client[db_name]
            logging.debug(MONGO_MESSAGES["MONGODB_SUCC_CRE_DB"].format(db_name))
        except Exception as exc:
            logging.error(MONGO_MESSAGES["MONGODB_ERR_CRE_DB"].format(db_name, exc))

    def delete_database(self, db_name):
        try:
            self.client.drop_database(db_name)
            logging.debug(MONGO_MESSAGES["MONGODB_SUCC_DEL_DB"].format(db_name))
        except Exception as exc:
            logging.error(MONGO_MESSAGES["MONGODB_ERR_DEL_DB"].format(db_name, exc))

    def create_collection(self, collection_name):
        try:
            self.collections['{}'.format(collection_name)] = \
                MongodbCollectionWrapper('{}'.format(collection_name),
                                         self.db['{}'.format(collection_name)])
            logging.debug(MONGO_MESSAGES["MONGODB_SUCC_CRE_COLL"].format(collection_name))
        except Exception as exc:
            logging.error(MONGO_MESSAGES["MONGODB_ERR_CRE_COLL"].format(collection_name, exc))

    def delete_collection(self, collection_name):
        try:
            self.collections['{}'.format(collection_name)].drop()
            logging.debug(MONGO_MESSAGES["MONGODB_SUCC_DEL_COLL"].format(collection_name))
        except Exception as exc:
            logging.error(MONGO_MESSAGES["MONGODB_ERR_DEL_COLL".format(collection_name, exc)])

    def insert_document(self, collection_name, document):
        self.collections['{}'.format(collection_name)].insert_one(document)

    def insert_documents(self, collection_name, documents):
        self.collections['{}'.format(collection_name)].insert_many(documents)

    def obtain_all_documents(self, collection_name):
        return self.collections['{}'.format(collection_name)].find({})

    def __setitem__(self, key, value):
        if key not in self.collections:
            self.create_collection(key)
        self.collections[key].insert_one(value)

    def __getitem__(self, collection_name):
        if collection_name not in self.collections:
            self.collections[collection_name] = MongodbCollectionWrapper(
                collection_name,
                self.db['{}'.format(collection_name)]
            )
        return self.collections[collection_name]

    def __delitem__(self, key):
        self.delete_collection(key)
        del self.collections[key]


class MongodbCollectionWrapper:
    """
    Wrapper for MongoDB collection
    """
    def __init__(self, name, collection):
        self.name = name
        self.collection = collection

    def __setitem__(self, key, value):
        self.collection.delete_one({'_id': key})
        result = self.collection.replace_one({'_id': key}, value)
        if result.matched_count == 0:
            value['_id'] = key
            self.collection.insert_one(value)

    def __getitem__(self, item):
        if not isinstance(item, slice):
            return self.collection.find_one({'_id': item})
        else:
            return self.collection.find({})

    def remove(self, key):
        self.collection.delete_one({'_id': key})

    def pop(self, key=None):
        if key:
            self.collection.delete_one({'_id': key})

    def append(self, item):
        self.collection.insert_one(item)

    def extend(self, item):
        self.collection.insert_many(item)

    def sort(self, key, reverse):
        to_sort = str(key).split('\'')[1]
        reverse = -1 if reverse else 1
        for idx, item in enumerate(self.collection.find({}).sort(to_sort, reverse)):
            self[idx] = item

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
