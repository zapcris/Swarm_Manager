import asyncio
from dataclasses import dataclass
from threading import Thread
from time import sleep

q1 = asyncio.Queue()
q2 = asyncio.Queue()


@dataclass
class Task:
    id: int
    allocation: bool
    robot: int


async def wait_queue():
    while True:
        try:
            task, prod = q2.get_nowait()
            print("Retrieved value in q2", task, prod)
            if task.allocation:
                print(f"Task {task} finally alloted in q2")
            elif not task.allocation:
                await asyncio.sleep(5)
                print(f"Task {task} queued back againto q2")
                prod += 100
                q2.put_nowait((task, prod))


        except:
            pass


def run_wait_queue():
    asyncio.run(wait_queue())


async def queue():
    while True:
        try:
            task, prod = q1.get_nowait()
            print("Retrieved value in q1", task, prod)
            if task.allocation == True:
                print(f"Task {task} alloted to robot {task.robot}")
            elif task.allocation == False:
                await asyncio.sleep(5)
                print(f"Task {task} queued into waiting queue")
                # prod +=100
                q2.put_nowait((task, prod))


        except:
            pass


def run_queue():
    asyncio.run(queue())


task_thread = Thread(target=run_queue, daemon=True)
task_thread.start()
task_waiting_thread = Thread(target=run_wait_queue, daemon=True)
task_waiting_thread.start()

count = 0

Task1 = Task(id=1, allocation=False, robot=999)
Task2 = Task(id=2, allocation=True, robot=1)

while True:
    a = 0

    sleep(4)
    if count == 0:
        q1.put_nowait((Task1, 100))
        print("Task1 entered")
        q1.put_nowait((Task2, 100))
        print("Task2 entered")
        count += 1

    else:
        pass
