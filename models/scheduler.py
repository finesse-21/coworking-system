from datetime import datetime
import matplotlib.pyplot as plt

class Scheduler:
    def __init__(self, buffer, workplaces):
        self.buffer = buffer
        self.workplaces = workplaces
        self.event_log = []
        self.rejection_count = 0
        self.total_requests = 0

    def process_step(self, request):
        self.total_requests += 1
        if not self.buffer.is_full():
            self.add_request_to_buffer(request)
        else:
            self.rejection_count += 1
            self.log_event("Request rejected: Buffer full", request)

        self.assign_workplace()

    def add_request_to_buffer(self, request):
        self.buffer.add_request(request)
        self.log_event("Request added to buffer", request)

    def assign_workplace(self):
        for workplace in self.workplaces:
            if not workplace.is_busy:
                request = self.buffer.remove_request()
                if request:
                    request.set_start_time(datetime.now())
                    workplace.start_service(request)
                    self.log_event(
                        f"Request {request.id} started at Workplace {workplace.id}", request
                    )

    def log_event(self, description, request):
        self.event_log.append({
            "time": datetime.now(),
            "event": description,
            "request_id": request.id,
        })

    def display_state(self):
        print("\nТекущее состояние:")
        print(f"Буфер: {len(self.buffer.requests)}/{self.buffer.size}")
        print("Рабочие места:")
        for workplace in self.workplaces:
            status = "Занято" if workplace.is_busy else "Свободно"
            print(f"  Рабочее место {workplace.id}: {status}")
        print(f"Процент отказов: {self.rejection_count / self.total_requests * 100:.2f}%")
        print("\nКалендарь событий:")
        print(f"{'Время':<20}{'Событие':<30}{'ID заявки':<10}")
        for event in self.event_log[-5:]:
            print(f"{event['time']:<20}{event['event']:<30}{event['request_id']:<10}")

    def display_graphs(self):
        rejection_rate = self.rejection_count / self.total_requests * 100
        print(f"Процент отказов: {rejection_rate:.2f}%")
        plt.plot([len(self.buffer.requests) for _ in range(len(self.event_log))])
        plt.title("Загрузка буфера")
        plt.xlabel("Шаг")
        plt.ylabel("Количество заявок")
        plt.show()