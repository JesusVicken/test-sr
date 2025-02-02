import pika
import json
import os
import logging

logging.basicConfig(filename='app/logs/app.log', level=logging.INFO)

def send_to_rabbitmq(mongo_id):
    try:
        # Obtém as variáveis de ambiente (se desejar, você pode também usar load_dotenv aqui)
        RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
        RABBITMQ_USER = os.getenv("RABBITMQ_USER", "root")
        RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "root")
        RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_data")
        
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        message = json.dumps({"mongo_id": str(mongo_id)})
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # Mensagem persistente
            )
        )
        logging.info(f"✅ Mensagem enviada ao RabbitMQ: {message}")
        connection.close()
    except Exception as e:
        logging.error(f"❌ Erro ao enviar mensagem para RabbitMQ: {e}")
