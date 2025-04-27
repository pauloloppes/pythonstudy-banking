from mysql.connector import connect, Error
from connection import database_variables

try:
    with connect(
        **database_variables.database_dictionary
    ) as connection:
        db_query = "SHOW TABLES"
        with connection.cursor() as cursor:
            cursor.execute(db_query)
            print(cursor.fetchall())
except Error as e:
    print(e)