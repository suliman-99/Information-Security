import pika
from cryptography.fernet import Fernet


def encrypt(message: str, key: str) -> str:
    key = key.encode()
    message = message.encode()
    fernet = Fernet(key)
    message = fernet.encrypt(message)
    return message


def send(data, queue, ip='localhost'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=data
    )

    connection.close()


if __name__ == '__main__':
    key = 'L4eZ-2YU3g1yetyaCuv1Y7QQ1OoKL4J9flRYAYp-OH0='
    message = 'Important Sensitive Data'
    message = encrypt(message, key)
    queue = 'q1'
    send(message, queue)

