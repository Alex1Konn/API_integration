"""

1. Имитация загрузки файлов

Создайте 5 потоков. Каждый поток имитирует загрузку файла:
Выводит сообщение «Загрузка файла N началась».
Ждет случайное время от 1 до 5 секунд.
Выводит сообщение «Файл N загружен».
Главный поток должен дождаться завершения всех загрузок.
"""
# import time
# import random
# from threading import Thread
#
# def runner(num):
#     print(f"Загрузка файла N{num} началась")
#     t = random.randint(1, 5)
#     time.sleep(t)
#     print(f"Файл N{num} загружен")
#
# threads = []
# for i in range(5):
#     t = Thread(target=runner, args=(i + 1,))
#     threads.append(t)
#     t.start()
#
# for t in threads:
#     t.join()
#
# print("Все загрузки завершены")
"""
2. Производитель и потребитель

Создайте очередь (queue.Queue).
Поток-производитель помещает в очередь числа от 1 до 20.
Поток-потребитель извлекает числа из очереди и выводит их.
После обработки всех чисел программа должна корректно завершиться.
"""
#
# import threading
# import queue
#
# q = queue.Queue(maxsize=20)
#
# def producer():
#     for i in range(1, 21):
#         q.put(i)
#         print(f"Произвели: {i}. Это",  threading.current_thread().name)
#
# def consumer():
#     for _ in range(20):
#         x = q.get()
#         print(f"Потратили {x}. Это",  threading.current_thread().name)
#         q.task_done()
#
# t1 = threading.Thread(target=producer, name="Producer")
# t2 = threading.Thread(target=consumer, name="Consumer")
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()
#
# print("Все числа обработаны!")
"""
3. Подсчет четных чисел

Создайте список из 1000 случайных чисел. Используйте 4 потока для подсчета количества четных чисел в разных частях списка. Соберите общий результат.
"""
import threading
import random
import time

numbers = [random.randint(1,100) for _ in range(1000)]
print(f"Сгенерировано {len(numbers)} чисел")

counter = 0
lock = threading.Lock()
threads = []

def count_even(start, finish, thread1):
    global counter
    local_counter = 0

    for i in range(start, finish):
        if numbers[i] %2 ==0:
            local_counter += 1

    lock.acquire()
    counter += local_counter
    lock.release()

    print(f"[{thread1}] Обработанот {start, finish}, "
          f"найдено {local_counter} четных чисел")

print("Запуск потоков")

threads = []

part_size = len(numbers) // 4

for i in range(4):
    start = i * part_size
    finish = len(numbers) if i == 3 else (i + 1) * part_size

    thread = threading.Thread(
        target=count_even,
        args=(start, finish, f"Поток-{i + 1}"),
        daemon=False
    )

    threads.append(thread)
    thread.start()
    print(f"Запущен {f'Поток-{i + 1}'} (индексы: {start}-{finish})")

for thread in threads:
    thread.join()
    print(f"Поток {thread.name} завершился")

print(f"\nИТОГО четных чисел: {counter}")




"""
4. Печать чисел

Создайте два потока:
первый печатает числа от 1 до 5;
второй печатает числа от 6 до 10.
Наблюдайте порядок вывода.
"""
# import threading
# import time
#
# def first():
#     time.sleep(2)
#     print(f"Первый поток:")
#     for i in range(1, 6):
#         print(i)
#
# def second():
#     print(f"Второй поток:")
#     for k in range(6, 11):
#         print(k)
#
# t1 = threading.Thread(target=first)
# t2 = threading.Thread(target=second)
# t1.start()
# t2.start()
# t1.join()
# t2.join()