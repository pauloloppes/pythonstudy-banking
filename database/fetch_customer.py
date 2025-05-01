from mysql.connector import connect, Error
from entities.Customer import Customer
from .database_variables import database_dictionary

def fetch_customer_in_database(id):
    db_query = f"""
    SELECT name,balance FROM customers
    WHERE id={id}
    """
    with connect(
        **database_dictionary
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(db_query)
            result = cursor.fetchall()
            if not result:
                raise IndexError(f"Cliente com ID {id} não encontrado!")
            return Customer(result[0][0],result[0][1],id)

def fetch_all_customers_in_database():
    db_query = f"""
    SELECT name,id FROM customers
    """

    with connect(
        **database_dictionary
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(db_query)
            result = cursor.fetchall()
            if not result:
                raise IndexError("Nenhum cliente encontrado!")
            customer_list = []
            for i in result:
                customer_list.append(Customer(i[0],id=i[1]))
            return customer_list