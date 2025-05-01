import datetime
class Customer:
    def __init__(self,name,balance=0,id=-1):
        self.name = name
        self.balance = balance
        self.id = id
        self.history = []
    
    def __str__(self):
        return self.name
    
    def deposit(self,amount):
        self.balance += amount
        self.history.append(["Depósito",amount,self.balance,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        return self.balance
    
    def withdraw(self,amount):
        if (amount > self.balance):
            raise ValueError("Não há saldo suficiente para efetuar o saque.")
        self.balance -= amount
        self.history.append(["Saque",amount,self.balance,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        return self.balance
    
    def transfer_send(self,amount,name):
        if (amount > self.balance):
            raise ValueError("Não há saldo suficiente para efetuar a transferência.")
        self.balance -= amount
        self.history.append([f"Transferência enviada para {name}",amount,self.balance,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        return self.balance
    
    def transfer_receive(self,amount,name):
        self.balance += amount
        self.history.append([f"Transferência recebida de {name}",amount,self.balance,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        return self.balance