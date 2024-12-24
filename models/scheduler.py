# models/scheduler.py
from models.buffer import Buffer
from models.workplace import Workplace

class Scheduler:
    def __init__(self, buffer_size, num_workplaces):
        self.buffer = Buffer(buffer_size)
        self.workplaces = [Workplace(i + 1) for i in range(num_workplaces)]
        self.next_workplace_index = 0

    def add_request_to_buffer(self, request):
        return self.buffer.add_request(request)

    def assign_workplace(self, request):
        for _ in range(len(self.workplaces)):
            workplace = self.workplaces[self.next_workplace_index]
            self.next_workplace_index = (self.next_workplace_index + 1) % len(self.workplaces)
            if not workplace.is_busy:
                workplace.start_service(request)
                return workplace.id
        return None