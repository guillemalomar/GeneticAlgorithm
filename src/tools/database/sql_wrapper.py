import logging
import mysql.connector
import sys

from creds import MYSQL_PARAMS
from settings.settings import MESSAGES


class SqlWrapper:
    """
    Wrapper for SQL Database
    """
    def __init__(self, model):
        """
        Creates the connection with the DB, and recreates the initial connection for a clean execution
        """
        self.host = MYSQL_PARAMS['host']
        self.user = MYSQL_PARAMS['user']
        self.password = MYSQL_PARAMS['pass']
        self.db_n = MYSQL_PARAMS['database']
        self.tb_n = MYSQL_PARAMS['table']

        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.delete_database(self.db_n)
        self.create_database(self.db_n)
        self.use_database(self.db_n)
        self.tables = {}
        self.model = model

    def connect(self):
        try:
            connection = mysql.connector.connect(host=self.host,
                                                 user=self.user,
                                                 password=self.password,
                                                 auth_plugin='mysql_native_password')
            logging.info(MESSAGES['MYSQL_CONN_SUCC'])
            return connection
        except Exception as exc:
            logging.ERROR(MESSAGES['MYSQL_CONN_ERR'].format(exc))
            sys.exit()

    def use_database(self, db_name):
        try:
            self.cursor.execute('USE  {}'.format(db_name))
            logging.debug(MESSAGES["MYSQL_USE_SUCC"].format(db_name))
        except Exception as exc:
            logging.error(MESSAGES["MYSQL_USE_ERR"].format(db_name, exc))
            sys.exit()

    def create_database(self, db_name):
        try:
            self.cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
            self.db.commit()
            logging.debug(MESSAGES["MYSQL_SUCC_CRE_DB"].format(db_name))
        except Exception as exc:
            logging.error(MESSAGES["MYSQL_ERR_CRE_DB"].format(db_name, exc))

    def delete_database(self, db_name):
        try:
            self.cursor.execute('DROP DATABASE IF EXISTS {}'.format(db_name))
            self.db.commit()
            logging.debug(MESSAGES["MYSQL_SUCC_DEL_DB"].format(db_name))
        except Exception as exc:
            logging.error(MESSAGES["MYSQL_ERR_DEL_DB"].format(db_name, exc))

    def create_table(self, table_name):
        try:
            values = ''.join(['`' + x + '` float(20), ' for x, y in self.model.items()])[:-2]
            to_exec = 'CREATE TABLE `{}` (`_id` int(11), `age` int(11), `value` float(20), {}, PRIMARY KEY (`_id`));' \
                if '_id' not in values else 'CREATE TABLE `{}` ({}, PRIMARY KEY (`_id`));'
            self.cursor.execute(
                to_exec.format(table_name, values)
            )
            self.tables[table_name] = SqlTableWrapper(table_name, self.db, self.cursor, self.model)
            logging.debug(MESSAGES["MYSQL_SUCC_CRE_TAB"].format(table_name))
        except Exception as exc:
            logging.error(MESSAGES["MYSQL_ERR_CRE_TAB"].format(table_name, exc))

    def delete_table(self, table_name):
        try:
            self.cursor.execute('DROP TABLE {}'.format(table_name))
            del self.tables[table_name]
            logging.debug(MESSAGES["MYSQL_SUCC_DEL_TAB"].format(table_name))
        except Exception as exc:
            logging.error(MESSAGES["MYSQL_ERR_DEL_TAB"].format(table_name, exc))

    def insert_entry(self, table_name, item):
        self.tables[table_name].append(item)

    def insert_entries(self, table_name, items):
        self.tables[table_name].extend(items)

    def obtain_all_entries(self, table_name):
        self.tables[table_name].find()

    def __setitem__(self, table_name, value):
        if table_name not in self.tables:
            self.create_table(table_name)
        self.tables[table_name].insert_one(value)

    def __getitem__(self, table_name):
        if table_name not in self.tables:
            self.create_table(table_name)
        return self.tables[table_name]

    def __delitem__(self, table_name):
        self.delete_table(table_name)

    def __iter__(self, table_name):
        for value in self.tables[table_name].find():
            yield value
        return


