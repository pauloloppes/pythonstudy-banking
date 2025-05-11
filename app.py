from flask import Flask, request, Response
from decimal import Decimal, getcontext, ROUND_DOWN
from entities.Customer import Customer
from mysql.connector import Error
from execution_logger import logger

from database import insert_new_customer_in_database
from database import fetch_customer_in_database
from database import fetch_all_customers_in_database
from database import insert_new_transaction_in_database
from database import insert_new_transfer_in_database
from database import fetch_history_in_database

#Necessary to round down numbers with more than two decimal digits
getcontext().rounding = ROUND_DOWN

app = Flask(__name__)
app.json.sort_keys = False #Don't change the order of json responses
app.json.ensure_ascii = False #Prevents problems with diacritics on json

@app.route('/')
def introduction():
    return '<h1>This is your bank! Hello</h1>'

@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        customer_list = fetch_all_customers_in_database()
        return_list = []
        for i in customer_list:
            return_list.append({
                "id": i.id,
                "name": i.name
                })
        logger.info("API - Fetched list of customers.")
        return return_list, 200, {'Content-Type': 'application/json'}
    except Error as error:
        logger.error(f"Database error - {repr(error)}")
        return {"message": "Não foi possível fazer operação no banco de dados."}, 500, {'Content-Type': 'application/json'}
    except Exception as error:
        logger.error(repr(error),exc_info=True)
        return {"message": "Ocorreu algum problema ao processar solicitação."}, 400, {'Content-Type': 'application/json'}

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer_by_id(id):
    try:
        customer = fetch_customer_in_database(id)
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "balance": round(customer.balance,2)
        }
        return customer_data, 200, {'Content-Type': 'application/json'}
    except IndexError as error:
        logger.error(repr(error),exc_info=True)
        return {"message":str(error)}, 404, {'Content-Type': 'application/json'}
    except Error as error:
        logger.error(f"Database error - {repr(error)}")
        return {"message": "Não foi possível fazer operação no banco de dados."}, 500, {'Content-Type': 'application/json'}
    except Exception as error:
        logger.error(repr(error),exc_info=True)
        return {"message": "Ocorreu algum problema ao processar solicitação."}, 400, {'Content-Type': 'application/json'}

@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        name = request.json['name']
        new_id = insert_new_customer_in_database(name)
        return {
            "message":"Cliente inserido com sucesso!",
            "new_customer_id": new_id
            }, 201, {'Content-Type': 'application/json'}
    except KeyError as error:
        logger.error(repr(error),exc_info=True)
        return {"message":f"Parâmetro não encontrado no request: {error}"}, 400, {'Content-Type': 'application/json'}
    except Error as error:
        logger.error(f"Database error - {repr(error)}")
        return {"message": "Não foi possível fazer operação no banco de dados."}, 500, {'Content-Type': 'application/json'}
    except Exception as error:
        logger.error(repr(error),exc_info=True)
        return {"message": "Ocorreu algum problema ao processar solicitação."}, 400, {'Content-Type': 'application/json'}

@app.route('/customers/<int:id>/transactions', methods=['GET'])
def get_customer_transactions(id):
    try:
        customer = fetch_customer_in_database(id)
        history = fetch_history_in_database(id)
        return_list = []
        for i in history:
            return_list.append({
                "description": i[0],
                "transaction_amount": round(i[1],2),
                "resulting_balance": round(i[2],2),
                "transaction_date": i[3].strftime("%Y-%m-%d %H:%M:%S")
            })
        return {
            "customer_id": customer.id,
            "name": customer.name,
            "transaction_list": return_list
        }, 200, {'Content-Type': 'application/json'}
    except IndexError as error:
        logger.error(repr(error),exc_info=True)
        return {"message":str(error)}, 404, {'Content-Type': 'application/json'}
    except Error as error:
        logger.error(f"Database error - {repr(error)}")
        return {"message": "Não foi possível fazer operação no banco de dados."}, 500, {'Content-Type': 'application/json'}
    except Exception as error:
        logger.error(repr(error),exc_info=True)
        return {"message": "Ocorreu algum problema ao processar solicitação."}, 400, {'Content-Type': 'application/json'}

@app.route('/customers/<int:id>/transactions', methods=['POST'])
def add_customer_transaction(id):
    try:
        customer = fetch_customer_in_database(id)
        transaction_type = request.json['transaction_type']
        amount = round(Decimal(request.json['amount']),2)
        if (amount > 0):
            if (transaction_type == 'deposit'):
                new_balance = customer.deposit(amount)
                transaction_id = insert_new_transaction_in_database(customer,amount,"Depósito")
                return {
                    "message": f"Depósito efetuado!",
                    "transaction_id": transaction_id,
                    "new_balance": round(new_balance,2)
                }, 201, {'Content-Type': 'application/json'}
            elif (transaction_type== 'withdraw'):
                new_balance = customer.withdraw(amount)
                transaction_id = insert_new_transaction_in_database(customer,amount,"Saque")
                return {
                    "message": f"Saque efetuado!",
                    "transaction_id": transaction_id,
                    "new_balance": round(new_balance,2)
                }, 201, {'Content-Type': 'application/json'}
            elif (transaction_type == 'transfer'):
                id_customer_receive = request.json['id_customer_receive']
                if (id == id_customer_receive):
                    raise ValueError("Não é possível transferir para a mesma conta.")
                customer_receive = fetch_customer_in_database(id_customer_receive)
                new_balance = customer.transfer_send(amount,customer_receive.name)
                customer_receive.transfer_receive(amount,customer.name)
                transaction_sent_id,transaction_received_id = insert_new_transfer_in_database(customer,amount,customer_receive)
                return {
                    "message": f"Transferência efetuada!",
                    "transaction_sent_id": transaction_sent_id,
                    "transaction_received_id": transaction_received_id,
                    "new_balance": round(new_balance,2)
                }, 201, {'Content-Type': 'application/json'}
            else:
                raise ValueError("Tipo inválido de transação.")
        else:
            raise ValueError("Valor deve ser uma quantia acima de zero.")
    except KeyError as error:
        logger.error(repr(error),exc_info=True)
        return {"message":f"Parâmetro não encontrado no request: {error}"}, 400, {'Content-Type': 'application/json'}
    except IndexError as error:
        logger.error(repr(error),exc_info=True)
        return {"message":str(error)}, 404, {'Content-Type': 'application/json'}
    except ValueError as error:
        logger.error(repr(error),exc_info=True)
        return {"message":str(error)}, 400, {'Content-Type': 'application/json'}
    except Error as error:
        logger.error(f"Database error - {repr(error)}")
        return {"message": "Não foi possível fazer operação no banco de dados."}, 500, {'Content-Type': 'application/json'}
    except Exception as error:
        logger.error(repr(error),exc_info=True)
        return {"message": "Ocorreu algum problema ao processar solicitação."}, 400, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)