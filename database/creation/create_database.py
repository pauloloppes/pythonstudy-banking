from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user="bankingapp",
        password="123456",
        #IMPORTANT NOTE
        #I'm leaving the credentials up on these files to simplify work only because I made a generic account to run locally anyway.
        #I know how it is important to hide credentials, and I used environment variables before when I worked in professional settings.
    ) as connection:
        create_db_query = "CREATE DATABASE banking"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
            print("Database 'bankingapp' created.")
except Error as e:
    print(e)