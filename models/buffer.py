from models.request import Request

class Buffer:
    def __init__(self, size: int):
        self.size = size
        self.requests = []

    def add_request(self, request: Request):
        if self.is_full():
            removed_request = self.requests.pop(0)
            return removed_request
        self.requests.append(request)
        return None

    def remove_request(self) -> Request:
        if not self.is_empty():
            return self.requests.pop()
        return None

    def is_empty(self) -> bool:
        return len(self.requests) == 0

    def is_full(self) -> bool:
        return len(self.requests) >= self.size