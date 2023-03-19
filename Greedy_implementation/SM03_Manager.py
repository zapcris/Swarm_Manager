import asyncio
import queue
import sys
import tracemalloc
from threading import Thread
from Greedy_implementation.SM02_opcua_client import start_opcua
from Greedy_implementation.SM06_Task_allocation import Task_Allocator_agent
from Greedy_implementation.SM07_Robot_agent import data_opcua, Workstation_robot, W_robot, null_product, Transfer_robot, \
    T_robot, Global_task, GreedyScheduler, Events, event1_exectime, event2_exectime, event3_exectime, event1_opcua, \
    event2_opcua, event3_opcua, \
    wk_1, wk_2, wk_3, wk_4, wk_5, wk_6, wk_7, wk_8, wk_9, wk_10, event1_chk_exec, event2_chk_exec, event3_chk_exec, \
    q_robot_to_opcua, \
    event1_pth_clr, event2_pth_clr, event3_pth_clr, p1, p3, p2, test_product, test_task, q_product_done, \
    wk_process_event, wk_proc_event, q_main_to_releaser, production_order


def task_released(task,loop):
    id = task["robot"] - 1
    print("Triggered robot id is:", id+1 )
    if id == 0 and data_opcua["rob_busy"][0]:
        loop.call_soon_threadsafe(event1_exectime.set)
        print("Triggered event is 1 for robot 1")
    elif id == 1 and data_opcua["rob_busy"][1]:
        loop.call_soon_threadsafe(event2_exectime.set)
        print("Triggered event is 1 for robot 2 ")
    elif id == 2 and data_opcua["rob_busy"][2]:
        loop.call_soon_threadsafe(event3_exectime.set)
        print("Triggered event is 1 for robot 3")

def opcua_cmd_event(task,loop):
    id = task.robot
    print("Triggered opcua robot id is:", id)
    if id == 1 and T_robot[id-1].exec_cmd == True:
        loop.call_soon_threadsafe(event1_chk_exec.set)
        print("Triggered event is 1 for robot 1")
    elif id == 2 and T_robot[id-1].exec_cmd == True:
        loop.call_soon_threadsafe(event2_chk_exec.set)
        print("Triggered event is 1 for robot 2")
    elif id == 3 and T_robot[id-1].exec_cmd == True:
        loop.call_soon_threadsafe(event3_chk_exec.set)
        print("Triggered event is 1 for robot 3")


# async def path_clear_event(event1, event2, event3):
#     if T_robot[0].exec_cmd == True and T_robot[0].path_clear == True:
#         loop.call_soon_threadsafe(event1.set)
#
#     elif T_robot[1].exec_cmd == True and T_robot[1].path_clear == True:
#         loop.call_soon_threadsafe(event2.set)
#
#     elif T_robot[2].exec_cmd == True and T_robot[2].path_clear == True:
#         loop.call_soon_threadsafe(event3.set)









