import asyncio
import queue
import time
import tracemalloc
from threading import Thread
from Reactive_majorversion2.SM02_opcua_client import start_opcua
from Reactive_majorversion2.SM05_Scheduler_agent import app_close
from Reactive_majorversion2.SM06_Task_allocation import Task_Allocator_agent
from Reactive_majorversion2.SM07_Robot_agent import data_opcua, Workstation_robot, W_robot, null_product, \
    Transfer_robot, \
    T_robot, Global_task, GreedyScheduler, Events, event1_exectime, event2_exectime, event3_exectime, wk_1, wk_2, wk_3, wk_4, wk_5, wk_6, wk_7, wk_8, wk_9, wk_10, event1_chk_exec, event2_chk_exec, event3_chk_exec, \
    q_robot_to_opcua, \
    event1_pth_clr, event2_pth_clr, event3_pth_clr, q_product_done, \
    q_main_to_releaser, production_order, q_task_wait, Ax_station, \
    Auxillary_station, opcua_cmd_event


def reconfigure_topology():
    # reconfig = "-5947.8017408,1345.07016512d-5891.42134789,3066.44623999d-5801.59637732,4823.26974015d"
    reconfig = "0,0d10000,6000d0,12000d0,18000d20000,24000d0,30000d30000,36000d0,42000d0,48000d0,54000d0,60000d"
    data_opcua["reconfiguration_machine_pos"] = reconfig
    time.sleep(0.5)
    data_opcua["do_reconfiguration"] = True
    time.sleep(1)
    data_opcua["do_reconfiguration"] = False


def task_released(robot_id, loop):
    # id = robot_id - 1
    # print("Triggered robot id is:", id + 1)
    if robot_id == 1 and data_opcua["rob_busy"][0]:
        loop.call_soon_threadsafe(event1_exectime.set)
        print("Triggered execution_timer event for robot 1")
    elif robot_id == 2 and data_opcua["rob_busy"][1]:
        loop.call_soon_threadsafe(event2_exectime.set)
        print("Triggered execution_timer event for robot 2 ")
    elif robot_id == 3 and data_opcua["rob_busy"][2]:
        loop.call_soon_threadsafe(event3_exectime.set)
        print("Triggered execution_timer event for robot 3")


def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def release_task_execution(loop):
    global Sim_step
    Sim_step = 0
    print("Simulation step initialized to 0")
    while True:
        try:

            if Sim_step < 100:
                if Sim_step == 0:
                    t = 15
                elif Sim_step > 0:
                    t = 3
                await asyncio.sleep(t)
                task_opcua = q_main_to_releaser.get_nowait()
                robot_id = task_opcua["robot"]
                print(task_opcua["robot"])
                # await T_robot[robot_id].sendtoOPCUA(task=task_opcua)
                # a = True
                await asyncio.sleep(1)
                T_robot[robot_id - 1].trigger_task(task=task_opcua)
                opcua_cmd_event(id=robot_id, loop=loop)
                print(f"Task released to robot {robot_id}")

                q_main_to_releaser.task_done()
                # done()
                print("Execution task release", task_opcua)

                Sim_step += 1
                print(f"Simulation step incremented to {Sim_step}")



        # Opt 1: Handle task here and call q.task_done()
        except:

            pass


def main_release(loop):
    asyncio.run(release_task_execution(loop))


async def task_wait_queue():
    while True:
        try:
            awaited_task = q_task_wait.get_nowait()
            print("Task found in the waiting queue", awaited_task[0])
            # await asyncio.sleep(10)
            wait_alloted_task = Greedy_Allocator.normal_allocation(awaited_task[0], awaited_task[1])
            # for task, product in zip(wait_alloted_task[0], wait_alloted_task[1]):
            if wait_alloted_task[0].allocation == True:
                print(f"task alloted while in the waiting queue:", wait_alloted_task[0])
                q_main_to_releaser.put_nowait(wait_alloted_task[0])
                print("Task released to Main Releaser")
                q_product_done.task_done()
            elif wait_alloted_task[0].allocation == False:
                print("Task again queued in waiting list")
                await asyncio.sleep(10)
                q_task_wait.put_nowait([wait_alloted_task[0], wait_alloted_task[1]])

        except:

            pass


def task_wait():
    asyncio.run(task_wait_queue())


