import pytest
import pymysql
from app.services.mysql_service import save_to_mysql

MYSQL_CONFIG = {
    "host": "mysql",
    "user": "root",
    "password": "root",
    "db": "users_db"
}

@pytest.fixture
def mysql_connection():
    connection = pymysql.connect(**MYSQL_CONFIG)
    yield connection
    connection.close()

def test_save_to_mysql(mysql_connection):
    data = [{"name": "Teste", "email": "teste@email.com", "age": 30}]
    save_to_mysql(data)

    with mysql_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = 'teste@email.com'")
        result = cursor.fetchone()
    
    assert result is not None
