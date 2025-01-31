import mysql.connector
import os

def save_to_mysql(data):
    connection = mysql.connector.connect(
        host="mysql",
        user="user",
        password="password",
        database="users_db"
    )
    cursor = connection.cursor()
    for user in data:
        cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
                       (user['name'], user['email'], user['age']))
    connection.commit()
    cursor.close()
    connection.close()