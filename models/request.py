class Request:
    def __init__(self, id, arrival_time, service_time, client):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.client = client
        self.start_time = None
        self.end_time = None
        self.status = "ожидает"
        self.buffer_snapshot = []

    def set_start_time(self, time):
        self.start_time = time
        self.status = "в обработке"

    def set_end_time(self, time):
        self.end_time = time
        self.status = "завершен"

    def add_to_buffer_snapshot(self, buffer_size):
        self.buffer_snapshot.append(buffer_size)