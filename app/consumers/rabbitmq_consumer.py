import pika
import json
import os
from bson import ObjectId
from app.services.mongo_service import collection
from app.services.mysql_service import save_to_mysql
import logging

# Configurações do RabbitMQ diretamente no código
RABBITMQ_HOST = "rabbitmq"  # ou o valor que você desejar
RABBITMQ_QUEUE = "user_data"
RABBITMQ_USER = "root"
RABBITMQ_PASSWORD = "root"

logging.basicConfig(filename='app/logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        mongo_id = message.get('mongo_id')

        if not mongo_id:
            logging.error("Mensagem sem mongo_id recebida.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        logging.info(f"Processando mensagem com mongo_id: {mongo_id}")

        # Busca os dados no MongoDB
        data = collection.find_one({"_id": ObjectId(mongo_id)})
        if not data:
            logging.error(f"Dados não encontrados para o MongoDB ID: {mongo_id}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        # Salva os dados no MySQL
        save_to_mysql(data['data'])
        logging.info(f"Dados salvos no MySQL com sucesso: {mongo_id}")

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Erro ao processar mensagem: {e}", exc_info=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def start_consumer():
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        logging.info("Aguardando mensagens...")
        channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=process_message)
        channel.start_consuming()
    except Exception as e:
        logging.critical(f"Erro ao conectar com RabbitMQ: {e}", exc_info=True)

if __name__ == "__main__":
    start_consumer()
