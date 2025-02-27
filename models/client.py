from models.request import Request
import random
from datetime import timedelta
import numpy as np

class Client:
    def __init__(self, id: int):
        self.id = id
        self.total_system_time = timedelta()
        self.processed_requests = 0
        self.generated_requests = 0
        self.service_times = []
        self.requests = []

    def generate_request(self, request_counter: int) -> Request:
        service_time = timedelta(seconds=random.expovariate(0.5))
        request = Request(id=request_counter, client=self, service_time=service_time)
        self.generated_requests += 1
        self.requests.append(request)
        return request

    def add_system_time(self, system_time: timedelta):
        self.total_system_time += system_time
        self.processed_requests += 1

    def average_system_time(self) -> float:
        if self.processed_requests > 0:
            return self.total_system_time.total_seconds() / self.processed_requests
        return 0.0

    def add_service_time(self, service_time: timedelta):
        self.service_times.append(service_time.total_seconds())

    def average_service_time(self) -> float:
        if len(self.service_times) > 0:
            return np.mean(self.service_times)
        return 0.0

    def service_time_variance(self) -> float:
        if len(self.service_times) > 1:
            return np.var(self.service_times, ddof=1)
        return 0.0