def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def release_task_execution(loop):
    global Sim_step
    Sim_step = 0
    print("Simulation step initialized to 0")
    while True:
        try:

            if Sim_step < 20:
                await asyncio.sleep(3)
                task_opcua = q_main_to_releaser.get_nowait()
                robot_id = task_opcua["robot"] - 1
                print(task_opcua["robot"])
                # await T_robot[robot_id].sendtoOPCUA(task=task_opcua)
                a = True
                await asyncio.sleep(1)
                T_robot[robot_id].trigger_task(task=task_opcua, execute=a)
                opcua_cmd_event(task=task_opcua, loop=loop)
                print(f"Task released to robot {robot_id + 1}")

                q_main_to_releaser.task_done()
                # done()
                print("Execution task release", task_opcua)

                Sim_step += 1
                print(f"Simulation step incremented to {Sim_step}")











        # Opt 1: Handle task here and call q.task_done()
        except:
            # Handle empty queue here

            # print("Task Queue emptied")
            # for robot in T_robot:
            #     if robot.finished_product != null_product:
            #         f_p = robot.finished_product
            #         fin_prod.append(f_p)
            #         print(f"product added to finished list")
            #         robot.clr_fin_prod()
            # if fin_prod:
            #     new_allotment = GreedyScheduler.prod_completed(fin_prod)
            #     alloted_new_task = Greedy_Allocator.step_allocation(new_allotment[0], new_allotment[1])
            #     fin_prod.clear()
            #     for task in alloted_new_task[0]:
            #         print(f"tasks entered in the queue:", task)
            #         q_main_to_releaser.put_nowait(task)
            # else:
            #     pass

            ## Not working code #######

            # for i, wk in enumerate(W_robot):
            #     if wk.done_product != null_product:
            #         d_p = wk.done_product
            #         done_prod.append(d_p)
            #         print(f"Executed product added to done list and for Task Allocation")
            #         wk.done_product = null_product

            # if not q_product_done.empty():
            #     done_prod = q_product_done.get_nowait()
            #     normal_allotment = GreedyScheduler.normalized_production(done_prod)
            #     alloted_normal_task = Greedy_Allocator.step_allocation(normal_allotment[0], normal_allotment[1])
            #     for task in alloted_normal_task[0]:
            #          print(f"tasks entered in the queue:", task)
            #          q_main_to_releaser.put_nowait(task)
            #          print("Task released to Main Releaser")
            #          q_product_done.task_done()
            #
            # else:
            #     pass






            pass


def main_release(loop):
    asyncio.run(release_task_execution(loop))


async def release_done_products():
    while True:
        try:


            done_prod = q_product_done.get_nowait()
            ###print("product retrieved from queue",done_prod)
            normal_allotment = GreedyScheduler.normalized_production(done_prod)
            ###print("normal allotment", normal_allotment)
            alloted_normal_task = Greedy_Allocator.step_allocation(normal_allotment[0], normal_allotment[1])
            for task in alloted_normal_task[0]:
                print(f"tasks entered in the queue:", task)
                q_main_to_releaser.put_nowait(task)
                print("Task released to Main Releaser")
                q_product_done.task_done()
        except:
            # await asyncio.sleep(10)
            # q_product_done.put_nowait(p1)
            # await asyncio.sleep(5)
            # print("Queue empty")
            # q_product_done.put_nowait(p1)
            # print("task added")
            pass


def done_release():
    asyncio.run(release_done_products())

def insert_opc_queue(data):
    q_robot_to_opcua.put_nowait(data)
    print(f"Task entered into the queue")

async def release_opcua_cmd(loop):
    while True:
        try:
            data = q_robot_to_opcua.get_nowait()
            task = data[0]
            id = data[1]
            cmd = ["" for _ in range(len(T_robot))]
            print(f"Task {task} received from Swarm Manager for robot {id} for execution")
            await asyncio.sleep(1)
            if task.command[1] == 12:
                c = str("s") + "," + str(task.command[0])
            else:
                c = str(task.command[0]) + "," + str(task.command[1])
            cmd.insert((int(id) - 1), c)

            if task.command[0] == 11:
                # sleep(3)
                data_opcua["create_part"] = task.pV
                # write_opcua(task["pV"], "create_part", None)
                await asyncio.sleep(0.7)
                print(f"part created for robot {id},", task.pV)
                data_opcua["create_part"] = 0
                await asyncio.sleep(0.7)
                data_opcua["mobile_manipulator"] = cmd
                await asyncio.sleep(0.7)
                data_opcua["mobile_manipulator"] = ["", "", ""]
                print("command sent to opcuaclient", cmd)
                await asyncio.sleep(0.5)
                W_robot[task.command[1] - 1].booked = True
                await asyncio.sleep(5)

            else:
                data_opcua["mobile_manipulator"] = cmd
                await asyncio.sleep(0.7)
                data_opcua["mobile_manipulator"] = ["", "", ""]
                print("command sent to opcuaclient", cmd)
                W_robot[task.command[0] - 1].product_clearance()
                print(f"Workstation {task.command[0]} is Product FREE")
                await asyncio.sleep(0.5)
                #W_robot[task.command[1] - 1].product_free = False
                #W_robot[task.command[1] - 1].robot_free = False
                W_robot[task.command[1] - 1].booked = True
                print(f"Workstation {task.command[1]} is BOOKED")

                # print(f"robot {self.id} busy status is ", data_opcua["rob_busy"][self.id-1])
                ### wait for robot busy flag status to update###
                await asyncio.sleep(3)
                Events["rob_execution"][id - 1] = True
                #T_robot[id - 1].exec_cmd = False

            q_robot_to_opcua.task_done()
            task_released(task=task, loop=loop)
            print("Event Status", Events["rob_execution"])





        except:
            # Handle empty queue here

            # print("Task Queue emptied")
            pass


