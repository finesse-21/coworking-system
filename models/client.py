from models.request import Request
import random

class Client:
    def __init__(self, id, num_generators):
        self.id = id
        self.request_id = 0
        self.num_generators = num_generators
        self.requests = []

    def generate_requests(self, current_time):
        requests = []
        for generator_id in range(self.num_generators):
            self.request_id += 1
            service_time = random.uniform(0.5, 2.0)
            requests.append(Request(self.request_id, current_time, service_time, generator_id))
        return requests