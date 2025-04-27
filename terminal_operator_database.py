from entities.Customer import Customer
from database import insert_new_customer_in_database
from database import fetch_customer_in_database
from database import fetch_all_customers_in_database
from database import insert_new_transaction_in_database
from database import insert_new_transfer_in_database
from decimal import Decimal, getcontext, ROUND_DOWN

getcontext().rounding = ROUND_DOWN
client_list = []
option = 1

client_list.append(Customer("Dummy"))
client_list.append(Customer("Fake"))

def show_divisor():
    print("_"*30)

def show_main_menu():
    show_divisor()
    print("--MENU INICIAL--")
    print("Opções:")
    print("1. Cadastrar novo cliente")
    print("2. Listar clientes")
    print("3. Verificar saldo de cliente")
    print("4. Exibir extrato de cliente")
    print("5. Efetuar depósito")
    print("6. Efetuar saque")
    print("7. Efetuar transferência")
    show_divisor()
    print("0. Sair")
    print("Opção: >",end="")

def new_client():
    show_divisor()
    print("--CADASTRO DE CLIENTE--")
    print("Entre com o nome do novo cliente: >",end="")
    name = input()
    try:
        insert_new_customer_in_database(name)
        print("Cliente inserido com sucesso!")
    except Exception as error:
        print(error)

def list_clients():
    show_divisor()
    print("--LISTA DE CLIENTES--")
    print("ID / Nome")
    try:
        customer_list = fetch_all_customers_in_database()
        for i in customer_list:
            print(f"{i.id}    {i}")
    except Exception as error:
        print(error)

def check_balance():
    show_divisor()
    print("--VERIFICAR SALDO--")
    print("Entre com o ID do cliente: >",end="")
    customer_id = int(input())
    try:
        customer = fetch_customer_in_database(customer_id)
        print(f"Saldo de {customer.name}: R$ {customer.balance:.2f}")
    except Exception as error:
        print(error)

def show_history():
    print("--HISTÓRICO DE TRANSAÇÕES--")
    print("Entre com o ID do cliente: >",end="")
    customer_id = int(input())
    customer = client_list[customer_id]
    for i in customer.history[::-1]:
        print(f"{i[0]}: R$ {i[1]:.2f}, Saldo resultante R$ {i[2]:.2f}. Data/hora: {i[3]}")

def deposit():
    show_divisor()
    print("--EFETUAR DEPÓSITO--")
    print("Entre com o ID do cliente: >",end="")
    customer_id = int(input())
    try:
        customer = fetch_customer_in_database(customer_id)
        print("Entre com a quantia a ser depositada: >",end="")
        amount = round(Decimal(input()),2)
        if (amount > 0):
            new_balance = customer.deposit(amount)
            insert_new_transaction_in_database(customer,amount,"Depósito")
            print(f"Depósito efetuado! Novo saldo de {customer.name}: R$ {new_balance:.2f}")
        else:
            print("Valor inválido para depósito!")
    except Exception as error:
        print("Problema em operação:",error)

def withdraw():
    show_divisor()
    print("--EFETUAR SAQUE--")
    print("Entre com o ID do cliente: >",end="")
    customer_id = int(input())
    try:
        customer = fetch_customer_in_database(customer_id)
        print("Entre com a quantia a ser sacada: >",end="")
        amount = round(Decimal(input()),2)
        if (amount > 0):
            new_balance = customer.withdraw(amount)
            insert_new_transaction_in_database(customer,amount,"Saque")
            print(f"Saque efetuado! Novo saldo de {customer.name}: R$ {new_balance:.2f}")
        else:
            print("Valor inválido para saque!")
    except Exception as error:
        print("Problema em operação:",error)

def transfer():
    show_divisor()
    print("--EFETUAR TRANSFERÊNCIA--")
    print("Entre com o ID do cliente a enviar: >",end="")
    id_send = int(input())
    try:
        customer_send = fetch_customer_in_database(id_send)
        print("Entre com o ID do cliente a receber: >",end="")
        id_receive = int(input())
        if (id_send == id_receive):
            print("Não é possível transferir para a mesma conta.")
        else:
            customer_receive = fetch_customer_in_database(id_receive)
            print("Entre com a quantia a ser transferida: >",end="")
            amount = round(Decimal(input()),2)
            if (amount > 0):
                new_balance = customer_send.transfer_send(amount,customer_receive.name)
                customer_receive.transfer_receive(amount,customer_send.name)
                insert_new_transfer_in_database(customer_send,amount,customer_receive)
                print(f"Transferência efetuada! Novo saldo de {customer_send.name}: R$ {new_balance:.2f}")
            else:
                print("Valor inválido para transferência!")
    except Exception as error:
        print("Problema em operação:",error)
    return
    client_send = client_list[id_send]
    print("Entre com o ID do cliente a receber: >",end="")
    id_receive = int(input())
    client_receive = client_list[id_receive]
    if (id_send == id_receive):
        print("Não é possível transferir para a mesma conta.")
    else:
        print("Entre com a quantia a ser transferida: >",end="")
        amount = float(input())
        if (amount > 0):
            try:
                new_balance = client_send.transfer_send(amount,client_receive.name)
                client_receive.transfer_receive(amount,client_send.name)
                print(f"Transferência efetuada! Novo saldo de {client_send.name}: R$ {new_balance:.2f}")
            except ValueError as error:
                print(error)
        else:
            print("Valor inválido para transferência!")

while (option > 0):
    show_main_menu()
    option = int(input())
    if (option == 1):
        new_client()
    elif (option == 2):
        list_clients()
    elif (option == 3):
        check_balance()
    elif (option == 4):
        show_history()
    elif (option == 5):
        deposit()
    elif (option == 6):
        withdraw()
    elif (option == 7):
        transfer()