def opcua_release(loop):
    asyncio.run(release_opcua_cmd(loop))


async def concurrent_tasks(loop):
    """Fetch all urls from the list of urls

    It is done concurrently and combined into a single coroutine"""

    # results = await asyncio.gather(
    # *tasks
    loop.create_task(T_robot[0].execution_time(event=event1_exectime, loop=loop))
    loop.create_task(T_robot[1].execution_time(event=event2_exectime, loop=loop))
    loop.create_task(T_robot[2].execution_time(event=event3_exectime, loop=loop))
    loop.create_task(T_robot[0].sendtoOPCUA(event_fromchkpath=event1_pth_clr))
    loop.create_task(T_robot[1].sendtoOPCUA(event_fromchkpath=event2_pth_clr))
    loop.create_task(T_robot[2].sendtoOPCUA(event_fromchkpath=event3_pth_clr))
    loop.create_task(W_robot[0].process_execution(event=wk_1))
    loop.create_task(W_robot[1].process_execution(event=wk_2))
    loop.create_task(W_robot[2].process_execution(event=wk_3))
    loop.create_task(W_robot[3].process_execution(event=wk_4))
    loop.create_task(W_robot[4].process_execution(event=wk_5))
    loop.create_task(W_robot[5].process_execution(event=wk_6))
    loop.create_task(W_robot[6].process_execution(event=wk_7))
    loop.create_task(W_robot[7].process_execution(event=wk_8))
    loop.create_task(W_robot[8].process_execution(event=wk_9))
    loop.create_task(W_robot[9].process_execution(event=wk_10))
    loop.create_task(T_robot[0].check_path_clear(event_frommain=event1_chk_exec, event_toopcua=event1_pth_clr))
    loop.create_task(T_robot[1].check_path_clear(event_frommain=event2_chk_exec, event_toopcua=event2_pth_clr))
    loop.create_task(T_robot[2].check_path_clear(event_frommain=event3_chk_exec, event_toopcua=event3_pth_clr))

    ### Unused task functions########
    # loop.create_task(main_function(data_opcua))
    # loop.create_task(release_task_execution(loop))
    # loop.create_task(release_done_products())
    # loop.create_task(release_opcua_cmd(loop))
    #loop.create_task(T_robot[0].check_rob_done(event=event1, event_opcua=event1_opcua))
    #loop.create_task(T_robot[1].check_rob_done(event=event2, event_opcua=event2_opcua))
    #loop.create_task(T_robot[2].check_rob_done(event=event3, event_opcua=event3_opcua))






        # )
        # print(results)



####### Main Thread ######


