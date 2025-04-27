from entities.Customer import Customer
from database import insert_new_customer_in_database
from database import fetch_customer_in_database
from database import fetch_all_customers_in_database

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
    insert_new_customer_in_database(name)

def list_clients():
    show_divisor()
    print("--LISTA DE CLIENTES--")
    print("ID / Nome")
    try:
        client_list = fetch_all_customers_in_database()
        for i in client_list:
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
    client_id = int(input())
    client = client_list[client_id]
    for i in client.history[::-1]:
        print(f"{i[0]}: R$ {i[1]:.2f}, Saldo resultante R$ {i[2]:.2f}. Data/hora: {i[3]}")

def deposit():
    show_divisor()
    print("--EFETUAR DEPÓSITO--")
    print("Entre com o ID do cliente: >",end="")
    client_id = int(input())
    client = client_list[client_id]
    print("Entre com a quantia a ser depositada: >",end="")
    amount = float(input())
    if (amount > 0):
        new_balance = client.deposit(amount)
        print(f"Depósito efetuado! Novo saldo de {client.name}: R$ {new_balance:.2f}")
    else:
        print("Valor inválido para depósito!")

def withdraw():
    show_divisor()
    print("--EFETUAR SAQUE--")
    print("Entre com o ID do cliente: >",end="")
    client_id = int(input())
    client = client_list[client_id]
    print("Entre com a quantia a ser sacada: >",end="")
    amount = float(input())
    if (amount > 0):
        try:
            new_balance = client.withdraw(amount)
            print(f"Saque efetuado! Novo saldo de {client.name}: R$ {new_balance:.2f}")
        except ValueError as error:
            print(error)
    else:
        print("Valor inválido para saque!")

def transfer():
    show_divisor()
    print("--EFETUAR TRANSFERÊNCIA--")
    print("Entre com o ID do cliente a enviar: >",end="")
    id_send = int(input())
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