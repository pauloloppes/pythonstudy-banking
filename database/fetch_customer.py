from mysql.connector import connect, Error
from entities.Customer import Customer
from .database_variables import database_dictionary
from .database_logger import logger

def fetch_customer_in_database(id):
    db_query = f"""
    SELECT name,balance FROM customers
    WHERE id={id}
    """
    try:
        with connect(
            **database_dictionary
        ) as connection:
            with connection.cursor() as cursor:
                logger.debug(f"SQL query executed:{db_query}")
                cursor.execute(db_query)
                result = cursor.fetchall()
                if not result:
                    logger.info(f"Customer with ID {id} not found on database.")
                    raise IndexError(f"Cliente com ID {id} não encontrado!")
                return Customer(result[0][0],result[0][1],id)
    except Error as e:
        logger.error(e)
        raise e

def fetch_all_customers_in_database():
    db_query = f"""
    SELECT name,id FROM customers
    """

    try:
        with connect(
            **database_dictionary
        ) as connection:
            with connection.cursor() as cursor:
                logger.debug(f"SQL query executed:{db_query}")
                cursor.execute(db_query)
                result = cursor.fetchall()
                if not result:
                    logger.info(f"Nenhum cliente encontrado!")
                    raise IndexError("Nenhum cliente encontrado!")
                customer_list = []
                for i in result:
                    customer_list.append(Customer(i[0],id=i[1]))
                return customer_list
    except Error as e:
        logger.error(e)
        raise e