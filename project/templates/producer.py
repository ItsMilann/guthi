import os
import enum
import json
import pika


class ServiceNames(enum.Enum):
    PATRACHAR = "darta_to_patrachar"
    DARTA = "patrachar_to_darta"
    COMMON = "patrachar"


class EventTypes(enum.Enum):
    REQUEST_DARTA = "request_darta"
    REQUEST_CHALANI = "request_chalani"


class Publisher:
    def __init__(self) -> None:
        USER = os.environ.get("RABBITMQ_DEFAULT_USER", "user")
        PASSWORD = os.environ.get("RABBITMQ_DEFAULT_PASS", "password")
        PORT = os.environ.get("RABBITMQ_HOST_PORT", "5672")
        HOST = os.environ.get("RABBITMQ_HOST_IP", "172.20.0.10")
        credentials = pika.PlainCredentials(username=USER, password=PASSWORD)
        params = pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange="patrachar", exchange_type="fanout")

    def publish(self, action: str, service_name: str, body: dict):
        """ write to stream """
        properties = pika.BasicProperties(action)
        data = json.dumps(body)
        self.channel.basic_publish(
            exchange="patrachar",
            routing_key=service_name,
            body=data,
            properties=properties,
        )
