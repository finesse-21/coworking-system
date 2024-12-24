from models.request import Request
import random

class Client:
    def __init__(self, id, num_generators):
        self.id = id
        self.request_id = 0
        self.num_generators = num_generators

    def generate_requests(self, current_time):
        requests = []
        for _ in range(self.num_generators):
            self.request_id += 1
            # Генерация случайного времени обслуживания с использованием равномерного распределения
            service_time = random.uniform(0.5, 2.0)
            requests.append(Request(self.request_id, current_time, service_time, self.id))
        return requests