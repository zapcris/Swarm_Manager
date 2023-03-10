import asyncio
import concurrent.futures
import queue
import sys
import tracemalloc

from queue import Empty
from threading import Thread

from Greedy_implementation.SM07_Robot_agent import Transfer_robot, Workstation_robot, data_opcua, Events, event1, \
    event2, event3, wk_1, wk_2, wk_3, wk_4, wk_5, wk_6, wk_7, wk_8, wk_9, wk_10, event1_opcua, event2_opcua, \
    event3_opcua
from Greedy_implementation.SM05_Scheduler import Joint_Scheduler
from Greedy_implementation.SM04_Task_Planner import Task_PG, order
from Greedy_implementation.SM06_Task_allocation import Task_Allocation
from Greedy_implementation.SM02_opcua_client import start_opcua


#### initialize OPCUA client to communicate to Visual Components ###################

tracemalloc.start()

Data_opcua = dict(data_opcua)


##### Start OPCUA Client Thread################
#
x = Thread(target=start_opcua, daemon=True, args=(data_opcua,))
x.start()


###########Initialization of Event Loop########################
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


### events flags for transfer and workstation robots#####




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



####### Task queue functions #############

q_main_to_releaser = asyncio.Queue()
#q_to_eventloop = queue.Queue()

for task in alloted_task:
    print(f"tasks in the queue:", task)
    q_main_to_releaser.put_nowait(task)

#print(q_main_to_releaser)




async def release_task_execution():

        global Sim_step
        Sim_step = 0
        print("Simulation step initialized to 0")
        while True:

            try:



                if Sim_step == 0 :
                    task_opcua = q_main_to_releaser.get_nowait()
                    robot_id = task_opcua["robot"] - 1
                    print(task_opcua["robot"])
                    await T_robot[robot_id].sendtoOPCUA(task_opcua)
                    print(f"Task released to robot {robot_id+1}")

                    q_main_to_releaser.task_done()
                    #done()
                    #print("Execution task release", task_opcua)
                    task_released(task=task_opcua)
                    print("Event Status", Events["rob_execution"])
                    await asyncio.sleep(5)




                elif Sim_step > 0 and Sim_step < 99 :
                    normal_task = GreedyScheduler.normal_production()
                    normal_allot = Greedy_Allocator.step_allocation(normal_task)
                    for task in normal_allot:
                        q_main_to_releaser.put_nowait(task)
                    task_opcua = q_main_to_releaser.get_nowait()
                    robot_id = task_opcua["robot"] - 1
                    print(task_opcua["robot"])

                    T_robot[robot_id].sendtoOPCUA(task_opcua)
                    q_main_to_releaser.task_done()
                    #print(f" Task completed on Simulation step {Sim_step} ")
                    #done()
                    #task_released(task=task_opcua)


            # Opt 1: Handle task here and call q.task_done()
            except:
                # Handle empty queue here



                print("No task to release")
                for robot in data_opcua["rob_busy"]:
                    if robot == False:
                        Sim_step = 99
                        print(f"Simulation step upgraded to {Sim_step}")

                pass


def main_release():
    asyncio.run(release_task_execution())

releaser_thread = Thread(target=main_release, daemon=True)

releaser_thread.start()


async def check_robot_status():
    while True:
        if event1 == True and data_opcua["rob_busy"][0] == False:
            event1_opcua.set()
            print("Event 2 (opcua) for Robot 1 acitivated")
        elif event2 == True and data_opcua["rob_busy"][1] == False:
            event2_opcua.set()
            print("Event 2 (opcua) for Robot 2 acitivated")
        elif event3 == True and data_opcua["rob_busy"][2] == False:
            event3_opcua.set()
            print("Event 2 (opcua) for Robot 3 acitivated")
        else:
            pass

def main_status():
    asyncio.run(check_robot_status())

# status_thread = Thread(target=main_status, daemon=True)
#
# status_thread.start()

### new Events check thread ####


def task_released(task):

    id = task["robot"] - 1
    print("Triggered robot id is:", id+1)
    if id == 0 and data_opcua["rob_busy"][0]:
        loop.call_soon_threadsafe(event1.set)
        print("Triggered event is 1 for robot 1")
    elif id == 1 and data_opcua["rob_busy"][1]:
        loop.call_soon_threadsafe(event2.set)
        print("Triggered event is 1 for robot 2 ")
    elif id == 2 and data_opcua["rob_busy"][2]:
        loop.call_soon_threadsafe(event3.set)
        print("Triggered event is 1 for robot 3")


