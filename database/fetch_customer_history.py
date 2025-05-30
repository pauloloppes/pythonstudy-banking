from mysql.connector import connect, Error
from entities.Customer import Customer
from .database_variables import database_dictionary
from .database_logger import logger

def fetch_history_in_database(id):
    db_query = f"""
    SELECT description,amount,balance,creation_date FROM transactions
    WHERE customer_id={id}
    ORDER BY creation_date DESC
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
                    logger.info("Histórico vazio para o cliente selecionado.")
                    raise IndexError("Histórico vazio para o cliente selecionado.")
                return result
    except Error as e:
        logger.error(e)
        raise e