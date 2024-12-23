from models.client import Client
from models.scheduler import Scheduler
from models.workplace import Workplace
from models.buffer import Buffer

def main():
    # Инициализация
    client = Client(id=1)
    workplaces = [Workplace(id=i + 1) for i in range(3)]
    buffer = Buffer(size=5)
    scheduler = Scheduler(buffer=buffer, workplaces=workplaces)

    # Выбор режима
    mode = input("Выберите режим (1 - пошаговый, 2 - автоматический): ")
    if mode == "1":
        step_by_step_mode(client, scheduler)
    elif mode == "2":
        automatic_mode(client, scheduler)
    else:
        print("Неверный выбор.")

def step_by_step_mode(client, scheduler):
    print("Пошаговый режим. Для перехода нажимайте Enter.")
    for _ in range(10):
        input("Нажмите Enter для следующего шага...")
        request = client.generate_request()
        scheduler.process_step(request)
        scheduler.display_state()

def automatic_mode(client, scheduler):
    print("Автоматический режим. Выполняется...")
    for _ in range(10):
        request = client.generate_request()
        scheduler.process_step(request)
    scheduler.display_graphs()

if __name__ == "__main__":
    main()