from datetime import datetime, timedelta

class Request:
    def __init__(self, id: int, client: 'Client', service_time: timedelta):
        self.id = id
        self.arrival_time = None
        self.service_time = service_time
        self.client = client
        self.status = "ожидание"
        self.start_time = None
        self.end_time = None

    def set_start_time(self, time: datetime):
        self.start_time = time

    def set_end_time(self, time: datetime):
        self.end_time = time