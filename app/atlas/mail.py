from django.core.mail import mail_admins
import datetime


def on_error(sensor_data):
    """
    Функция вызываемая при получении ошибки из поступающих данных
    """
    # sensor_data = sensor_data  # type: SensorData
    if not sensor_data.id_error_log.objects.last().error_start_date + datetime.timedelta(hours=1) > sensor_data.date:
        mail_theme = f'Ошибка датчика {sensor_data.id_sensor.name}'
        mail_body = f'Ошибка датчика:  {sensor_data.id_sensor.name}\n' \
                    f'Код ошибки: {sensor_data.id_error_log.error}\n' \
                    f'Дата обработки сигнала: {sensor_data.date}\n'
        mail_admins(mail_theme, mail_body)
