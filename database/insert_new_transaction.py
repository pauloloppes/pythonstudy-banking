from mysql.connector import connect, Error
from .database_variables import database_dictionary

def insert_new_transaction_in_database(customer,amount,type):
    db_query_transaction = f"""
    INSERT INTO transactions (customer_id,amount,description,balance)
    VALUES ({customer.id}, {amount}, '{type}', {customer.balance})
    """

    db_query_update_balance = f"""
    UPDATE customers SET balance={customer.balance}
    WHERE id={customer.id}
    """
    
    try:
        with connect(
            **database_dictionary
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(db_query_transaction)
                cursor.execute(db_query_update_balance)
                connection.commit()
    except Error as e:
        print("Problema em banco de dados:",e.msg)
        connection.rollback()
        raise e

def insert_new_transfer_in_database(customer_send,amount,customer_receive):
    db_query_transaction_sent = f"""
    INSERT INTO transactions (customer_id,sent_customer_id,amount,description,balance)
    VALUES ({customer_send.id}, {customer_receive.id}, {amount}, 'Transferência enviada para {customer_receive.name}', {customer_send.balance})
    """

    db_query_transaction_received = f"""
    INSERT INTO transactions (customer_id,sent_customer_id,amount,description,balance)
    VALUES ({customer_receive.id}, {customer_send.id}, {amount}, 'Transferência recebida de {customer_send.name}', {customer_receive.balance})
    """

    db_query_update_sent = f"""
    UPDATE customers SET balance={customer_send.balance}
    WHERE id={customer_send.id}
    """

    db_query_update_received = f"""
    UPDATE customers SET balance={customer_receive.balance}
    WHERE id={customer_receive.id}
    """
    
    try:
        with connect(
            **database_dictionary
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(db_query_transaction_sent)
                cursor.execute(db_query_transaction_received)
                cursor.execute(db_query_update_sent)
                cursor.execute(db_query_update_received)
                connection.commit()
    except Error as e:
        print("Problema em banco de dados:",e.msg)
        connection.rollback()
        raise e