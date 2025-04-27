from mysql.connector import connect, Error
from .database_variables import database_dictionary

def test_database_connection():
    try:
        with connect(
            **database_dictionary
        ) as connection:
            db_query = "SHOW TABLES"
            with connection.cursor() as cursor:
                cursor.execute(db_query)
                print(cursor.fetchall())
    except Error as e:
        print(e)
