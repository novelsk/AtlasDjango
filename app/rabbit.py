import logging
import pika
import pytz
from json import loads
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

    context = loads(str(body.decode('utf-8')))
    dt, tm = context['date'].split()
    date = datetime.strptime(dt + ' ' + tm, '%d.%m.%Y %H:%M:%S')
    tz = pytz.timezone(context['tzinfo'])
    context['date'] = date.astimezone(tz).isoformat()
    context['csrf'] = 'a very secret key'
    print(context)
    response = post(url=settings.DJANGO_RESPONSE_URL, data=context)
    LOGGER.info('Response status: {}, data: {}'.format(response.status_code, response.json()['']))
    chan.basic_ack(delivery_tag=method_frame.delivery_tag)


def main():
    """Main method."""
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
    except KeyboardInterrupt:
        connection.close()
    except Exception:
        main()


if __name__ == '__main__':
    main()
