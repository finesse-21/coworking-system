class Buffer:
    def __init__(self, size):
        self.size = size
        self.requests = []

    def add_request(self, request):
        if len(self.requests) < self.size:
            self.requests.append(request)
        else:
            raise OverflowError("Buffer is full")

    def remove_request(self):
        if self.requests:
            return self.requests.pop(0)
        return None

    def is_full(self):
        return len(self.requests) >= self.size

    def is_empty(self):
        return len(self.requests) == 0

    def get_requests_by_source(self, source_id):
        return [req for req in self.requests if req.client.id == source_id]

    def clear_requests_by_source(self, source_id):
        self.requests = [req for req in self.requests if req.client.id != source_id]