async def release_products():
    while True:
        try:

            done_prod = q_product_done.get_nowait()
            # print("product retrieved from queue",done_prod)
            normal_allotment = GreedyScheduler.normalized_production(done_prod)
            # print("normal allotment", normal_allotment)
            # print("Allocation Started for task", normal_allotment[0])
            alloted_normal_task = Greedy_Allocator.normal_allocation(normal_allotment[0], normal_allotment[1])
            # print("alloted normal task", alloted_normal_task)

            # for task, product in zip(alloted_normal_task[0], alloted_normal_task[1]):
            if alloted_normal_task[0].allocation == True:
                print(f"tasks entered in the queue:", alloted_normal_task[0])
                q_main_to_releaser.put_nowait(alloted_normal_task[0])
                print("Task released to Main Releaser")
                q_product_done.task_done()
            elif alloted_normal_task[0].allocation == False:
                print("Task again queued in waiting list")
                await asyncio.sleep(10)
                q_task_wait.put_nowait([alloted_normal_task[0], alloted_normal_task[1]])
                print("Task queued in waiting list")


        except:

            pass


def done_release():
    asyncio.run(release_products())


def insert_opc_queue(data):
    q_robot_to_opcua.put_nowait(data)
    print(f"Task entered into the queue")


async def bg_tsk(flag):
    await asyncio.sleep(3)
    flag.set()


async def release_opcua_cmd(loop):
    while True:
        try:
            data = q_robot_to_opcua.get_nowait()
            sub_task = data[0]
            target = int(sub_task[1])
            id = data[1]
            product = data[2]
            cmd = ["" for _ in range(3)]
            print(f"Task {sub_task} received from Swarm Manager for robot {id} for execution")
            # await asyncio.sleep(1)
            match sub_task[0]:
                case 'pick':
                    # print("case1 activated")
                    c = "a" + "," + sub_task[1]
                    cmd.insert((int(id) - 1), c)
                    # print("command to opcua", cmd)
                    # print("id", id)
                    # print("target station", sub_task[1])
                    # print("part to be created", product)
                    if 10 <= target <= 19:
                        flag = asyncio.Event()
                        data_opcua["create_part"] = product
                        # write_opcua(task["pV"], "create_part", None)
                        await asyncio.sleep(3)
                        # "Test code for stopping over creation of product at base"
                        # while data_opcua["create_part"] == product and data_opcua["create_part"] > 0:
                        #     #await asyncio.sleep(2)
                        #     if data_opcua["recive_part"] == True :
                        #         print(f"Product{product} command received by Visual Component")
                        #         print(f"Part create command received by Visual Components", data_opcua["recive_part"])
                        #         break
                        #     else:
                        #         continue

                        #asyncio.create_task(bg_tsk(flag))
                        data_opcua["create_part"] = 0
                        data_opcua["recive_part"] = False
                        print(f"product {product} created for robot {id}")
                        # Ax_station[target-10].booked = True
                        await asyncio.sleep(0.5)

                case "q1":
                    endpoint = str(target + 20)
                    c = "n" + "," + endpoint
                    cmd.insert((int(id) - 1), c)
                case "q2":
                    endpoint = str(target + 30)
                    c = "n" + "," + endpoint
                    cmd.insert((int(id) - 1), c)
                case "drop":
                    c = "b" + "," + sub_task[1]
                    cmd.insert((int(id) - 1), c)
                case "sink":
                    c = "s" + "," + sub_task[1]
                    cmd.insert((int(id) - 1), c)
                    # Ax_station[10].booked = True
                case "base":
                    y_pos = -1700 + ((id - 1) * 5000)
                    c = "m" + "," + "-10662" + "," + str(y_pos) + "," + "0"
                    cmd.insert((int(id) - 1), c)

            data_opcua["mobile_manipulator"] = cmd
            #await asyncio.sleep(3)
            "Wait for rob_busy"
            while data_opcua["mobile_manipulator"] == cmd:
            # await asyncio.sleep(0)
                if data_opcua["rob_busy"][id-1] == True:
                    print(f"Task{cmd} received by Robot {id-1}")
                    break
                else:
                    continue
            data_opcua["mobile_manipulator"] = ['', '', '']
            print("command sent to opcuaclient", cmd)
            # await asyncio.sleep(1)
            # W_robot[task.command[1] - 1].booked = True
            # W_robot[10].product_clearance()
            # await asyncio.sleep(2)
            # W_robot[target].product_clearance()
            # W_robot[target].booked = True
            q_robot_to_opcua.task_done()
            task_released(robot_id=id, loop=loop)
            print("Event Status", Events["rob_execution"])



        except:
            # Handle empty queue here

            # print("Task Queue emptied")
            pass


def opcua_release(loop):
    asyncio.run(release_opcua_cmd(loop))


def close_application():
    print("Closing Loop")
    loop.close()
    opcua_client.join()
    task_releaser_thread.join()
    opcuacmd_thread.join()
    done_product_thread.join()


