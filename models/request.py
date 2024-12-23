class Request:
    def __init__(self, id, arrival_time, service_time, client):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.client = client
        self.start_time = None
        self.end_time = None
        self.status = "Created"

    def set_start_time(self, time):
        self.start_time = time
        self.status = "In Progress"

    def set_end_time(self, time):
        self.end_time = time
        self.status = "Completed"