



import asyncio
import sys
from threading import Thread
from time import sleep




step =10

match step:
    case 0:
        print("Step 1")

    case 1:
        print("Step2")

    case 10:
        print("Step10")
        step = 11

    case 11:
        print("step11")

print(step)
sys.exit()
q1 = asyncio.Queue()



async def queue(q1):
    while True:
        try:
            data, prod = q1.get_nowait()
            print("Retrieved value", data, prod)
            if data !=0 :
                print("Data alloted")
            elif data ==0:
                await asyncio.sleep(5)
                print("Data queued back again")
                prod +=100
                q1.put_nowait((data, prod))


        except:
            pass

def run_queue(q1):
    asyncio.run(queue(q1))


task_waiting_thread = Thread(target=run_queue, daemon=True, args=(q1, ))
task_waiting_thread.start()

count = 0

while True:
    a = 0

    sleep(4)
    if a == 0 and count ==0 :
        q1.put_nowait((a,100))
        print("Data entered")
        count += 1

    else:
        pass
