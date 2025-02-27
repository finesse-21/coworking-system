import random
from datetime import datetime, timedelta
from typing import List
import matplotlib.pyplot as plt
from models.buffer import Buffer
from models.client import Client
from models.scheduler import Scheduler
from models.workplace import Workplace
import numpy as np

def format_time(time: datetime) -> str:
    """Форматирует время в формат ЧЧ:ММ:СС.ммм."""
    return time.strftime("%H:%M:%S.%f")[:-3]


def simulate_step_by_step(num_workplaces: int, buffer_size: int, simulation_steps: int, num_clients: int):
    buffer = Buffer(buffer_size)
    workplaces = [Workplace(id=i) for i in range(1, num_workplaces + 1)]
    scheduler = Scheduler(buffer, workplaces)
    clients = [Client(id=i) for i in range(1, num_clients + 1)]

    request_counter = 1
    current_time = datetime.now()

    for step in range(simulation_steps):
        print(f"\nШаг {step + 1}")
        input("Нажмите Enter для выполнения следующего шага...")

        for client in clients:
            if random.random() < 0.9:
                request = client.generate_request(request_counter)
                request_counter += 1
                request.arrival_time = current_time + timedelta(seconds=random.uniform(0.0, 2.0))
                print(
                    f"Заявка {request.id} от клиента {client.id} поступила в {format_time(request.arrival_time)}"
                    f" (время использования: {request.service_time.total_seconds():.3f} сек)")

                if buffer.is_empty():
                    if scheduler.assign_workplace(request, current_time):
                        print(f"Заявка {request.id} назначена на рабочее место")
                    else:
                        removed_request = scheduler.add_request_to_buffer(request)
                        if removed_request:
                            print(f"Буфер переполнен. Заявка {removed_request.id} вытеснена из буфера.")
                        print(f"Заявка {request.id} добавлена в буфер")
                else:
                    removed_request = scheduler.add_request_to_buffer(request)
                    if removed_request:
                        print(f"Буфер переполнен. Заявка {removed_request.id} вытеснена из буфера.")
                    print(f"Заявка {request.id} добавлена в буфер")

        for workplace in workplaces:
            if workplace.is_busy and workplace.current_request is not None:
                request = workplace.current_request
                if current_time >= request.start_time + request.service_time:
                    workplace.end_service(current_time)
                    print(f"Рабочее место {workplace.id} завершило обработку заявки {request.id}")

        if not buffer.is_empty():
            for workplace in workplaces:
                if not workplace.is_busy:
                    next_request = scheduler.get_next_request()
                    if next_request:
                        workplace.start_service(next_request, current_time)
                        print(f"Заявка {next_request.id} извлечена из буфера и назначена на рабочее место {workplace.id}")

        print("\nСостояние системы:")
        print(f"Буфер: {[req.id for req in buffer.requests if req is not None]}")
        print("Рабочие места:")
        for workplace in workplaces:
            if workplace.is_busy:
                print(f"Рабочее место {workplace.id}: Занят (Заявка {workplace.current_request.id})")
            else:
                print(f"Рабочее место {workplace.id}: Свободен")

        current_time += timedelta(seconds=1)


def print_statistics(total_requests: int, workplaces: List[Workplace], simulation_duration: int, rejected_requests: int,
                     rejection_percentage: float, average_system_time: float):
    """Выводит статистику симуляции."""
    print("\nСтатистика симуляции:")
    print(f"Общее количество созданных заявок: {total_requests}")
    print(f"Количество отклоненных заявок: {rejected_requests}")
    print(f"Процент отклонения заявок: {rejection_percentage:.2f}%")
    print(f"Среднее время нахождения в системе: {average_system_time:.3f} сек")

    print("\nЗагруженность рабочих мест:")
    print(f"{'Рабочее место':<15} {'Время занятости (сек)':<20} {'Процент загруженности':<20}")

    total_busy = 0
    for workplace in workplaces:
        busy_time_seconds = workplace.total_busy_time.total_seconds()
        busy_percentage = (busy_time_seconds / simulation_duration) * 100
        total_busy += busy_percentage
        print(f"     {workplace.id:<15} {busy_time_seconds:<20.2f} {busy_percentage:.2f}%")
    print(f"Средняя загруженность: {total_busy / len(workplaces):.2f}%")

def plot_graphs(time_steps: List[float], buffer_sizes: List[int], clients: List[Client], workplaces: List[Workplace],
                simulation_duration: int):
    """Строит графики на основе данных симуляции."""
    plt.figure(figsize=(15, 10))

    plt.subplot(3, 1, 1)
    plt.plot(time_steps, buffer_sizes, label="Количество заявок в буфере")
    plt.xlabel("Время (сек)")
    plt.ylabel("Количество заявок")
    plt.title("Динамика количества заявок в буфере")
    plt.legend()

    plt.subplot(3, 1, 2)
    client_ids = [client.id for client in clients]
    avg_system_times = [
        client.total_system_time.total_seconds() / client.processed_requests if client.processed_requests > 0 else 0 for
        client in clients]
    plt.plot(client_ids, avg_system_times, label="Среднее время нахождения в системе")
    plt.xlabel("Номер клиента")
    plt.ylabel("Среднее время (сек)")
    plt.title("Среднее время нахождения в системе для каждого клиента")
    plt.xticks(client_ids)
    plt.legend()

    plt.subplot(3, 1, 3)
    workplace_ids = [workplace.id for workplace in workplaces]
    busy_percentages = [(workplace.total_busy_time.total_seconds() / simulation_duration) * 100 for workplace in
                        workplaces]
    plt.plot(workplace_ids, busy_percentages, label="Загруженность рабочих мест", color="orange")
    plt.xlabel("Номер рабочего места")
    plt.ylabel("Загруженность (%)")
    plt.title("Загруженность рабочих мест")
    plt.ylim(0, 100)
    plt.xticks(workplace_ids)
    plt.legend()

    plt.tight_layout()
    plt.show()