async def check_event():
        while event1.is_set() or event2.is_set() or event3.is_set():
            if event1.is_set() and data_opcua["rob_busy"][0] == False:
                event1_opcua.set()
                print("Event 2 (opcua) for Robot 1 acitivated")
            elif event2.is_set() and data_opcua["rob_busy"][1] == False:
                event2_opcua.set()
                print("Event 2 (opcua) for Robot 2 acitivated")
            elif event3.is_set() and data_opcua["rob_busy"][2] == False:
                event3_opcua.set()
                print("Event 2 (opcua) for Robot 3 acitivated")
            else:
                pass


# async def execution_time(flag, id):
#
#     while True:
#         # print(f'waiting for robot {id} for  execution')
#         await flag.wait()
#         print(f'Robot {id} execution timer has started')
#         #await asyncio.sleep(3)
#         start_time = datetime.now()
#         Events["rob_execution"][id - 1] = True
#         while Events["rob_execution"][id - 1] == True:
#             if data_opcua["rob_busy"][id - 1] == True:
#                 # exec_time = (datetime.now() - start_time).total_seconds()
#                 # print(f"Robot {id} is running")
#                 pass
#             elif data_opcua["rob_busy"][id - 1] == False:
#                 Events["rob_execution"][id - 1] = False
#         exec_time = (datetime.now() - start_time).total_seconds()
#
#         flag.clear()
#
#         return print(f"Robot {id} took {exec_time:,.2f} seconds to run")
#
#
# async def process_execution(event, wk, product_pv):
#     process_time = order["Process_times"][product_pv][wk-1]
#     await event.wait()
#     print(f"Process task executing at workstation {wk}")
#     await asyncio.sleep(process_time)
#     print("Process task completed on workstation ",wk )
#     #prod_release()
#     event.clear()

async def main() :
    """Fetch all urls from the list of urls

    It is done concurrently and combined into a single coroutine"""
    # t1 = asyncio.ensure_future(release_task_execution())
    # t2 = asyncio.ensure_future((T_robot[0].execution_time(event1, 1)))
    # t3 = asyncio.ensure_future((T_robot[1].execution_time(event2, 2)))
    # t4 = asyncio.ensure_future((T_robot[2].execution_time(event3, 3)))

    # tasks = [t1, t2, t3, t4]
    results = await asyncio.gather(
        #*tasks
        (T_robot[0].execution_time(event1, 1, event1_opcua)),
        (T_robot[1].execution_time(event2, 2, event2_opcua)),
        (T_robot[2].execution_time(event3, 3, event3_opcua)),
        (T_robot[0].check_rob_done(event1, event1_opcua)),
        (T_robot[1].check_rob_done(event2, event2_opcua)),
        (T_robot[2].check_rob_done(event3, event3_opcua)),

        (process_execution(wk_1, 1, 1)),
        (process_execution(wk_2, 2, 1)),
        (process_execution(wk_3, 3, 1)),
        (process_execution(wk_4, 4, 1)),
        (process_execution(wk_5, 5, 1)),
        (process_execution(wk_6, 6, 1)),
        (process_execution(wk_7, 7, 1)),
        (process_execution(wk_8, 8, 1)),
        (process_execution(wk_9, 9, 1)),
        (process_execution(wk_10, 10, 1))
    )
    print(results)


####### Event loop runs in main thread######

try:
    asyncio.ensure_future(main())

    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()



##### END of Main Program ############






sys.exit()

