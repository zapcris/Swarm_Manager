import asyncio
import queue
import tracemalloc
from threading import Thread
from time import sleep

tracemalloc.start()

####### Normal queue functionality####
q_main_to_releaser = asyncio.Queue()
alloted_task = [m for m in range(1000)]

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
    if id >= 0 and id <=3:
        loop.call_soon_threadsafe(event1.set)
        print("Triggered event is 1")
    elif id >= 4 and id <=6:
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

#asyncio.run(main())


try:
    asyncio.ensure_future(main())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()

##### Start Task releaser to Robot thread################

