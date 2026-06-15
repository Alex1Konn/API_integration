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
"""
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