if __name__ == "__main__":
    tracemalloc.start()
    fin_prod = []
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    #########Initialization of Workstation robots###############################
    sink_station = Workstation_robot(wk_no=12, order=production_order, product=null_product)
    source_station = Workstation_robot(wk_no=11, order=production_order, product=null_product)
    for i, type in enumerate(production_order["Wk_type"]):
        if type == 1 or type == 2:
            # print("create wk", i, pt, type)
            wr = Workstation_robot(wk_no=i, order=production_order, product=null_product)
            W_robot.append(wr)
    W_robot.append(source_station)
    W_robot.append(sink_station)

    ########## Initialization of Carrier robots######################################################
    q_robot = []
    for r in data_opcua["rob_busy"]:
        q = queue.Queue()
        q_robot.append(q)
    for i, R in enumerate(data_opcua["rob_busy"]):
        # print(i+1, R)
        robot = Transfer_robot(id=i + 1, global_task=Global_task, product=None, tqueue=q_robot[i])
        T_robot.append(robot)


    ##### Initialize Task Allocator agent #########
    Greedy_Allocator = Task_Allocator_agent()

    ### Perform task creation and allocation process
    initial_allotment = GreedyScheduler.initialize_production()
    alloted_initial_task = Greedy_Allocator.step_allocation(initial_allotment[0], initial_allotment[1])

    ###### Task queue functions #############

    for task in alloted_initial_task[0]:
        print(f"tasks in the queue:", task)
        q_main_to_releaser.put_nowait(task)
    # GreedyScheduler.active_products = test_product
    # q_product_done.put_nowait([p1])


    ##### Start OPCUA Client Thread################
    opcua_client = Thread(target=start_opcua, daemon=True, args=(data_opcua,))
    opcua_client.start()

    ##### Start Task Release Thread################
    task_releaser_thread = Thread(target=main_release, daemon=True, args=(loop, ))
    task_releaser_thread.start()
    ##### Start OPCUA Command Thread################
    opcuacmd_thread = Thread(target=opcua_release, daemon=True, args=(loop, ))
    opcuacmd_thread.start()
    ##### Start done product Thread################
    done_product_thread = Thread(target=done_release, daemon=True)
    done_product_thread.start()

    try:
        # with concurrent.futures.ThreadPoolExecutor() as pool:
        #     result = await loop.run_in_executor(
        #         pool, blocking_io)
        #     print('custom thread pool', result)

        #asyncio.ensure_future(main(), loop=loop)
        asyncio.run(concurrent_tasks(loop), debug=True)
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()












