from datetime import datetime, timedelta
from models.request import Request

class Workplace:
    def __init__(self, id: int):
        self.id = id
        self.is_busy = False
        self.current_request = None
        self.total_busy_time = timedelta()
        self.last_busy_start_time = None

    def start_service(self, request: Request, current_time: datetime):
        self.is_busy = True
        self.current_request = request
        request.set_start_time(current_time)
        request.status = "в обработке"
        self.last_busy_start_time = current_time

    def end_service(self, current_time: datetime):
        if self.current_request:
            request = self.current_request
            request.set_end_time(current_time)
            request.status = "завершен"
            self.is_busy = False
            self.total_busy_time += current_time - self.last_busy_start_time
            request.client.add_system_time(request.end_time - request.arrival_time)
            request.client.add_service_time(request.service_time)
            self.current_request = None
            self.last_busy_start_time = None
