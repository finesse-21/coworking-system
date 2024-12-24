from models.client import Client
from models.scheduler import Scheduler
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
import random

event_calendar = []
last_event_index = 0
request_workplace_map = {}

# Основной цикл симуляции
def run_simulation_step(scheduler, client, completed_requests, rejected_requests, current_time):
    created_requests = 0
    requests = client.generate_requests(current_time)
    client.requests.extend(requests)
    for request in requests:
        event_calendar.append(f"Заявка {request.id} сгенерирована в {current_time}")
        workplace_id = scheduler.assign_workplace(request)
        if workplace_id is not None:
            event_calendar.append(f"Заявка {request.id} назначена на рабочее место {workplace_id}")
            request_workplace_map[request.id] = workplace_id  # Map request to workplace
        else:
            rejected_request = scheduler.add_request_to_buffer(request)
            if rejected_request:
                rejected_requests.append(rejected_request)  # Add rejected request to the list
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
            request_workplace_map[request.id] = workplace.id  # Map request to workplace

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

def run_simulation_auto(scheduler, client, duration_seconds):
    completed_requests = []
    rejected_requests = []
    generator_stats = {i: {'generated': 0, 'rejected': 0, 'waiting_times': [], 'system_times': [], 'service_times': []} for i in range(client.num_generators)}
    workplace_stats = {workplace.id: 0 for workplace in scheduler.workplaces}

    start_time = datetime.now()
    current_time = start_time

    while (datetime.now() - start_time).seconds < duration_seconds:
        created_requests = run_simulation_step(scheduler, client, completed_requests, rejected_requests, current_time)

        # Обновление статистики
        for request in completed_requests:
            generator_id = request.client
            generator_stats[generator_id]['generated'] += 1
            if request.status == "отклонена":
                generator_stats[generator_id]['rejected'] += 1
            elif request.status == "завершен" and request.start_time and request.end_time:
                waiting_time = max(0, (request.start_time - request.arrival_time).total_seconds())
                system_time = max(0, (request.end_time - request.arrival_time).total_seconds())
                service_time = max(0, (request.end_time - request.start_time).total_seconds())
                generator_stats[generator_id]['waiting_times'].append(waiting_time)
                generator_stats[generator_id]['system_times'].append(system_time)
                generator_stats[generator_id]['service_times'].append(service_time)

        # Учёт занятости рабочих мест
        for workplace in scheduler.workplaces:
            if workplace.is_busy:
                workplace_stats[workplace.id] += 1

        current_time += timedelta(seconds=1)

    # Рассчёт средней статистики
    for stats in generator_stats.values():
        stats['rejection_percentage'] = (stats['rejected'] / stats['generated']) * 100 if stats['generated'] > 0 else 0
        stats['avg_waiting_time'] = sum(stats['waiting_times']) / len(stats['waiting_times']) if stats['waiting_times'] else 0
        stats['avg_system_time'] = sum(stats['system_times']) / len(stats['system_times']) if stats['system_times'] else 0
        stats['avg_service_time'] = sum(stats['service_times']) / len(stats['service_times']) if stats['service_times'] else 0

    return completed_requests, rejected_requests, generator_stats, workplace_stats

def print_statistics(scheduler, client, generator_stats, rejected_requests, completed_requests, workplace_stats):
    total_requests = len(client.requests)
    rejected_requests_count = len(rejected_requests)
    rejection_rate = (rejected_requests_count / total_requests) * 100 if total_requests > 0 else 0

    print(f"Всего сгенерировано заявок: {total_requests}")
    print(f"Количество отклонённых заявок: {rejected_requests_count}")
    print(f"Процент отклонения: {rejection_rate:.2f} %")

    print("\nВремя обслуживания рабочего места:")
    for workplace_id, time_busy in workplace_stats.items():
        print(f"Рабочее место {workplace_id}: было занято {time_busy} секунд")

    print("\nСтатистика по каждому генератору:")
    for generator_id, stats in generator_stats.items():
        total_generated = stats['generated']
        total_rejected = stats['rejected']
        rejection_rate = (total_rejected / total_generated) * 100 if total_generated > 0 else 0
        avg_waiting_time = stats['avg_waiting_time']
        avg_system_time = stats['avg_system_time']
        avg_service_time = stats['avg_service_time']

        print(f"Генератор {generator_id}:")
        print(f"  Сгенерировано заявок: {total_generated}")
        print(f"  Процент отклонённых заявок: {rejection_rate:.2f} %")
        print(f"  Среднее время ожидания заявки: {avg_waiting_time:.2f} секунд")
        print(f"  Среднее время в системе: {avg_system_time:.2f} секунд")
        print(f"  Среднее время обслуживания заявки: {avg_service_time:.2f} секунд")

def main():
    buffer_size = 10  # Размер буфера
    num_workplaces = 2  # Количество рабочих мест
    num_generators = 2  # Количество генераторов заявок
    scheduler = Scheduler(buffer_size, num_workplaces)
    client = Client(1, num_generators)
    rejected_requests = []  # Store rejected requests in main
    completed_requests = []  # Store completed requests in main

    mode = input("Выберите режим: 'a' для автоматического или 's' для пошагового: ")

    if mode == 's':
        for step in range(1, 11):
            created_requests = run_simulation_step(scheduler, client, completed_requests, rejected_requests, datetime.now())
            state_info = get_model_state(scheduler, completed_requests, step, created_requests)
            print(state_info)
            input("Нажмите Enter для следующего шага...")
            time.sleep(0.1)  # Добавляем небольшую задержку
    elif mode == 'a':
        duration = int(input("Введите продолжительность симуляции (в секундах): "))
        completed_requests, rejected_requests, generator_stats, workplace_stats = run_simulation_auto(scheduler, client, duration)
        print_statistics(scheduler, client, generator_stats, rejected_requests, completed_requests, workplace_stats)

if __name__ == "__main__":
    main()