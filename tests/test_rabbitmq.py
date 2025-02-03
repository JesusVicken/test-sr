import pytest
import pika
import json
from app.services.rabbitmq_service import send_to_rabbitmq

@pytest.fixture
def rabbitmq_connection():
    credentials = pika.PlainCredentials("root", "root")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", credentials=credentials))
    yield connection
    connection.close()

def test_send_to_rabbitmq(rabbitmq_connection):
    send_to_rabbitmq("test_mongo_id")

    channel = rabbitmq_connection.channel()
    method_frame, header_frame, body = channel.basic_get(queue="user_data")

    assert body is not None
    message = json.loads(body)
    assert message["mongo_id"] == "test_mongo_id"
