MESSAGES = {
    "WRONG_DATABASE": "The specified database is not available. Choose MongoDB or MySQL."
}

MONGO_MESSAGES = {
    "MONGODB_CONN_SUCCESS": "Success connecting to MongoDB",
    "MONGODB_CONN_ERROR": "MongoDB parameters not correct. Check the creds.py file, or create it from creds_dummy.py. {}",
    "MONGODB_SUCCESS_CREATING_DB": "Success creating the MongoDB database: {}",
    "MONGODB_ERROR_CREATING_DB": "Error creating a database {}: {}",
    "MONGODB_SUCCESS_DELETING_DB": "Success deleting the MongoDB database: {}",
    "MONGODB_ERROR_DELETING_DB": "Error deleting a database {}: {}",
    "MONGODB_SUCCESS_CREATING_COLL": "Success creating the MongoDB collection: {}",
    "MONGODB_ERROR_CREATING_COLL": "Error creating a collection {}: {}",
    "MONGODB_SUCCESS_DELETING_COLL": "Success deleting a collection: {}",
    "MONGODB_ERROR_DELETING_COLL": "Error deleting a collection {}: {}"
}

MYSQL_MESSAGES = {
    "MYSQL_CONN_SUCCESS": "Success connecting to MySQL",
    "MYSQL_CONN_ERROR": "Error connecting to MySQL: {}",
    "MYSQL_USE_SUCCESS": "Success using the database {}",
    "MYSQL_USE_ERROR": "Error using the database {}: {}",
    "MYSQL_SUCCESS_CREATING_DB": "Success creating the database {}",
    "MYSQL_ERROR_CREATING_DB": "Error creating the database {}: {}",
    "MYSQL_SUCCESS_DELETING_DB": "Success deleting the database {}",
    "MYSQL_ERROR_DELETING_DB": "Error deleting the database {}: {}",
    "MYSQL_SUCCESS_CREATING_TAB": "Success creating a table: {}",
    "MYSQL_ERROR_CREATING_TAB": "Error creating the table {}: {}",
    "MYSQL_SUCCESS_DELETING_TAB": "Success deleting a table: {}",
    "MYSQL_ERROR_DELETING_TAB": "Error deleting the table {}: {}",
    "SELECT_QUERY": "SELECT {} FROM `{}`",
    "INSERT_QUERY": "INSERT INTO `{}` ({}) VALUES ({})",
    "INSERT_QUERY_2": "INSERT INTO `{}` (`_id`, `age`, `value`, {}) VALUES ({}, {}, {}, {})",
    "SELECT_ONE_QUERY": "SELECT {} FROM `{}` WHERE `_id` = {} LIMIT 1",
    "SELECT_LIMIT_QUERY": "SELECT {} FROM `{}` LIMIT `{}`",
    "COUNT_QUERY": "SELECT COUNT(*) FROM {}",
    "SORT_QUERY": "SELECT {} FROM `{}` ORDER BY `{}`",
    "DELETE_ONE_QUERY": "DELETE FROM {} WHERE `_id` = {}",
    "DROP_TABLE_QUERY": "DROP TABLE {}",
    "CREATE_DB_QUERY": "CREATE DATABASE IF NOT EXISTS {}",
    "DROP_DB_QUERY": "DROP DATABASE IF EXISTS {}",
    "USE_QUERY": ""
}
