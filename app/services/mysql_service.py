from dotenv import load_dotenv
import pymysql
import os

# Carrega as variáveis de ambiente do arquivo .env, se existir
load_dotenv()

# Configurações de conexão com o MySQL usando o usuário root
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DB = os.getenv("MYSQL_DB", "users_db")

def save_to_mysql(data):
    try:
        # Conexão com o MySQL
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DB
        )
        with connection.cursor() as cursor:
            # Inserção de dados na tabela users
            for user in data:
                query = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
                cursor.execute(query, (user['name'], user['email'], user['age']))
            # Commit da transação
            connection.commit()
        print("Dados inseridos no MySQL com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar dados no MySQL: {e}")
    finally:
        connection.close()
