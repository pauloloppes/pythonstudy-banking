from mysql.connector import connect, Error
from .database_variables import database_dictionary
from .database_logger import logger

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
                logger.debug(f"SQL query executed:{db_query}")
                cursor.execute(db_query)
                connection.commit()
                customer_id = cursor.lastrowid
                logger.info(f"Customer created with ID {customer_id}.")
                return customer_id
    except Error as e:
        connection.rollback()
        logger.error(e)
        raise e