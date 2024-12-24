from models.client import Client
from models.scheduler import Scheduler
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

event_calendar = []
last_event_index = 0

def is_any_workplace_free(scheduler):
    return any(not workplace.is_busy for workplace in scheduler.workplaces)

# Основной цикл симуляции
def run_simulation_step(scheduler, client, completed_requests, current_time):
    created_requests = 0
    requests = client.generate_requests(current_time)
    for request in requests:
        event_calendar.append(f"Заявка {request.id} сгенерирована в {current_time}")
        workplace_id = scheduler.assign_workplace(request)
        if workplace_id is not None:
            event_calendar.append(f"Заявка {request.id} назначена на рабочее место {workplace_id}")
        else:
            rejected_request = scheduler.add_request_to_buffer(request)
            if rejected_request:
                event_calendar.append(f"Заявка {rejected_request.id} отклонена из-за переполнения буфера в {current_time}")
            event_calendar.append(f"Заявка {request.id} добавлена в буфер")
        created_requests += 1

    for workplace in scheduler.workplaces:
        completed_request = workplace.end_service()
        if completed_request:
            completed_requests.append(completed_request)
            event_calendar.append(f"Заявка {completed_request.id} завершена в {current_time}")

    # Назначение заявок на рабочие места
    for workplace in scheduler.workplaces:
        if not workplace.is_busy and not scheduler.buffer.is_empty():
            request = scheduler.buffer.remove_request()
            workplace.start_service(request)
            event_calendar.append(f"Заявка {request.id} назначена на рабочее место {workplace.id}")

    return created_requests


# Формализованная схема модели — текущий статус
def get_model_state(scheduler, completed_requests, step, created_requests):
    global last_event_index
    state_info = []
    state_info.append(f"Шаг {step}")
    state_info.append(f"[Клиент] -> Заявок создано: {created_requests}")
    state_info.append(f"[Буфер] -> Заявок в буфере: {scheduler.buffer.get_size()} "
                      f"{'(пуст)' if scheduler.buffer.is_empty() else '(полон)' if scheduler.buffer.is_full() else ''}")
    state_info.append("Содержимое буфера:")
    for request in scheduler.buffer.requests:
        state_info.append(f"  Заявка ID {request.id}")
    state_info.append("[Рабочие места]")
    for workplace in scheduler.workplaces:
        status = "свободен" if not workplace.is_busy else f"занят (Заявка ID {workplace.current_request.id})"
        state_info.append(f"  Рабочее место {workplace.id}: {status}")
    state_info.append("\n")
    state_info.append("Календарь событий:")
    for event in event_calendar[last_event_index:]:
        state_info.append(event)
    last_event_index = len(event_calendar)
    state_info.append("\n")
    return "\n".join(state_info)

# Автоматический режим
def run_simulation_auto(scheduler, client, duration_seconds):
    completed_requests = []
    start_time = datetime.now()
    current_time = start_time

    while (datetime.now() - start_time).seconds < duration_seconds:
        run_simulation_step(scheduler, client, completed_requests, current_time, batch_mode=True)
        current_time += timedelta(seconds=1)

    return completed_requests

# Построение графиков
def plot_statistics(completed_requests):
    times = [req.end_time - req.start_time for req in completed_requests if req.end_time]
    service_times = [t.total_seconds() for t in times]

    # Plot service times
    plt.figure()
    plt.plot(range(len(service_times)), service_times, label="Service Time")
    plt.xlabel("Steps")
    plt.ylabel("Seconds")
    plt.title("Service Time per Request")
    plt.legend()
    plt.grid()

    plt.show()

def main():
    buffer_size = 10  # Размер буфера
    num_workplaces = 4  # Количество рабочих мест
    num_generators = 4  # Количество генераторов заявок
    scheduler = Scheduler(buffer_size, num_workplaces)
    client = Client(1, num_generators)

    mode = input("Выберите режим: 'a' для автоматического или 's' для пошагового: ")

    if mode == 's':
        completed_requests = []
        for step in range(1, 11):
            created_requests = run_simulation_step(scheduler, client, completed_requests, datetime.now(), batch_mode=True)
            state_info = get_model_state(scheduler, completed_requests, step, created_requests)
            print(state_info)
            input("Нажмите Enter для следующего шага...")
            time.sleep(0.1)  # Добавляем небольшую задержку
    elif mode == 'a':
        duration = int(input("Введите продолжительность симуляции (в секундах): "))
        completed_requests = run_simulation_auto(scheduler, client, duration)
        plot_statistics(completed_requests)
        print("Автоматический режим завершен.")

if __name__ == "__main__":
    main()