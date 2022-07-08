from .mail import on_warning_last_data_upd
import threading


class SensorDataWarning:
    timer = None

    def sensor_data_warning(self, sender, **kwargs):
        if self.timer is not None:
            self.timer.cancel()
        self.timer = threading.Timer(3600, on_warning_last_data_upd(kwargs['date']))
        self.timer.start()
