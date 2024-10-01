# db.py
import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            user='root',
            password='9119',
            database='edu_blog'
        )
        print("Connected to the database")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
