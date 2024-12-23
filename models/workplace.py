from datetime import datetime

class Workplace:
    def __init__(self, id):
        self.id = id
        self.is_busy = False
        self.current_request = None

    def start_service(self, request):
        self.is_busy = True
        self.current_request = request

    def end_service(self):
        self.is_busy = False
        self.current_request.set_end_time(datetime.now())
        self.current_request = None