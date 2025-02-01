import pymysql
import os
import logging

# Configurações de conexão com o MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DB = os.getenv("MYSQL_DB", "users_db")

logging.basicConfig(filename='app/logs/app.log', level=logging.INFO)

def save_to_mysql(data):
    connection = None
    try:
        # Conexão com o MySQL
        logging.info(f"Conectando ao MySQL: {MYSQL_HOST}...")  # Log de tentativa de conexão
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DB
        )

        with connection.cursor() as cursor:
            for user in data:
                logging.info(f"Iniciando inserção do usuário: {user}")  # Log de cada usuário
                try:
                    query = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
                    cursor.execute(query, (user['name'], user['email'], user['age']))
                    logging.info(f"Usuário inserido: {user['name']}")  # Log do sucesso da inserção
                except Exception as e:
                    logging.error(f"Erro ao inserir usuário {user['name']}: {e}")
                    continue  # Em caso de erro, continuar com o próximo usuário

            # Commit da transação
            connection.commit()
            logging.info("Todos os dados foram inseridos no MySQL com sucesso!")

    except Exception as e:
        logging.error(f"Erro ao conectar ou salvar dados no MySQL: {e}")
    finally:
        # Fechar a conexão
        if connection:
            connection.close()
            logging.info("Conexão com o MySQL fechada.")
