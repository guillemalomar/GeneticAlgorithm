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
        if MONGODB_PARAMS['database'] in self.client.list_database_names():
            self.delete_database(MONGODB_PARAMS['database'])
        self.create_database(MONGODB_PARAMS['database'])

    def create_database(self, db_name):
        self.db = self.client[db_name]

    def delete_database(self, db_name):
        self.client.drop_database(db_name)

    def create_collection(self, iteration):
        self.collections[iteration] = self.db['Iteration{}'.format(iteration)]

    def delete_collection(self, iteration):
        my_col = self.collections[iteration]
        my_col.drop()

    def insert_document_into_collection(self, iteration, document):
        self.collections[iteration].insert_one(document)

    def insert_documents_into_collection(self, iteration, documents):
        for document in documents:
            self.collections[iteration].insert_one(document)

    def obtain_all_documents(self, iteration):
        return self.collections[iteration].find({})
