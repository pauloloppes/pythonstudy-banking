from mysql.connector import connect, Error

def create_customers_table():
    return """
            CREATE TABLE customers(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                balance DECIMAL(19,4),
                creation_date DATETIME DEFAULT(now()),
                modification_date DATETIME
            )
            """

def create_transactions_table():
    return """
            CREATE TABLE transactions(
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                sent_customer_id INT,
                description VARCHAR(200),
                amount DECIMAL(19,4),
                balance DECIMAL(19,4),
                creation_date DATETIME DEFAULT(now()),
                FOREIGN KEY(customer_id) REFERENCES customers(id),
                FOREIGN KEY(sent_customer_id) REFERENCES customers(id)
            )
            """

def create_update_trigger():
    return """
            CREATE TRIGGER banking.update_date
            BEFORE UPDATE ON banking.customers
            FOR EACH ROW
            BEGIN
                    SET new.modification_date=now();
            END
            """

try:
    with connect(
        host="localhost",
        user="bankingapp",
        password="123456",
        database="banking",
        #IMPORTANT NOTE
        #I'm leaving the credentials up on these files to simplify work only because I made a generic account to run locally anyway.
        #I know how it is important to hide credentials, and I used environment variables before when I worked in professional settings.
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(create_customers_table())
            cursor.execute(create_transactions_table())
            cursor.execute(create_update_trigger())
            connection.commit()
            print("Finished execution.")
except Error as e:
    print(e)
