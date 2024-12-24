from datetime import datetime, timedelta

class Workplace:
    def __init__(self, id):
        self.id = id
        self.is_busy = False
        self.current_request = None
        self.service_end_time = None

    def start_service(self, request):
        self.current_request = request
        self.is_busy = True
        self.service_end_time = datetime.now() + timedelta(seconds=request.service_time)
        request.set_start_time(datetime.now())

    def end_service(self):
        if self.is_busy and datetime.now() >= self.service_end_time:
            self.is_busy = False
            self.current_request.set_end_time(datetime.now())
            completed_request = self.current_request
            self.current_request = None
            return completed_request
        return None