async def concurrent_tasks(loop):
    """Fetch all urls from the list of urls

    It is done concurrently and combined into a single coroutine"""

    # results = await asyncio.gather(
    # *tasks
    loop.create_task(T_robot[0].initiate_task(event_frommain=event1_chk_exec, event_toopcua=event1_pth_clr))
    loop.create_task(T_robot[1].initiate_task(event_frommain=event2_chk_exec, event_toopcua=event2_pth_clr))
    loop.create_task(T_robot[2].initiate_task(event_frommain=event3_chk_exec, event_toopcua=event3_pth_clr))
    loop.create_task(T_robot[0].sendtoOPCUA(event_fromchkpath=event1_pth_clr))
    loop.create_task(T_robot[1].sendtoOPCUA(event_fromchkpath=event2_pth_clr))
    loop.create_task(T_robot[2].sendtoOPCUA(event_fromchkpath=event3_pth_clr))
    loop.create_task(T_robot[0].execution_timer(event_main=event1_exectime, event_init_task=event1_chk_exec, loop=loop))
    loop.create_task(T_robot[1].execution_timer(event_main=event2_exectime, event_init_task=event2_chk_exec, loop=loop))
    loop.create_task(T_robot[2].execution_timer(event_main=event3_exectime, event_init_task=event3_chk_exec, loop=loop))
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

    # )
    # print(results)


####### Main Thread ######


if __name__ == "__main__":
    tracemalloc.start()
    fin_prod = []
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    ##### Initialization of auxiliary stations#######
    for i in range(10):
        source = Auxillary_station(stn_no=i + 10, order=production_order, product=null_product)
        Ax_station.append(source)
    sink_station = Auxillary_station(stn_no=40, order=production_order, product=null_product)
    Ax_station.append(sink_station)

    #########Initialization of Workstation robots###############################
    ##### Start OPCUA Client Thread################
    opcua_client = Thread(target=start_opcua, args=(data_opcua,))
    opcua_client.start()

    while (True):
        time.sleep(2)
        print("Awaiting data from Visual Components")
        # print(data_opcua["machine_pos"])
        # print(data_opcua["robot_pos"])
        if data_opcua["machine_pos"][0] != [0, 0]:
            global_wk_pos = data_opcua["machine_pos"]
            break

    print("The values of workstation positions are", data_opcua["machine_pos"])

    for i, type in enumerate(production_order["Wk_type"]):
        if type == 1 or type == 2:
            # print("create wk", i, pt, type)
            wr = Workstation_robot(wk_no=i + 1, order=production_order, product=null_product)
            W_robot.append(wr)
    # W_robot.append(source_station)
    # W_robot.append(sink_station)
    #W_robot[0].booked = True
    ########## Initialization of Carrier robots######################################################
    q_robot = []
    # for r in data_opcua["rob_busy"]:
    for r in range(3):
        q = queue.Queue()
        q_robot.append(q)
    # for i, R in enumerate(data_opcua["rob_busy"]):
    for i in range(3):
        # print(i+1, R)
        robot = Transfer_robot(id=i + 1, global_task=Global_task, product=None, tqueue=q_robot[i],
                               machine_pos=global_wk_pos)
        T_robot.append(robot)

    ##### Initialize Task Allocator agent #########
    Greedy_Allocator = Task_Allocator_agent()

    ### Perform task creation and allocation process
    initial_allotment = GreedyScheduler.initialize_production()
    alloted_initial_task = Greedy_Allocator.step_allocation(initial_allotment[0], initial_allotment[1])

    ##### Start Task Release Thread################
    task_releaser_thread = Thread(target=main_release, daemon=True, args=(loop,))
    task_releaser_thread.start()
    ##### Task waiting Thread ################
    task_waiting_thread = Thread(target=task_wait, daemon=True)
    task_waiting_thread.start()
    ##### Start OPCUA Command Thread################
    opcuacmd_thread = Thread(target=opcua_release, daemon=True, args=(loop,))
    opcuacmd_thread.start()
    ##### Start done product Thread################
    done_product_thread = Thread(target=done_release, daemon=True)
    done_product_thread.start()

    ###### Task queue functions #############

    for task in alloted_initial_task[0]:
        print(f"tasks in the queue:", task)
        q_main_to_releaser.put_nowait(task)

    if app_close.is_set() == True:
        print("Closing Loop and Threads")
        loop.close()
        opcua_client.join()
        task_releaser_thread.join()
        opcuacmd_thread.join()
        done_product_thread.join()
        task_waiting_thread.join()

    try:
        # asyncio.ensure_future(main(), loop=loop)
        asyncio.run(concurrent_tasks(loop), debug=True)
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()
