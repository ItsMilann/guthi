# pylint:disable=import-outside-toplevel wrong-import-position
import os
import datetime
import json
import django
import pika
import pytz


RABBIT_USER = os.environ.get("RABBITMQ_DEFAULT_USER", "user")
RABBIT_PASSWORD = os.environ.get("RABBITMQ_DEFAULT_PASS", "password")
RABBIT_PORT = os.environ.get("RABBITMQ_HOST_PORT", "5672")
RABBIT_HOST = os.environ.get("RABBITMQ_HOST_IP", "172.20.0.1")

_TZ = pytz.timezone("Asia/Kathmandu")


def sync_data(
    channel_: pika.BlockingConnection,
    method: pika.DeliveryMode,
    properties: pika.BasicProperties,
    body: bytes,
):
    from consumers.constants import EventHandlersMapper

    timestamp = datetime.datetime.now(tz=_TZ).strftime("%Y-%m-%d %H:%M:%S")
    data = json.loads(body)
    func = EventHandlersMapper.get(properties.content_type)
    if func:
        print(f"[INFO: {timestamp}]", "trigger func: ", func.__name__)
        object_ = func(data)
        print(f"[INFO: {timestamp}]", "received action: ", properties.content_type)
        print(f"[INFO: {timestamp}]", "altered object: ", object_)


def main():
    timestamp = datetime.datetime.now(tz=_TZ).strftime("%Y-%m-%d %H:%M:%S")
    credentials = pika.PlainCredentials(username=RABBIT_USER, password=RABBIT_PASSWORD)
    params = pika.ConnectionParameters(
        host=RABBIT_HOST,
        port=RABBIT_PORT,
        credentials=credentials,
        blocked_connection_timeout=300,
        heartbeat=30,
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(exchange="patrachar", exchange_type="fanout")
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange="patrachar", queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=sync_data, auto_ack=True)
    print(f"[INFO: {timestamp}]", " [*] Waiting for logs. To exit press CTRL+C")
    channel.start_consuming()
    channel.close()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.development")
    django.setup()
    from django.conf import settings

    if settings.FEATURES.get("SYNC_WITH_AUTH_SERVICE"):
        main()
