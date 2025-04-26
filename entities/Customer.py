import datetime
class Customer:
    def __init__(self,name):
        self.name = name
        self.balance = 0
        self.history = []
    
    def __str__(self):
        return self.name
    
    def deposit(self,amount):
        self.balance += amount
        self.history.append(["Depósito",amount,self.balance,str(datetime.datetime.now())])
        return self.balance
    
    def withdraw(self,amount):
        if (amount <= self.balance):
            self.balance -= amount
            self.history.append(["Saque",amount,self.balance,str(datetime.datetime.now())])
            return self.balance
        else:
            return -1
    
    def transfer_send(self,amount,name):
        if (amount <= self.balance):
            self.balance -= amount
            self.history.append([f"Transferência enviada para {name}",amount,self.balance,str(datetime.datetime.now())])
            return self.balance
        else:
            return -1
    
    def transfer_receive(self,amount,name):
        self.balance += amount
        self.history.append([f"Transferência recebida de {name}",amount,self.balance,str(datetime.datetime.now())])
        return self.balance