from Greedy_implementation.SM10_Product_Task import Task

T = Task(id=1, type=1, command=[11,2], pI=1, pV=1, allocation= True,status="first",robot=1)

print(T.command)


data_opcua = {
    "brand": "Ford",
    "mobile_manipulator": ["", "", ""],
    "rob_busy": [False, False, False],
    "machine_pos": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], ],
    "robot_pos": [[0, 0], [0, 0], [0, 0]],
    "create_part": 0,
    "mission": ["", "", "", "", "", "", "", "", "", ""],
    "robot_exec": [False, False, False]
}
def check_cond(input):
    return input

condition = data_opcua["rob_busy"][1]

print(check_cond(condition))

from random import random
import asyncio


# task coroutine
async def task(condition, work_list):
    # acquire the condition
    async with condition:
        # generate a random value between 0 and 1
        value = random()
        # block for a moment
        await asyncio.sleep(value)
        # add work to the list
        work_list.append(value)
        print(f'Task added {value}')
        # notify the waiting coroutine
        condition.notify()


# main coroutine
async def main():
    # create a condition
    condition = asyncio.Condition()
    # define work list
    work_list = list()
    # create and start many tasks
    _ = [asyncio.create_task(task(condition, work_list)) for _ in range(5)]
    # acquire the condition
    async with condition:
        # wait to be notified
        await condition.wait_for(lambda: len(work_list) == 5)
        # report final message
        print(f'Done, got: {work_list}')


# run the asyncio program
asyncio.run(main())
