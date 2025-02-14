from models.request import Request

class Buffer:
    def __init__(self, size: int):
        self.size = size
        self.requests = [None] * size
        self.head = 0
        self.tail = 0
        self.count = 0

    def add_request(self, request: Request) -> Request:
        removed_request = None
        if self.is_full():
            removed_request = self.requests[self.head]
            self.head = (self.head + 1) % self.size
            self.count -= 1
        self.requests[self.tail] = request
        self.tail = (self.tail + 1) % self.size
        self.count += 1
        return removed_request

    def remove_request(self) -> Request:
        if self.is_empty():
            return None
        self.tail = (self.tail - 1) % self.size
        request = self.requests[self.tail]
        self.requests[self.tail] = None
        self.count -= 1
        return request

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.size