# async def release_task_execution():
#     global Sim_step
#     Sim_step = 0
#     print("Simulation step initialized to 0")
#     while True:
#         try:
#
#             if Sim_step <= 3:
#                 await asyncio.sleep(3)
#                 task_opcua = q_main_to_releaser.get_nowait()
#                 robot_id = task_opcua["robot"] - 1
#                 print(task_opcua["robot"])
#                 # await T_robot[robot_id].sendtoOPCUA(task=task_opcua)
#                 a = True
#                 await asyncio.sleep(3)
#                 T_robot[robot_id].trigger_task(task=task_opcua, execute=a)
#                 opcua_cmd_event(task=task_opcua)
#                 print(f"Task released to robot {robot_id + 1}")
#
#                 q_main_to_releaser.task_done()
#                 # done()
#                 # print("Execution task release", task_opcua)
#
#                 Sim_step += 1
#                 print(f"Simulation step incremented to {Sim_step}")
#
#
#
#
#         # Opt 1: Handle task here and call q.task_done()
#         except:
#             # Handle empty queue here
#
#             # print("Task Queue emptied")
#             for robot in T_robot:
#                 if robot.finished_product != null_product:
#                     f_p = robot.finished_product
#                     fin_prod.append(f_p)
#                     print(f"product added to finished list")
#                     robot.clr_fin_prod()
#             if fin_prod:
#                 new_allotment = GreedyScheduler.prod_completed(fin_prod)
#                 alloted_new_task = Greedy_Allocator.step_allocation(new_allotment[0], new_allotment[1])
#                 fin_prod.clear()
#                 for task in alloted_new_task[0]:
#                     print(f"tasks entered in the queue:", task)
#                     q_main_to_releaser.put_nowait(task)
#             else:
#                 pass
#
#             for i, wk in enumerate(W_robot):
#                 if wk.done_product.robot != 0:
#                     d_p = wk.done_product
#                     done_prod.append(d_p)
#                     print(f"product added to done list and for Task Allocation")
#                     wk.clr_done_prod()
#             if done_prod:
#                 normal_allotment = GreedyScheduler.normalized_production(done_prod)
#                 alloted_normal_task = Greedy_Allocator.step_allocation(normal_allotment[0], normal_allotment[1])
#                 done_prod.clear()
#                 for task in alloted_normal_task[0]:
#                     print(f"tasks entered in the queue:", task)
#                     q_main_to_releaser.put_nowait(task)
#             else:
#                 pass
#
#             pass
#
#
# def main_release():
#     asyncio.run(release_task_execution())
#
#
# releaser_thread = Thread(target=main_release, daemon=True)
#
# releaser_thread.start()
#
# def insert_opc_queue(data):
#     q_robot_to_opcua.put_nowait(data)
#     print(f"Task entered into the queue")
#
# async def release_opcua_cmd():
#     while True:
#         try:
#             data = q_robot_to_opcua.get_nowait()
#             task = data[0]
#             id = data[1]
#             cmd = ["" for _ in range(2)]
#             print(f"Task {task} received from Swarm Manager for robot {id} for execution")
#             await asyncio.sleep(1)
#             if task.command[1] == 12:
#                 c = str(task.command[0]) + "," + str("s")
#             else:
#                 c = str(task.command[0]) + "," + str(task.command[1])
#             cmd.insert((int(id) - 1), c)
#
#             if task.command[0] == 11:
#                 # sleep(3)
#                 data_opcua["create_part"] = task.pV
#                 # write_opcua(task["pV"], "create_part", None)
#                 await asyncio.sleep(0.7)
#                 print(f"part created for robot {id},", task.pV)
#                 data_opcua["create_part"] = 0
#                 await asyncio.sleep(0.7)
#                 data_opcua["mobile_manipulator"] = cmd
#                 await asyncio.sleep(0.7)
#                 data_opcua["mobile_manipulator"] = ["", "", ""]
#                 print("command sent to opcuaclient", cmd)
#
#             else:
#
#                 data_opcua["mobile_manipulator"] = cmd
#                 await asyncio.sleep(0.7)
#                 data_opcua["mobile_manipulator"] = ["", "", ""]
#                 W_robot[task.command[0] - 1].product_clearance()
#                 # print(f"robot {self.id} busy status is ", data_opcua["rob_busy"][self.id-1])
#                 Events["rob_execution"][id - 1] = True
#                 #T_robot[id - 1].exec_cmd = False
#
#             q_robot_to_opcua.task_done()
#             task_released(task=task)
#             print("Event Status", Events["rob_execution"])
#             await asyncio.sleep(7)
#
#
#
#
#         except:
#             # Handle empty queue here
#
#             # print("Task Queue emptied")
#             pass
#
#
# def opcua_release():
#     asyncio.run(release_opcua_cmd())
#
#
# opcuacmd_thread = Thread(target=opcua_release, daemon=True)
#
# opcuacmd_thread.start()
#
# sys.exit()
# ### new Events check thread ####
#
# async def main():
#     """Fetch all urls from the list of urls
#
#     It is done concurrently and combined into a single coroutine"""
#
#     results = await asyncio.gather(
#         # *tasks
#         (T_robot[0].execution_time(event=event1, event2=event1_opcua)),
#         (T_robot[1].execution_time(event=event2, event2=event2_opcua)),
#         (T_robot[2].execution_time(event=event3, event2=event3_opcua)),
#         (T_robot[0].check_rob_done(event=event1, event_opcua=event1_opcua)),
#         (T_robot[1].check_rob_done(event=event2, event_opcua=event2_opcua)),
#         (T_robot[2].check_rob_done(event=event3, event_opcua=event3_opcua)),
#         (T_robot[0].sendtoOPCUA(event=event1_1)),
#         (T_robot[1].sendtoOPCUA(event=event2_1)),
#         (T_robot[2].sendtoOPCUA(event=event3_1)),
#         (W_robot[0].process_execution(event=wk_1)),
#         (W_robot[1].process_execution(event=wk_2)),
#         (W_robot[2].process_execution(event=wk_3)),
#         (W_robot[3].process_execution(event=wk_4)),
#         (W_robot[4].process_execution(event=wk_5)),
#         (W_robot[5].process_execution(event=wk_6)),
#         (W_robot[6].process_execution(event=wk_7)),
#         (W_robot[7].process_execution(event=wk_8)),
#         (W_robot[8].process_execution(event=wk_9)),
#         (W_robot[9].process_execution(event=wk_10))
#
#     )
#     print(results)
#
#
# ####### Event loop runs in main thread######
#
# try:
#     asyncio.ensure_future(main())
#
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
# finally:
#     print("Closing Loop")
#     loop.close()



