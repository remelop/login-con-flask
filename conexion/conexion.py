import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # cambia si tienes clave
        database="desarrollo_web"
    )
    return connection
