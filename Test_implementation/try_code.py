import asyncio

from Greedy_implementation.SM10_Product_Task import Task

a = [10, 20 ,30, 40]
b = []
event = asyncio.Event()
if b:
    print("list has elements")
else:
    print("list is empty")

q = asyncio.Queue()

task = Task(id=1, allocation=True, command=[1,2], robot=1, type=1, pV=1, pI=1,status="New")
id = 1

data = [task, id, event]
q.put_nowait(data)

new_data = q.get_nowait()

print(new_data[0],new_data[1],new_data[2])

new_data[2].clear()

print(new_data[2].is_set())