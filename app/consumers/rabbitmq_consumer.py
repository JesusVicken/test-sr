
import pika
import json
import os
import time
from bson import ObjectId
from app.services.mongo_service import collection
from app.services.mysql_service import save_to_mysql
import logging

# Configuração do logger
logging.basicConfig(
    filename='app/logs/app.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configurações do RabbitMQ via variáveis de ambiente
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_data")

def process_message(ch, method, properties, body):
    """Processa cada mensagem da fila."""
    try:
        message = json.loads(body)
        mongo_id = message.get('mongo_id')

        if not mongo_id:
            logging.error("Mensagem sem mongo_id recebida. Descartando...")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # Não reenvia
            return

        logging.info(f"Processando mensagem com mongo_id: {mongo_id}")

        # Busca os dados no MongoDB
        data = collection.find_one({"_id": ObjectId(mongo_id)})
        if not data:
            logging.error(f"Dados não encontrados para o MongoDB ID: {mongo_id}. Descartando...")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # Evita loop infinito
            return

        # Processa os dados e salva no MySQL
        for user in data.get('data', []):  # Usa `.get()` para evitar erro se 'data' não existir
            save_to_mysql(user)
            logging.info(f"Dados salvos no MySQL com sucesso: {user.get('name', 'Desconhecido')}")

        # Confirma o processamento da mensagem
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.error(f"Erro ao processar mensagem: {e}", exc_info=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def connect_to_rabbitmq():
    """Tenta conectar ao RabbitMQ com reconexão automática."""
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                heartbeat=600,  # Mantém a conexão ativa
                blocked_connection_timeout=300  # Tempo de espera para conexão bloqueada
            ))
            channel = connection.channel()
            channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
            return connection, channel
        except pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Falha na conexão com RabbitMQ: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)

def start_consumer():
    """Inicia o consumidor e garante que ele permaneça rodando."""
    while True:
        try:
            connection, channel = connect_to_rabbitmq()
            logging.info("Aguardando mensagens...")

            channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=process_message)

            # Mantém o consumidor ativo
            channel.start_consuming()

        except KeyboardInterrupt:
            logging.info("Consumidor encerrado manualmente.")
            break  # Permite encerrar com Ctrl+C

        except Exception as e:
            logging.critical(f"Erro no consumidor: {e}", exc_info=True)
            logging.info("Reiniciando o consumidor em 5 segundos...")
            time.sleep(5)  # Aguarda um tempo antes de tentar novamente

if __name__ == "__main__":
    start_consumer()