class SqlTableWrapper:
    """
    Wrapper for SQL table
    """
    def __init__(self, name, db, cursor, model):
        self.name = name
        self.cursor = cursor
        self.model = model
        self.db = db

    def __setitem__(self, key, value):
        self.delete_one(key)
        value['_id'] = key
        self.append(value)

    def __getitem__(self, item):
        column_names = ', '.join(x for x in self.model.keys()) + ', `_id`, `age`, `value`'
        self.cursor.execute('SELECT {} FROM `{}` WHERE `_id` = {} LIMIT 1;'.format(column_names, self.name, item))
        results = self.cursor.fetchall()
        if len(results) > 0:
            individual = dict(self.model)
            ind = False
            for ind, key in enumerate(individual.keys()):
                individual[key] = results[0][ind]
            if ind:
                individual['_id'] = results[0][ind + 1]
                individual['age'] = results[0][ind + 2]
                individual['value'] = results[0][ind + 3]
            return individual
        else:
            return

    def remove(self, key):
        self.delete_one(key)

    def pop(self, key=None):
        if key:
            self.delete_one(key)

    def append(self, item):
        column_names = ', '.join(x for x in item.keys() if x in self.model.keys())
        column_values = ', '.join(str(y) for x, y in item.items() if x in self.model.keys())
        if '_id' not in column_names:
            query = 'INSERT INTO `{}` (`_id`, `age`, `value`, {}) VALUES ({}, {}, {}, {})'
            self.cursor.execute(query.format(
                self.name,
                column_names,
                item['_id'],
                item['age'],
                item['value'],
                column_values)
            )
            self.db.commit()
        else:
            query = 'INSERT INTO `{}` ({}) VALUES ({})'
            self.cursor.execute(query.format(
                self.name,
                column_names,
                column_values)
            )
            self.db.commit()

    def extend(self, items):
        for item in items:
            self.append(item)

    def sort(self, key, reverse):
        column_names = ', '.join(x for x in self.model.keys()) + ', `_id`, `age`, `value`'
        to_sort = str(key).split('\'')[1]
        query = 'SELECT {} FROM `{}` ORDER BY `{}`'
        query += ' DESC' if reverse else ' ASC'
        self.cursor.execute(query.format(column_names, self.name, to_sort))
        results = self.cursor.fetchall()
        for ind, entry in enumerate(results):
            individual = dict(self.model)
            ind2 = False
            for ind2, key in enumerate(individual.keys()):
                individual[key] = entry[ind2]
            if ind2:
                individual['_id'] = entry[ind2 + 1]
                individual['age'] = entry[ind2 + 2]
                individual['value'] = entry[ind2 + 3]
            self[ind] = individual

    def limit(self, max_to_return):
        column_names = ', '.join(x for x in self.model.keys()) + ', `_id`, `age`, `value`'
        query = 'SELECT {} FROM `{}` LIMIT `{}`'
        self.cursor.execute(query.format(column_names, self.name, max_to_return))
        results = self.cursor.fetchall()
        individuals = []
        for ind, entry in enumerate(results):
            individual = dict(self.model)
            ind2 = False
            for ind2, key in enumerate(individual.keys()):
                individual[key] = entry[ind2]
            if ind2:
                individual['_id'] = entry[ind2 + 1]
                individual['age'] = entry[ind2 + 2]
                individual['value'] = entry[ind2 + 3]
                individuals.append(individual)
        return individuals

    def insert_many(self, items):
        for item in items:
            self.append(item)

    def insert_one(self, item):
        self.append(item)

    def delete_one(self, key):
        self.cursor.execute('DELETE FROM {} WHERE `_id` = {}'.format(self.name, key))
        self.db.commit()

    def find(self):
        column_names = ', '.join(x for x in self.model.keys()) + ', `_id`, `age`, `value`'
        self.cursor.execute('SELECT {} FROM `{}`;'.format(column_names, self.name))
        results = self.cursor.fetchall()
        individuals = []
        for entry in results:
            individual = dict(self.model)
            ind = False
            for ind, key in enumerate(individual.keys()):
                individual[key] = entry[ind]
            if ind:
                individual['_id'] = entry[ind + 1]
                individual['age'] = entry[ind + 2]
                individual['value'] = entry[ind + 3]
                individuals.append(individual)
        return individuals

    def drop(self, key):
        self.delete_one(key)

    def __iter__(self):
        for value in self.find():
            yield value
        return

    def check_size(self):
        self.cursor.execute('SELECT COUNT(*) FROM {}'.format(self.name))
        results = self.cursor.fetchall()
        return results[0][0]
