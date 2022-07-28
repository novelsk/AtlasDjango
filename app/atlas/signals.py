from .mail import on_warning_last_data_upd
import threading
from datetime import datetime


class SensorDataSignals:
    def __init__(self):
        self.date = datetime.now()
        self.timer = threading.Timer(10, on_warning_last_data_upd(datetime.now()))

    def time_warning(self, sender, **kwargs):
        if self.timer is not None:
            self.timer.cancel()
        self.date = datetime.now()
        self.timer = threading.Timer(10, on_warning_last_data_upd(self.date))
        self.timer.start()
