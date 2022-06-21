import asyncio
import logging
import pika
from json import loads
from pika.exchange_type import ExchangeType
from threading import Timer
from .models import SensorData, SensorError


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


async def startapp(channel):
    timer = Timer(5, channel.stop_consuming)
    timer.start()
    channel.start_consuming()


def on_message(chan, method_frame, header_frame, body, userdata=None):
    """Called when a message is received. Log message and ack it."""
    # LOGGER.info('Delivery properties: %s, message metadata: %s', method_frame, header_frame)
    # LOGGER.info('Userdata: %s, message body: %s', userdata, body)

    # json представление
    input_info = loads(str(body.decode('utf-8')).replace(',', ',').replace('AiMean:', 'AiMean\":'))
    # обработка времени
    dt, tm = input_info['Date'].split()
    temp = ' '.join(['-'.join(str(dt).split('.')[::-1]), tm])
    # создание объекта данных датчика
    new_data = SensorData.objects.create(id_sensor=input_info['Sensor'], date=temp, mode=input_info['SysMode'],
                                         ai_max=input_info['AiMax'], ai_min=input_info['AiMin'],
                                         ai_mean=input_info['AiMean'], stat_min=input_info['StMin'],
                                         stat_max=input_info['StMax'], ml_min=input_info['MlMin'],
                                         ml_max=input_info['MlMax'], status=input_info['Sts'])
    # подключение журнала ошибок
    previous_data = SensorData.objects.all().last()
    error = input_info['Err']
    if error != 0 and previous_data.id_error_log.error == error:
        new_data.id_error_log = previous_data.id_error_log
    elif error != 0:
        new_journal = SensorError.objects.create(id_sensor=new_data.id_sensor, error=error, error_start_date=temp)
        new_journal.save()
        new_data.id_error_log = new_journal.id
    elif previous_data.id_error_log is not None:
        previous_data.id_error_log.error_end_date = previous_data.date
    new_data.save()
    # подтверждаем прочитанную очередь
    chan.basic_ack(delivery_tag=method_frame.delivery_tag)


async def main():
    """Main method."""
    parameters = pika.URLParameters('amqp://user:atlasrabbit@77.222.54.167:5672/%2F?FirstStep')
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(
        exchange='test_exchange',
        exchange_type=ExchangeType.direct,
        passive=False,
        durable=True,
        auto_delete=False)
    # channel.queue_declare(queue='FirstStep', auto_delete=False)
    channel.queue_bind(queue='FirstStep', exchange='test_exchange', routing_key='standard_key')
    channel.basic_qos(prefetch_count=4)
    channel.basic_consume('FirstStep', on_message_callback=on_message)
    await startapp(channel)
    connection.close()


if __name__ == '__main__':
    asyncio.run(main())
