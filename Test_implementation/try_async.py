import asyncio

async def task1():
    print("Task 1 is running")
    await asyncio.sleep(1)
    print("Task 1 is calling Task 2")
    await task2()
    print("Task 1 is finished")

async def task2():
    print("Task 2 is running")
    await asyncio.sleep(1)
    print("Task 2 is calling Task 1")
    await task1()
    print("Task 2 is finished")

##############
order = {
    "Name": "Test",
    "PV": 1,
    "sequence": [[11, 1, 7, 5, 6, 8, 9, 12]],
    "PI": [1],
    "Wk_type": [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    "Process_times": [[20, 30, 40, 50, 20, 40, 80, 70, 30, 60]]
}

print(order["Process_times"][0][0])