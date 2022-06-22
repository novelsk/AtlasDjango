import logging
import pika
from json import loads
from pika.exchange_type import ExchangeType
from asyncio import sleep
from requests.api import post


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def on_message(chan, method_frame, header_frame, body):
    """Called when a message is received. Log message and ack it."""
    # LOGGER.info('Delivery properties: %s, message metadata: %s', method_frame, header_frame)
    # LOGGER.info('Userdata: %s, message body: %s', userdata, body)

    # json представление
    input_info = loads(str(body.decode('utf-8')).replace(',', ',').replace('AiMean:', 'AiMean\":'))
    # обработка времени
    dt, tm = input_info['Date'].split()
    temp = ' '.join(['-'.join(str(dt).split('.')[::-1]), tm])
    response_data = {
        'csrf': 'a very secret key',
        'id_object': input_info['Object'],
        'id_sensor': input_info['Sensor'],
        'date': temp,
        'mode': input_info['SysMode'],
        'ai_max': input_info['AiMax'],
        'ai_min': input_info['AiMin'],
        'ai_mean': input_info['AiMean'],
        'stat_min': input_info['StMin'],
        'stat_max': input_info['StMax'],
        'ml_min': input_info['MlMin'],
        'ml_max': input_info['MlMax'],
        'status': input_info['Sts'],
        'error': input_info['Err']
    }
    response = post(url='http://localhost:8000/rabbit_data', data=response_data)
    LOGGER.info('Response status: {}, data: {}'.format(response.status_code, response.json()['']))
    chan.basic_ack(delivery_tag=method_frame.delivery_tag)


def main():
    """Main method."""
    sleep(10)
    parameters = pika.URLParameters('amqp://user:atlasrabbit@77.222.54.167:5672/%2F?FirstStep')
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(
        exchange='test_exchange',
        exchange_type=ExchangeType.direct,
        passive=False,
        durable=True,
        auto_delete=False)
    channel.queue_bind(queue='FirstStep', exchange='test_exchange', routing_key='standard_key')
    channel.basic_consume('FirstStep', on_message_callback=on_message)
    try:
        channel.start_consuming()
    finally:
        connection.close()
        main()


if __name__ == '__main__':
    main()
