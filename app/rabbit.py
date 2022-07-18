import logging
import pika
from json import loads
from asyncio import sleep
from requests.api import post
from website import settings
from datetime import datetime


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def on_message(chan, method_frame, header_frame, body):
    """Called when a message is received. Log message and ack it."""
    # LOGGER.info('Delivery properties: %s, message metadata: %s', method_frame, header_frame)
    # LOGGER.info('Userdata: %s, message body: %s', userdata, body)

    # json представление
    context = loads(str(body.decode('utf-8')))
    # обработка времени
    dt, tm, utc = context['date'].split()
    temp = datetime.strptime(dt + ' ' + tm, '%d.%m.%Y %H:%M:%S')
    context['csrf'] = 'a very secret key'
    context['date'] = temp.isoformat()
    response = post(url=settings.DJANGO_RESPONSE_URL, data=context)
    LOGGER.info('Response status: {}, data: {}'.format(response.status_code, response.json()['']))
    LOGGER.info(str(body.decode('utf-8')))
    chan.basic_ack(delivery_tag=method_frame.delivery_tag)


def main():
    """Main method."""
    sleep(10)
    parameters = pika.URLParameters(settings.RABBIT_REQUEST_URL)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(
        exchange=settings.RABBIT_EXCHANGE,
        exchange_type='direct',  # ExchangeType.direct
        passive=False,
        durable=True,
        auto_delete=False)
    channel.queue_bind(queue=settings.RABBIT_QUEUE, exchange=settings.RABBIT_EXCHANGE, routing_key='standard_key')
    channel.basic_consume(settings.RABBIT_QUEUE, on_message_callback=on_message)
    try:
        channel.start_consuming()
        return 1
    except KeyboardInterrupt:
        connection.close()
        return 0


if __name__ == '__main__':
    main()
