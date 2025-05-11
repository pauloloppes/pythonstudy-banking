from app import app
from decimal import Decimal, getcontext, ROUND_DOWN
import pytest
import json

getcontext().rounding = ROUND_DOWN

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def request_header():
    return {"Content-Type":"application/json","Accept":"application/json"}

def test_get_all_customers(client):
    response = client.get('/customers')
    assert response.status_code == 200
    response_list = json.loads(response.data)
    assert len(response_list) > 0
    assert {"id":1,"name":"Paulo"} in response_list

def test_get_customer(client):
    response = client.get('/customers/2')
    assert response.status_code == 200
    response_dict = json.loads(response.data)
    assert response_dict["id"] == 2
    assert response_dict["name"] == "Alex"
    assert "balance" in response_dict.keys()

def test_create_customer(client,request_header):
    customer_name = "Francisco"
    customer_data = {"name":customer_name}
    response = client.post('/customers',data=json.dumps(customer_data),headers=request_header)
    assert response.status_code == 201
    response_dict = json.loads(response.data)
    assert response_dict["message"] == "Cliente inserido com sucesso!"
    assert "new_customer_id" in response_dict.keys()

def test_get_transactions(client):
    response = client.get('/customers/1/transactions')
    assert response.status_code == 200
    response_dict = json.loads(response.data)
    assert response_dict["name"] == "Paulo"
    assert len(response_dict["transaction_list"]) > 0
    oldest_transaction = {
        "description": "Depósito",
        "transaction_amount": "20.00",
        "resulting_balance": "50.00",
        "transaction_date": "2025-04-27 17:32:09"
    }
    assert oldest_transaction == response_dict["transaction_list"][-1]

def test_deposit(client,request_header):
    client_response = client.get('/customers/2')
    assert client_response.status_code == 200
    customer_response_dict = json.loads(client_response.data)
    old_balance = Decimal(customer_response_dict["balance"])
    amount = 30
    transaction_data = {"transaction_type":"deposit","amount":amount}
    transaction_response = client.post('/customers/2/transactions',data=json.dumps(transaction_data),headers=request_header)
    assert transaction_response.status_code == 201
    transaction_response_dict = json.loads(transaction_response.data)
    assert transaction_response_dict["message"] == "Depósito efetuado!"
    assert "transaction_id" in transaction_response_dict.keys()
    assert Decimal(transaction_response_dict["new_balance"]) == Decimal(old_balance+amount)

def test_withdraw(client,request_header):
    client_response = client.get('/customers/2')
    assert client_response.status_code == 200
    customer_response_dict = json.loads(client_response.data)
    old_balance = Decimal(customer_response_dict["balance"])
    amount = 5
    transaction_data = {"transaction_type":"withdraw","amount":amount}
    transaction_response = client.post('/customers/2/transactions',data=json.dumps(transaction_data),headers=request_header)
    assert transaction_response.status_code == 201
    transaction_response_dict = json.loads(transaction_response.data)
    assert transaction_response_dict["message"] == "Saque efetuado!"
    assert "transaction_id" in transaction_response_dict.keys()
    assert Decimal(transaction_response_dict["new_balance"]) == Decimal(old_balance-amount)

def test_transfer(client,request_header):
    client_response = client.get('/customers/2')
    assert client_response.status_code == 200
    customer_response_dict = json.loads(client_response.data)
    old_balance = Decimal(customer_response_dict["balance"])
    amount = 7
    transaction_data = {"transaction_type":"transfer","amount":amount,"id_customer_receive":1}
    transaction_response = client.post('/customers/2/transactions',data=json.dumps(transaction_data),headers=request_header)
    assert transaction_response.status_code == 201
    transaction_response_dict = json.loads(transaction_response.data)
    assert transaction_response_dict["message"] == "Transferência efetuada!"
    assert "transaction_sent_id" in transaction_response_dict.keys()
    assert "transaction_received_id" in transaction_response_dict.keys()
    assert Decimal(transaction_response_dict["new_balance"]) == Decimal(old_balance-amount)