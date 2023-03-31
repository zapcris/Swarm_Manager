import asyncio
import sys
from threading import Thread
from time import sleep
import numpy as np
from scipy.spatial import distance

from Greedy_implementation.SM07_Robot_agent import data_opcua

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
wk_loc = [900, 100]
wk_loc2 = [200, 200]
id = 1

def rising_edge(data, threshold):
    sign = data >= threshold
    pos = np.where(np.convolve(sign, [1, -1]) == 1)
    return pos

data = np.array([0])
trigger = rising_edge(data, 0.3)
print(trigger)
# while True:
#     a = 0
#     dist = distance.euclidean(wk_loc, data_opcua["robot_pos"][id-1])
#     print(dist)
#     sleep(4)
#     # if a == 0 and count ==0 :
#     #     q1.put_nowait((a,100))
#     #     print("Data entered")
#     #     count += 1
#
#
#     # else:
#     #     pass
