from datetime import datetime
from models.request import Request

class Client:
    def __init__(self, id):
        self.id = id

    def generate_request(self):
        return Request(
            id=datetime.now().microsecond,
            arrival_time=datetime.now(),
            service_time=2.0,  # Примерное время обработки
            client=self
        )