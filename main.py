"""
Синхронное программирование (!= синхронное взаимодействие) - последовательное
выполненийе функций и шагов. Сейчас мы пишем
в стиле

Асинхронное программирование - паралельное
Асинхронная функция называется - корутина - не мжет быть одна,
нужно переписать все функции на асинхронность. Исключенгие если пишем на iogramm
там могут быть и обычными функциями

import asyncio

async def hello():
    print('Привет!')

asyncio.run(hello())

#
import asyncio

async def main():
    print("Старт")
    await asyncio.sleep(2)
    print("Конец")

asyncio.run(main())

#
import asyncio

async def task(name, delay):
    await asyncio.sleep(delay)
    print(f"{name} Готово")

async def main():
    await task("A", 1)
    await task("B", 1)

asyncio.run(main())


#Паралельный запуск через gather
# gather - запуск  корутин асинхронно (пареллельно)
# почему-то - не отработало, нужно было ретурны поменять на принты
import asyncio
async def task(name, delay):
    await asyncio.sleep(delay)
    return(f"{name} Готово")

async def main():
    result = await asyncio.gather(
        task("A", 1),
        task("B", 5),
        task("C", 1)
    )
    print(result)
asyncio.run(main())


# РАБОТВЮЩИЙ ПРМИЕР С gather
import asyncio
async def hello_a():
    await asyncio.sleep(1)
    print("Привет A")

async def hello_b():
    await asyncio.sleep(4)
    print("Привет B")

async def hello_c():
    await asyncio.sleep(1)
    print("Привет C")

async def main():
    result = await asyncio.gather(
        hello_a(),
        hello_b(),
        hello_c()
    )
    # print(result)

asyncio.run(main())

# Асинхронный таймер с обратным отсчетом
import asyncio
async def timer(name, seconds):
    for i in range(seconds, 0, -1):
        print(f"[{name} осталось {i} секунд]")
        await asyncio.sleep(1)
    print(f"[{name} Время вышло!]")

async def main():
    await asyncio.gather(
        timer('чай', 4),
        timer('Приготовление риса', 6)
    )

asyncio.run(main())


# Ассинхронный веб краулер(имитация) или веб-паук - технология посиковиков для ранжирования сайтов
import asyncio, random

visited = set() #пустое множество повтори!

async def crawl(url, depth=0):
    if url in visited or depth > 2:
        return visited.add(url)
    await asyncio.sleep(random.uniform(0.1, 0.4))
    print(" " * depth + f"Посетил {url}")
    children = [f"{url}/{c}" for c in ("a", "b")]
    await asyncio.gather(*(crawl(c, depth + 1) for c in children))#рекурсивная функция

asyncio.run(crawl("site"))

asyncio.wait_for() в Python — это встроенная функция,
которая позволяет запустить асинхронную задачу или корутину с ограничением по времени.
 Она ждет завершения операции заданное количество секунд.Если операция завершается вовремя,
 возвращается ее результат.
Если время истекает раньше, функция отменяет задачу и вызывает исключение

#тайм-аут на группу задач
# Отметить все, что не успели за отведенное время

import asyncio
async def job(i):
    await asyncio.sleep(i)
    print(f"Job {i}")

async def main():
    tasks = [job(i) for i in range(1, 6)]
    try:
        results = await asyncio.wait_for(asyncio.gather(*tasks), timeout=3)
        print(results)
    except asyncio.TimeoutError:
        print(f"Не все задачи успели за 3 секунду")

asyncio.run(main())

# МНОГОПОТОЧНОЕ ПРОГРАМИРОВАНИЕ. ПРОЦЕСС. ПОТОК
GIL (Global Interpreter Lock) — это глобальный блокировщик интерпретатора
 в классическом Python (CPython), который позволяет
только одному потоку выполнять код в конкретный момент времени, даже на многоядерных процессора.
Главная задача GIL — защита управления памятью (сборщика мусора) от одновременного доступа.
Без этой блокировки в многопоточной среде возникали бы состояния гонки (race conditions)
и повреждения данных
CPU-bound задачи - многопоточность не ускоряет потокли а лишь конкурирует за GIL
I|0 bound задачи (сеть диск БД) многопточность эффективна потомучто приожидании
вводвывода пооток совобождаяет GIL и другой поток работает


# 1й пример
import threading

def worker(name):
    print(f"Поток {name} работает")

t = threading.Thread(target=worker, args=("A",))
t.start()
t.join()

Асинхронность работает в рамках одного потока.

# Пример запуска когда все просыпется в разном порядке как отработал процессор
import time

from threading import Thread

def sleepMe(i):
    print(f"Поток {i} засыпает на 5 секунд {i}")
    time.sleep(5)
    print(f"Поток {i} сейчас проснулся {i}")

for i in range(10):
    th = Thread(target=sleepMe, args=(i,))
    th.start()


#Таймер напоминания
import time
from threading import Thread

#делаем отдельную функцию с напоминанием
def remind():
    text = str(input("О чем вам напомнить?"))

    local_time = float(input("Через сколько минут?"))
    local_time = local_time * 60

    time.sleep(local_time)
    print(text)
# Создаем новый поток Пишем всегда th при создании нового потока

th = Thread(target=remind, args=())
th.start()
#пока работает поток выведем что-то на экран через 20 секунд после запуска
time.sleep(20)
print("Пока поток работает, мы можем сделать что-нибудь еще")

#многопоточнось оптимизурет все для железа,
# а если работа с дисками лили бд, т.е. что-то дл приложения то асинхронность



import threading
#поочереддный вывод чисел #Создайте 2 потока: 1й выводит нечетные числа, второй четные. Полка не стали дедать

#Гонка потоков. Создайте 5 потоков. Каждый бежит случайное время(напрмиерб спит от 500 - 3000 мс)
# после чего сообщает о финише

import time
import random
from threading import Thread

def runner(num):
    t = random.randint(1, 3)
    time.sleep(t)
    print(f"Поток {num} финишировал")

threads = []
for i in range(5):
    t = threading.Thread(target=runner, args=(i + 1,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Все участники завершили гонку")



# Создать 2 потока.
# 1 приветб 2 мир
#Написать готово после выводы

import threading
def hello():
    print("Привет")

def world():
    print("мир")

t1 = threading.Thread(target=hello)
t2 = threading.Thread(target=world)
t1.start()
t2.start()
t1.join()
t2.join()

print("Все готово")


#два потока считают. 1 - выводит 1 2 3 4 5 , 2 - 6789 10


import threading
import time

def first():
    time.sleep(2)
    print(f"Первый поток:")
    for i in range(1, 6):
        print(i)

def second():
    print(f"Второй поток:")
    for k in range(6, 11):
        print(k)

t1 = threading.Thread(target=first)
t2 = threading.Thread(target=second)
t1.start()
t2.start()
t1.join()
t2.join()

#передача параметра

import threading

def print_number(n):
    print(n)

t = threading.Thread(target=print_number, args=(100,))
t.start()
t.join()

# именование потока

import threading
def task():
    print("Работает поток", threading.current_thread().name)

t = threading.Thread(target=task, name="Worker")
t.start()
t.join()



#Производитель-потребитель. 1-поток - создает числаЖ 12345.... . 2-поток их забирает и печатает
#используйте очередб ограниченного рпзмера напрмиер 5 элементов

import threading
import queue

q = queue.Queue(maxsize=5)

def producer():
    for i in range(1, 11):
        q.put(i)
        print(f"Произвели: {1}. Это",  threading.current_thread().name)

def consumer():
    for _ in range(10):
        x = q.get()
        print(f"Потратили {x}. Это",  threading.current_thread().name)
        q.task_done()

t1 = threading.Thread(target=producer, name="Producer")
t2 = threading.Thread(target=consumer, name="Consumer")
t1.start()
t2.start()
t1.join()
t2.join()

threading.Lock() - эта функция создаёт объект блокировки (lock), который нужен для синхронизации
потоков и защиты общих данных от одновременного доступа.
Проще говоря, Lock работает как «дверь»: пока один поток «открывает» дверь
(получает блокировку), другие потоки вынуждены ждать. Это нужно, чтобы избежать состояния гонки (race condition) — ситуации, когда несколько
потоков пытаются одновременно изменить общие данные, и результат получается непредсказуемым

Оператор global в Python позволяет функции изменять значение глобальной переменной —
то есть объявленной вне функции, на уровне модуля.
Без этого ключевого слова Python воспринимает любое присваивание внутри функции
 как создание локальной переменной — даже если снаружи уже есть глобальная с таким же именем.
 Ключевое слово global явно указывает, что нужно работать с глобальной переменной,
  а не создавать локальную.


#Блокировка потоков
#Создайте 10 потоков, каждый увеличивает его на 1000
#После завершения всех потоков результат должен быть 10 000
import threading
counter = 0
lock = threading.Lock()
def worker():
    global counter
    for _ in range(1000):
        with lock:
            counter += 1

threads = []
for _ in range(10):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(counter)


#Есть счет баланс 1000. Несколько потоков одновременно снимают деньги.
#Необходимо предовратить ситуцацию когда баланс становиться  отрицательным из-за гонки данных


import threading
counter = 10000

def worker():
    global counter
    for _ in range(1000):
        with lock:
            counter -= 1

threads = []
for _ in range(12):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
    Lock.acquire(blocking=True, counter=0)

for t in threads:
    t.join()

print(counter)
"""