def print_client_statistics(clients: List[Client]):
    """Выводит таблицу с подробной статистикой по каждому клиенту."""
    print("\nСтатистика по клиентам:")
    print(
        f"| {'ID клиента':^12} | {'Заявок создано':^15} | {'Заявок обработано':^15} | {'Заявок отклонено':^18} "
        f"| {'% отклонения':^15} | {'Ср. T в системе (сек)':^25} | {'Ср. T обсл. (сек)':^18} "
        f"| {'Дисперсия T обсл.':^18} | {'Дисперсия T в системе':^20} |"
    )
    print("-" * 187)

    total_generated = 0
    total_processed = 0
    total_rejected = 0
    total_system_time = timedelta()
    system_times = []

    for client in clients:
        generated_requests = client.generated_requests
        processed_requests = client.processed_requests
        rejected_requests = generated_requests - processed_requests
        rejection_percentage = (rejected_requests / generated_requests * 100) if generated_requests > 0 else 0

        avg_system_time = client.average_system_time()
        avg_service_time = client.average_service_time()
        service_time_variance = client.service_time_variance()

        system_times_client = [
            (req.end_time - req.arrival_time).total_seconds() for req in client.requests if req.end_time is not None
        ]
        system_time_variance = np.var(system_times_client) if len(system_times_client) > 1 else 0

        print(
            f"| {client.id:^12} | {generated_requests:^15} | {processed_requests:^17} | {rejected_requests:^18} "
            f"| {rejection_percentage:^15.2f} | {avg_system_time:^25.2f} | {avg_service_time:^18.2f} "
            f"| {service_time_variance:^18.2f} | {system_time_variance:^21.2f} |"
        )
        print("-" * 187)

        total_generated += generated_requests
        total_processed += processed_requests
        total_rejected += rejected_requests
        total_system_time += client.total_system_time
        system_times.extend(system_times_client)

    overall_rejection_percentage = (total_rejected / total_generated * 100) if total_generated > 0 else 0
    overall_average_system_time = (total_system_time.total_seconds() / total_processed) if total_processed > 0 else 0
    return total_rejected, overall_rejection_percentage, overall_average_system_time

def simulate_automatic(num_workplaces: int, buffer_size: int, simulation_duration: int, num_clients: int):
    buffer = Buffer(buffer_size)
    workplaces = [Workplace(id=i) for i in range(1, num_workplaces + 1)]
    scheduler = Scheduler(buffer, workplaces)
    clients = [Client(id=i) for i in range(1, num_clients + 1)]

    request_counter = 1
    current_time = datetime.now()
    end_time = current_time + timedelta(seconds=simulation_duration)

    total_requests = 0
    rejected_requests = 0
    total_system_time = timedelta()
    processed_requests = 0

    time_steps = []
    buffer_sizes = []

    while current_time < end_time:
        time_steps.append((current_time - datetime.now()).total_seconds())
        buffer_sizes.append(len(buffer.requests))

        for client in clients:
            if random.random() < 0.9:
                request = client.generate_request(request_counter)
                request_counter += 1
                total_requests += 1
                request.arrival_time = current_time + timedelta(seconds=random.uniform(0.0, 2.0))

                if buffer.is_empty():
                    if scheduler.assign_workplace(request, current_time):
                        processed_requests += 1
                        request.start_time = request.arrival_time
                    else:
                        rejected_request = scheduler.add_request_to_buffer(request)
                        if rejected_request:
                            rejected_requests += 1
                            rejected_request.client.processed_requests -= 1
                else:
                    rejected_request = scheduler.add_request_to_buffer(request)
                    if rejected_request:
                        rejected_requests += 1
                        rejected_request.client.processed_requests -= 1

        for workplace in workplaces:
            if workplace.is_busy and workplace.current_request is not None:
                request = workplace.current_request
                if current_time >= request.start_time + request.service_time:
                    workplace.end_service(current_time)
                    processed_requests += 1
                    system_time = request.end_time - request.arrival_time
                    total_system_time += system_time

        if not buffer.is_empty():
            for workplace in workplaces:
                if not workplace.is_busy:
                    next_request = scheduler.get_next_request()
                    if next_request:
                        workplace.start_service(next_request, current_time)
                        next_request.start_time = current_time

        current_time += timedelta(seconds=1)

    total_rejected, rejection_percentage, average_system_time = print_client_statistics(clients)
    print_statistics(total_requests, workplaces, simulation_duration, total_rejected, rejection_percentage,
                     average_system_time)
    # plot_graphs(time_steps, buffer_sizes, clients, workplaces, simulation_duration)


if __name__ == "__main__":
    num_workplaces = 11
    num_clients = 5
    buffer_size = 15
    simulation_steps = 10
    simulation_duration = 300

    print("Выберите режим работы:")
    print("1. Пошаговый режим")
    print("2. Автоматический режим")
    mode = input("Введите номер режима: ")

    if mode == "1":
        simulate_step_by_step(num_workplaces, buffer_size, simulation_steps, num_clients)
    elif mode == "2":
        simulate_automatic(num_workplaces, buffer_size, simulation_duration, num_clients)
    else:
        print("Неверный выбор режима.")