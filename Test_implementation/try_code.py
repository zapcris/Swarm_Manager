import asyncio
from datetime import time
from threading import Thread
from time import sleep

from Greedy_implementation.SM02_opcua_client import start_opcua
from Greedy_implementation.SM04_Task_Planning_agent import order
from Greedy_implementation.SM05_Scheduler_agent import Scheduling_agent
from Greedy_implementation.SM06_Task_allocation import Task_Allocator_agent
from Greedy_implementation.SM07_Robot_agent import T_robot, Product_task, data_opcua
from Greedy_implementation.SM10_Product_Task import Task, Product
from scipy.spatial import distance


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
q.put_nowait(data)



##### Start OPCUA Client Thread################
opcua_client = Thread(target=start_opcua, daemon=True, args=(data_opcua,))
opcua_client.start()


print("Workstation positions", data_opcua["machine_pos"])

print("Robot positions", data_opcua["robot_pos"])

print("Robot positions", data_opcua["rob_busy"])

while True:
    ######### between workstation 3 and 4 ################
    sleep(4)
    # task_cost1 = distance.euclidean(data_opcua["machine_pos"][2], data_opcua["machine_pos"][4])
    # marginal_cost_1 = distance.euclidean(data_opcua["machine_pos"][2], data_opcua["robot_pos"][1])
    # marginal_cost_2 = distance.euclidean(data_opcua["machine_pos"][2], data_opcua["robot_pos"][2])
    # total_c1 = task_cost1 + marginal_cost_1
    # total_c2 = task_cost1 + marginal_cost_2
    #
    # print("Task (3,5)  robot 2", marginal_cost_1)
    # print("Task (3,5)  robot 3", marginal_cost_2)
    #
    # task_cost2 = distance.euclidean(data_opcua["machine_pos"][1], data_opcua["machine_pos"][3])
    # marginal_cost_1_2 = distance.euclidean(data_opcua["machine_pos"][1], data_opcua["robot_pos"][1])
    # marginal_cost_2_2 = distance.euclidean(data_opcua["machine_pos"][1], data_opcua["robot_pos"][2])
    # total_c1_2 = task_cost2 + marginal_cost_1_2
    # total_c2_2 = task_cost2 + marginal_cost_2_2
    #
    # print("Task (2,4)  robot 2", marginal_cost_1_2)
    # print("Task (2,4)  robot 3", marginal_cost_2_2)


    print(f"Distance between robot 2 and workstation 3:",
          distance.euclidean(data_opcua["machine_pos"][2], data_opcua["robot_pos"][1]))

    print(f"Distance between robot 3 and workstation 3:",
          distance.euclidean(data_opcua["machine_pos"][2], data_opcua["robot_pos"][2]))

    for pos in data_opcua["machine_pos"]:
        print(pos)
