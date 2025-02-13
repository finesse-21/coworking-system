from datetime import datetime
from typing import List
from models.buffer import Buffer
from models.request import Request
from models.workplace import Workplace

class Scheduler:
    def __init__(self, buffer: Buffer, workplaces: List[Workplace]):
        self.buffer = buffer
        self.workplaces = workplaces

    def add_request_to_buffer(self, request: Request):
        return self.buffer.add_request(request)

    def get_next_request(self) -> Request:
        return self.buffer.remove_request()

    def assign_workplace(self, request: Request, current_time: datetime):
        for workplace in self.workplaces:
            if not workplace.is_busy:
                workplace.start_service(request, current_time)
                return True
        return False