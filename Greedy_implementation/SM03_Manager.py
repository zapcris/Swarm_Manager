import asyncio
import queue
import sys
import threading
from queue import Empty
from threading import Thread

from spinach import AsyncioWorkers

from Greedy_implementation.SM07_Robot_agent import Transfer_robot, Workstation_robot, data_opcua
from Greedy_implementation.SM05_Scheduler import Joint_Scheduler
from Greedy_implementation.SM04_Task_Planner import Task_PG, order
from Greedy_implementation.SM06_Task_allocation import Task_Allocation
from Greedy_implementation.SM02_opcua_client import start_opcua, main_function

#### initialize OPCUA client to communicate to Visual Components ###################


Events = {
        "brand": "Ford",
        "rob_execution": [False, False, False],
        "rob_mission": ["", "", ""],
        "rob_product": [[int,int],[int,int],[int,int]],
        "machine_status": [False for stat in range(10)],
        "machine_product": [[int,int] for product in range(10)],
        "elapsed_time": [int for et in range(10)],
        "Product_finished": []

}

Data_opcua = dict(data_opcua)


##### Start OPCUA Client Thread################

# x = Thread(target=start_opcua, args=(Data_opcua,))
# x.start()


### instantiate order and generation of task list to that order
test_order = Task_PG(order)
generate_task = test_order.task_list()
Product_task = generate_task[0]
Global_task = generate_task[1]
Task_Queue = generate_task[2]

# for i in Task_Queue:
#     print(i)
# print(Product_task)
#print(Global_task)





#########Initialization of Workstation robots###############################

W_robot = []
for i, (type,pt) in enumerate(zip(order["Wk_type"], order["Process_times"])):
    if type==1 or type==2:
        #print("create wk", i, pt, type)
        wr = Workstation_robot(i, pt, data_opcua)
        W_robot.append(wr)


########## Initialization of Carrier robots######################################################
T_robot = []
q_robot = []

for r in data_opcua["rob_busy"]:
    q = queue.Queue()
    q_robot.append(q)


for i , R in enumerate(data_opcua["rob_busy"]):
    #print(i+1, R)

    robot = Transfer_robot(id=i + 1, global_task=Global_task, data_opcua=data_opcua, tqueue=q_robot[i])
    T_robot.append(robot)


### Initialize Reactive Scheduler
GreedyScheduler = Joint_Scheduler(order, Global_task, Product_task, data_opcua, T_robot)

## Initialize Task Allocator
Greedy_Allocator = Task_Allocation(Global_task, data_opcua, T_robot)



### Perform task creation and allocation process
initial_task = GreedyScheduler.initialize_production()

alloted_task = Greedy_Allocator.step_allocation(initial_task)

for aalt in alloted_task:
    #print(aalt["id"],aalt["robot"])
    print(aalt)



####### Task queue functions #############

q_main_to_releaser = queue.Queue()
#q_to_eventloop = queue.Queue()

for task in alloted_task:
    q_main_to_releaser.put_nowait(task)

#print(q_main_to_releaser)




def release_function():

        global Sim_step
        Sim_step = 0
        print("Simulation step initialized to 0")
        while True:

            try:
                #asyncio.run(T_robot[1].unlatch_busy())


                if Sim_step == 0 :
                    task_opcua = q_main_to_releaser.get(False)
                    robot_id = task_opcua["robot"] - 1
                    print(task_opcua["robot"])
                    status = T_robot[robot_id].sendtoOPCUA(task_opcua)

                    #scheduling_queue.done()
                    # if task_opcua is None:
                    #     q_main_to_releaser.task_done()
                    #     break
                    q_main_to_releaser.task_done()
                    #asyncio.run(T_robot[robot_id].unlatch_busy())



                    print(f"All task completed on Simulation step {Sim_step} ")
                else:
                    normal_task = GreedyScheduler.normal_production()
                    normal_allot = Greedy_Allocator.step_allocation(normal_task)
                    for task in normal_allot:
                        q_main_to_releaser.put_nowait(task)
                    task_opcua = q_main_to_releaser.get(False)
                    robot_id = task_opcua["robot"] - 1
                    print(task_opcua["robot"])
                    status = T_robot[robot_id].sendtoOPCUA(task_opcua)
                    q_main_to_releaser.task_done()
                    print(f"All task completed on Simulation step {Sim_step} ")

            # Opt 1: Handle task here and call q.task_done()
            except Empty:
                # Handle empty queue here


                print("No task to release")
                for robot in data_opcua["rob_busy"]:
                    if robot == False:
                        Sim_step = 1
                        print(f"Simulation step upgraded to {Sim_step}")

                pass



##### Start Task releaser to Robot thread################

releaser_thread = Thread(target=release_function, args=(T_robot,))

releaser_thread.start()



##### running loop example ######
loop = asyncio.get_event_loop()
asyncio.ensure_future(T_robot[0].unlatch_busy(40))
asyncio.ensure_future(T_robot[1].unlatch_busy(20))
loop.run_forever()

threading.Thread(
    target=checker_function,
    args=(asyncio.get_event_loop(), loop)
).start()


# q_main_to_releaser.join()
# print('All work completed')



############################## Test debug function###########################################


#broadcast_bid(task_list)

# for t in task_list:
#     if t["id"] == 1 or t["id"] == 2 :
#         t.assign(robot="one")
#         t.cstatus(status="Executing")
#         print(t)
#     else:
#         t.deassign(robot="None")
#         print(t)



##### injecting async function to a thread #######

# async def main():
#     # create classes and call methods here
#     await asyncio.gather(  # waits for both of the arguments to return
#         asyncio.create_task(T_robot[0].unlatch_busy(20)),
#         asyncio.create_task(T_robot[1].unlatch_busy(20)),
#         asyncio.create_task(T_robot[2].unlatch_busy(20)),  # schedules first to run independently under asyncio.
#         asyncio.to_thread(release_function),  # runs second in thread
#     )
#
# asyncio.run(main())