# def event_loop() -> None:
#     global loop
#     loop = asyncio.new_event_loop()
#     t = Thread(target=event_background_loop, args=(loop,), daemon=True)
#     t.start()
#
#     asyncio.run_coroutine_threadsafe(main(), loop)
#
#
# if __name__ == "__main__":
#     event_loop()
#
#
# sys.exit()
#
# # loop = asyncio.new_event_loop()
# # asyncio.set_event_loop(loop)
# #
# # try:
# #     #asyncio.ensure_future(firstWorker())
# #     #asyncio.ensure_future(secondWorker())
# #     #asyncio.ensure_future(robot_exec_time())
# #     # asyncio.ensure_future(execution_time(event1, 1))
# #     # asyncio.ensure_future(execution_time(event2, 2))
# #     # asyncio.ensure_future(execution_time(event3, 3))
# #     # t1 = asyncio.create_task(execution_time(event1, 1))
# #     # t2 = asyncio.create_task(execution_time(event2, 2))
# #     # t3 = asyncio.create_task(execution_time(event3, 3))
# #     # tasks = [t1,t2,t3]
# #     # asyncio.gather(*tasks)
# #     #asyncio.run(main())
# #     asyncio.ensure_future(main())
# #     loop.run_forever()
# # except KeyboardInterrupt:
# #     pass
# # finally:
# #     print("Closing Loop")
# #     loop.close()
# #
# #
# #
# #
# #
# # sys.exit()
# #
# # thread_eloop = Thread(target=event_loop, daemon=True)
# # thread_eloop.start()
# #
# #
# #
# #
# #
# #
# # # #asyncio.create_task(T_robot[0].execution_time(event1))
# # # asyncio.create_task(foo(event1))
# # # print("Event status is: " ,Events["rob_execution"][0])
# # #
# # # if Events["rob_execution"][0] == True:
# # #     event1.set()
# # #     event1.clear()
# # #     print("Event is set true")
# #
# # try:
# #     asyncio.ensure_future(main1())
# #     #asyncio.ensure_future(secondWorker())
# #     loop.run_forever()
# # except KeyboardInterrupt:
# #     pass
# # finally:
# #     print("Closing Loop")
# #     loop.close()
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# # sys.exit()
# #
# # ######### Code for separate Event Loop Thread##########
# # def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
# #     asyncio.set_event_loop(loop)
# #     loop.run_forever()
# #
# #
# #
# #
# # async def fetch_all_robots(T_robot) :
# #     """Fetch all urls from the list of urls
# #
# #     It is done concurrently and combined into a single coroutine"""
# #
# #     condition = asyncio.Condition()
# #     event = asyncio.Event()
# #     events = [event for i in range(3)]
# #
# #     tasks = []
# #
# #
# #
# #     # for i, robot in enumerate(T_robot):
# #     #     #if Events["rob_execution"][i] == True:
# #     #     t3 = asyncio.create_task(T_robot[i].execution_time(condition))
# #     #     tasks.append(t3)
# #     #
# #     # for i, rob in enumerate(Events["rob_execution"]):
# #     #     if rob[i] == True:
# #     #         events[i].set()
# #
# #     t = asyncio.create_task(T_robot[0].execution_time(event))
# #
# #     tasks.append(t)
# #
# #
# #
# #     # async with condition:
# #     #     t = asyncio.create_task(T_robot[0].execution_time(condition=condition))
# #     #     tasks.append(t)
# #     #
# #     #     await condition.wait()
# #     results = await asyncio.gather(*tasks)
# #
# #     if Events["rob_execution"][0]==True:
# #         event.set()
# #         print("Event is set true")
# #
# #
# #
# #     return results
# #
# # ##### running loop example ######
# # loop = asyncio.new_event_loop()
# # t = Thread(target=start_background_loop, args=(loop,), daemon=True)
# # t.start()
# # #task = asyncio.run_coroutine_threadsafe(fetch_all_robots(), loop)
# #
# #
# # task = asyncio.run_coroutine_threadsafe(fetch_all_robots(T_robot), loop)
# #
# # # q_main_to_releaser.join()
# # # print('All work completed')
# #
# #
# #
# # ############################## Test debug function###########################################
# #
# #
# # #broadcast_bid(task_list)
# #
# # # for t in task_list:
# # #     if t["id"] == 1 or t["id"] == 2 :
# # #         t.assign(robot="one")
# # #         t.cstatus(status="Executing")
# # #         print(t)
# # #     else:
# # #         t.deassign(robot="None")
# # #         print(t)
# #
# #
# #
# # ##### injecting async function to a thread #######
# #
# # # async def main():
# # #     # create classes and call methods here
# # #     await asyncio.gather(  # waits for both of the arguments to return
# # #         asyncio.create_task(T_robot[0].unlatch_busy(20)),
# # #         asyncio.create_task(T_robot[1].unlatch_busy(20)),
# # #         asyncio.create_task(T_robot[2].unlatch_busy(20)),  # schedules first to run independently under asyncio.
# # #         asyncio.to_thread(release_function),  # runs second in thread
# # #     )
# # #
# # # asyncio.run(main())
# #
# #
