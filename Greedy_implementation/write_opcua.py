import asyncio
import queue
import tracemalloc
from datetime import datetime
import random
from threading import Thread
from time import sleep

from Greedy_implementation.SM04_Task_Planner import order
from Greedy_implementation.SM07_Robot_agent import Events, data_opcua

tracemalloc.start()

####### Normal queue functionality####
q_main_to_releaser = asyncio.Queue()
alloted_task = [m for m in range(10)]

for task in alloted_task:
    q_main_to_releaser.put_nowait(task)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
Task_allocation = False

### events flags for transfer and workstation robots#####
event1 = asyncio.Event()
event2 = asyncio.Event()
event3 = asyncio.Event()
wk_1 = asyncio.Event()
wk_2 = asyncio.Event()
wk_3 = asyncio.Event()
wk_4 = asyncio.Event()
wk_5 = asyncio.Event()
wk_6 = asyncio.Event()
wk_7 = asyncio.Event()
wk_8 = asyncio.Event()
wk_9 = asyncio.Event()
wk_10 = asyncio.Event()

robot_state = []
robot_dict= { "id" : int,
         "task" : []
        }
for i in range(3):
    rob = robot_dict
    robot_state.append(rob)

def wk_event(wk):
    if wk == 1:
       return wk_1
    elif wk == 2:
        return wk_2
    elif wk == 3:
        return wk_3
    elif wk == 4:
        return wk_4
    elif wk == 5:
        return wk_5
    elif wk == 6:
        return wk_6
    elif wk == 7:
        return wk_7
    elif wk == 8:
        return wk_8
    elif wk == 9:
        return wk_9
    elif wk == 10:
        return wk_10




def t_released(id,task):

    id = id
    task = task

    print("Triggered robot id is:", id+1)
    if id == 0 or id == 2 :
        robot_state[0]["task"] = task
        print("the task alloted to robot 1 is ",robot_state[0]["task"])

        loop.call_soon_threadsafe(event1.set)
        print("Triggered event is 1")
    elif id == 1 and id <=3:
        robot_state[1]["task"] = task
        print("the task alloted to robot 2 is ", robot_state[1]["task"])
        loop.call_soon_threadsafe(event2.set)
        print("Triggered event is 2")
    else:
        robot_state[2]["task"] = task
        print("the task alloted to robot 3 is ", robot_state[2]["task"])
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
            t_released(id=task_opcua, task=[random.randint(1, 10), random.randint(1, 10)])
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



        print(f"Robot {id} took {exec_time:,.2f} seconds to run")
        task = robot_state[id-1]["task"]
        print(f"the product is delivered to workstation {task}")
        a =  wk_event(task[1])

        loop.call_soon_threadsafe(a.set)
        rob_released()
        #await process_execution(task[1], 1)
        print("Triggered workstation is  is",task[1])
        flag.clear()


        return None

async def process_execution(wk, product_pv):
    process_time = order["Process_times"][product_pv][wk-1]
    #await event.wait()
    print(f"Process task executing at {wk}")
    await asyncio.sleep(process_time)
    print("Process task completed on workstation ",wk )
    prod_release()
    #event.clear()

def prod_release():
    global Task_allocation
    Task_allocation = True
    return

def free_wk():
    return
def rob_released():
    return

#asyncio.run(main())
async def main2() :
    """Fetch all urls from the list of urls

    It is done concurrently and combined into a single coroutine"""


    results = await asyncio.gather(
        (execution_time(event1, 1 )),
        (execution_time(event2, 2)),
        (execution_time(event3, 3,))
        # (process_execution(wk_1, 1, 1)),
        # (process_execution(wk_2, 2, 1)),
        # (process_execution(wk_3, 3, 1)),
        # (process_execution(wk_4, 4, 1)),
        # (process_execution(wk_5, 5, 1)),
        # (process_execution(wk_6, 6, 1)),
        # (process_execution(wk_7, 7, 1)),
        # (process_execution(wk_8, 8, 1)),
        # (process_execution(wk_9, 9, 1)),
        # (process_execution(wk_10, 10, 1))
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

