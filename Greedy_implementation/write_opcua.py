import asyncio
import queue
import tracemalloc
from datetime import datetime
from threading import Thread
from time import sleep

from Greedy_implementation.SM07_Robot_agent import Events, data_opcua

tracemalloc.start()

####### Normal queue functionality####
q_main_to_releaser = asyncio.Queue()
alloted_task = [m for m in range(10)]

for task in alloted_task:
    q_main_to_releaser.put_nowait(task)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

event1 = asyncio.Event()
event2 = asyncio.Event()
event3 = asyncio.Event()
def t_released(task):

    id = task
    print("Triggered robot id is:", id+1)
    if id == 0 or id == 2 :
        loop.call_soon_threadsafe(event1.set)
        print("Triggered event is 1")
    elif id == 1 and id <=3:
        loop.call_soon_threadsafe(event2.set)
        print("Triggered event is 2")
    else:
        loop.call_soon_threadsafe(event3.set)
        print("Triggered event is 3")

async def r_function():

    while True:

        try:
            # asyncio.run(T_robot[1].unlatch_busy())


            task_opcua = q_main_to_releaser.get_nowait()

            print(f"Task {task_opcua} picked from queue ")



            q_main_to_releaser.task_done()
            # done()
            # print("Execution task release", task_opcua)
            t_released(task=task_opcua)
            await asyncio.sleep(5)



            # Opt 1: Handle task here and call q.task_done()
        except queue.Empty:
            # Handle empty queue here
            pass

def start_queue():
    asyncio.run(r_function())

r_thread = Thread(target=start_queue, daemon=True)

r_thread.start()





async def factorial(name, number, event):
    #await event.wait()
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    event.clear()
    return f


async def main():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        factorial("A", 2, event1),
        factorial("B", 3, event2),
        factorial("C", 4, event3),
    )
    print(L)

async def execution_time(flag, id):

    while True:
        # print(f'waiting for robot {id} for  execution')
        await flag.wait()
        print(f'Robot {id} execution timer has started')
        start_time = datetime.now()
        if id == 1 :
            stime = 15
        elif id == 2:
            stime = 5
        elif id == 3:
            stime = 2
        else:
            stime = 0

        await asyncio.sleep(stime)

        # Events["rob_execution"][id - 1] = True
        # while Events["rob_execution"][id - 1] == True:
        #     if data_opcua["rob_busy"][id - 1] == True:
        #         # exec_time = (datetime.now() - start_time).total_seconds()
        #         # print(f"Robot {id} is running")
        #         pass
        #     elif data_opcua["rob_busy"][id - 1] == False:
        #         Events["rob_execution"][id - 1] = False
        exec_time = (datetime.now() - start_time).total_seconds()

        flag.clear()
        print(f"Robot {id} took {exec_time:,.2f} seconds to run")

        return None

#asyncio.run(main())
async def main2() :
    """Fetch all urls from the list of urls

    It is done concurrently and combined into a single coroutine"""


    results = await asyncio.gather(
        (execution_time(event1, 1)),
        (execution_time(event2, 2)),
        (execution_time(event3, 3))
    )
    print(results)

try:
    asyncio.ensure_future(main2())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()

##### Start Task releaser to Robot thread################

