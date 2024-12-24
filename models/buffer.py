class Buffer:
    def __init__(self, size):
        self.size = size
        self.requests = []

    def add_request(self, request):
        if self.is_full():
            rejected_request = self.requests.pop(0)  # Remove the oldest request
            self.requests.append(request)
            return rejected_request
        else:
            self.requests.append(request)
            return None

    def remove_request(self):
        if not self.is_empty():
            return self.requests.pop()  # LIFO principle
        return None

    def is_empty(self):
        return len(self.requests) == 0

    def is_full(self):
        return len(self.requests) >= self.size

    def get_size(self):
        return len(self.requests)