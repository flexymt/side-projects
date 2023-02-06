# The table is created within a SQLite3 database


def create_table() -> None:
   sql = '''CREATE TABLE CAR_DATASET(
      PRICE INT NOT NULL,
      TIMESTAMP CHAR(20),
      CAR_STRING CHAR(500),
      YEAR CHAR(10),
      miles INT,
      CAR_MODEL CHAR(30),
      UNIQUE(PRICE, TIMESTAMP, CAR_STRING, YEAR, MILES, CAR_MODEL)
   )'''
   cursor.execute(sql)