import pika
from cryptography.fernet import Fernet


def decrypt(message: str, key: str) -> str:
    key = key.encode()
    fernet = Fernet(key)
    message = fernet.decrypt(message)
    message = message.decode()
    return message


def process_message(ch, method, propertiescd , message, key):
    message = decrypt(message, key)
    GREEN_COLOR = "\033[32m"
    WHITE_COLOR = "\033[0m"
    print('\n Message Received: ( ' + GREEN_COLOR + message + WHITE_COLOR + ' ) \n')


def run_listner(function, queue, key, ip='localhost'):
    print('Run Listner ...')
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(
        queue=queue,
        auto_ack=True,
        on_message_callback=lambda ch, method, properties, body: function(ch, method, properties, body, key)
    )
    channel.start_consuming()


if __name__ == '__main__':
    key = 'L4eZ-2YU3g1yetyaCuv1Y7QQ1OoKL4J9flRYAYp-OH0='
    queue = 'q1'
    function = process_message
    run_listner(function, 'q1', key)

