import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def insert_into_db(car_dataset):
    sql_connection = create_connection('car_prices.db')
    cursor = sql_connection.cursor()
    for index, row in car_dataset.iterrows():
        price = row[0]
        timestamp = row[1]
        car_string = row[2]
        year = row[3]
        miles = row[4]
        car_model = row[5]
        sql = f"INSERT OR IGNORE INTO CAR_DATASET(PRICE,TIMESTAMP,CAR_STRING,YEAR,MILES,CAR_MODEL) VALUES({price},'{timestamp}','{car_string}',{year},{miles},'{car_model}');"
        cursor.execute(sql)
    sql_connection.commit() # Used to commit code to the database if auto commit is turned of. 