from models.request import Request
import random
from datetime import timedelta

class Client:
    def __init__(self, id: int):
        self.id = id
        self.total_system_time = timedelta()
        self.processed_requests = 0
        self.generated_requests = 0

    def generate_request(self, request_counter: int) -> Request:
        service_time = timedelta(seconds=random.expovariate(0.5))
        request = Request(id=request_counter, client=self, service_time=service_time)
        self.generated_requests += 1
        return request

    def add_system_time(self, system_time: timedelta):
        self.total_system_time += system_time
        self.processed_requests += 1

    def average_system_time(self) -> float:
        if self.processed_requests > 0:
            return self.total_system_time.total_seconds() / self.processed_requests
        return 0.0