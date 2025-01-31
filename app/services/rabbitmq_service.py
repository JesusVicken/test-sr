import pika
import json
import logging

logging.basicConfig(filename='app/logs/app.log', level=logging.INFO)

def send_to_rabbitmq(mongo_id):
    """ Envia o ID do MongoDB para a fila RabbitMQ """
    try:
        credentials = pika.PlainCredentials('user', 'password')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq', credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue='user_data', durable=True)  # Garantir persistência da fila

        # Formata a mensagem JSON
        message = json.dumps({"mongo_id": str(mongo_id)})

        # Publica a mensagem
        channel.basic_publish(
            exchange='',
            routing_key='user_data',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # Mensagem persistente
            )
        )

        logging.info(f"✅ Mensagem enviada ao RabbitMQ: {message}")
        connection.close()

    except Exception as e:
        logging.error(f"❌ Erro ao enviar mensagem para RabbitMQ: {str(e)}")
