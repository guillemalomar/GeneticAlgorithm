initial_population_size = 1000
max_iterations = 100
mutation_factor = 0.05
elitism = True

MESSAGES = {
    "MYSQL_CONN_SUCC": "Success connecting to MySQL",
    "MYSQL_CONN_ERR": "Error connecting to MySQL: {}",
    "MYSQL_USE_SUCC": "Success using the database {}",
    "MYSQL_USE_ERR": "Error using the database {}: {}",
    "MYSQL_SUCC_CRE_DB": "Success creating the database {}",
    "MYSQL_ERR_CRE_DB": "Error creating the database {}: {}",
    "MYSQL_SUCC_DEL_DB": "Success deleting the database {}",
    "MYSQL_ERR_DEL_DB": "Error deleting the database {}: {}",
    "MYSQL_SUCC_CRE_TAB": "Success creating a table: {}",
    "MYSQL_ERR_CRE_TAB": "Error creating the table {}: {}",
    "MYSQL_SUCC_DEL_TAB": "Success deleting a table: {}",
    "MYSQL_ERR_DEL_TAB": "Error deleting the table {}: {}",
    "MONGODB_CONN_SUCC": "Success connecting to MongoDB",
    "MONGODB_CONN_ERR": "MongoDB parameters not correct. Check the creds.py file, or create it from creds_dummy.py. {}",
    "MONGODB_SUCC_CRE_DB": "Success creating the MongoDB database: {}",
    "MONGODB_ERR_CRE_DB": "Error creating a database {}: {}",
    "MONGODB_SUCC_DEL_DB": "Success deleting the MongoDB database: {}",
    "MONGODB_ERR_DEL_DB": "Error deleting a database {}: {}",
    "MONGODB_SUCC_CRE_COLL": "Success creating the MongoDB collection: {}",
    "MONGODB_ERR_CRE_COLL": "Error creating a collection {}: {}",
    "MONGODB_SUCC_DEL_COLL": "Success deleting a collection: {}",
    "MONGODB_ERR_DEL_COLL": "Error deleting a collection {}: {}",
    "WRONG_DATABASE": "The specified database is not available. Choose MongoDB or MySQL.",
    "CANCELLED_EXECUTION": "Execution cancelled manually",
    "POP_STAGE": "*** Population stage ***",
    "ITERATION_STAGE": "*** Iteration stage ***",
    "CLOSING_STAGE": "*** Closing stage ***",
    "MULTIPLE_AND_NAME": "The multiple flag has been activated, but a name for a single execution has been given. \n "
                         "Check your input parameters",
    "MULTIPLE_AND_PARAM": "The multiple flag has been activated, but single parameters have been specified. \n"
                          "Check your input parameters",
    "INCORR_PARAM_FORMAT": "The format of the parameters is incorrect.",
    "INCORR_PARAM_NUMBER": "The amount of parameters is incorrect.",
    "ABOUT_MESSAGE": 30 * "#" + " Genetic Algorithm " + 31 * "#" + '\n' +
                     "# This project is an example of the most classic Genetic Algorithm problem.    #\n" +
                     "# The default mode will obtain 1 or more environments, will create a set of    #\n" +
                     "# individuals with random parameters values within a specified range, and will #\n" +
                     "# show how these parameters change when facing the individuals against the     #\n" +
                     "# environments over many iterations.                                           #\n" +
                     80 * "#"
}
