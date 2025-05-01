from mysql.connector import connect, Error
from .database_variables import database_dictionary

def insert_new_customer_in_database(name):
    db_query = f"""
    INSERT INTO customers (name,balance)
    VALUES ('{name}', 0)
    """
    try:
        with connect(
            **database_dictionary
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(db_query)
                connection.commit()
                return cursor.lastrowid
    except Error as e:
        raise Exception(e.msg)