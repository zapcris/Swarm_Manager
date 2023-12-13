import asyncio
import itertools
import queue
import time
from multiprocessing import Process, Manager
from SM02_opcua_client import start_opcua
from Reactive_10Robots.SM04_Task_Planning_agent import Task_Planning_agent
from Reactive_10Robots.SM05_Scheduler_agent import Scheduling_agent
from Reactive_10Robots.SM06_Task_allocation import Task_Allocator_agent
from Reactive_10Robots.SM07_Robot_agent import production_order, Workstation_robot, null_product, Transfer_robot, \
    Auxillary_station




async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')


async def producer(queue: asyncio.Queue, queue2: asyncio.Queue):
    """producer emulator, creates ~ 10 tasks per second"""
    sleep_seconds = 1
    counter = itertools.count(1)
    run = 1
    i = 0
    while run == 1:
        await queue.put(next(counter))
        await queue2.put(next(counter))
        await asyncio.sleep(sleep_seconds)
        i += 1
        print(data_opcua)
        if i >= 20:
            run = 0
            print("Task Ended")
            # break


async def consumer(queue: asyncio.Queue, index, queue2: asyncio.Queue):
    """slow io-bound consumer emulator, process ~ 5 tasks per second"""
    sleep_seconds = 4
    while True:
        task = await queue.get()
        print(f"consumer={index}, task={task}, queue_size={queue.qsize()}")
        await asyncio.sleep(sleep_seconds)

        # await queue2.put(task)
        queue.task_done()


async def consumer2(queue: asyncio.Queue, index):
    """slow io-bound consumer emulator, process ~ 5 tasks per second"""

    sleep_seconds = 1
    while True:
        task = await queue.get()
        print(f"consumer2={index}, task2={task}, queue_size2={queue.qsize()}")
        # print(data_opcua)
        await asyncio.sleep(sleep_seconds)


async def release_products(q_done_product, q_task_waiting, q_mission_release):
    while True:
        done_prod = await q_done_product.get()
        # print(f"product PV={done_prod.pv_Id} and PI={done_prod.pi_Id} released from QUEUE")
        print("Done Processed Product", done_prod)
        normal_allotment = GreedyScheduler.normalized_production(done_prod)
        # print("normal allotment", normal_allotment)
        # print("Allocation Started for task", normal_allotment[0])
        alloted_normal_task = Greedy_Allocator.normal_allocation(normal_allotment[0], normal_allotment[1],
                                                                 T_robot=T_robot, data_opcua=data_opcua)
        # print("alloted normal task", alloted_normal_task)

        # for task, product in zip(alloted_normal_task[0], alloted_normal_task[1]):
        if alloted_normal_task[0].allocation == True:
            # print(f"tasks entered in the queue:", alloted_normal_task[0])
            await q_mission_release.put(alloted_normal_task[0])
            # print("Task released to Main Releaser")

        elif alloted_normal_task[0].allocation == False:
            # print("Task again queued in waiting list")
            await asyncio.sleep(10)
            await q_task_waiting.put([alloted_normal_task[0], alloted_normal_task[1]])
            # print("Task queued in waiting list")
        q_done_product.task_done()


async def release_task_execution(q_mission_release):
    global Sim_step
    Sim_step = 0
    # print("Simulation step initialized to 0")
    while True:

        task_opcua = await q_mission_release.get()
        robot_id = task_opcua["robot"]
        # await asyncio.sleep(1)
        print(f"Task released to robot {robot_id}")
        print(f'>got {task_opcua["robot"]}')
        # print(robot_id)
        await T_robot[robot_id - 1].trigger_task(task=task_opcua)

        for i in range(len(T_robot)):
            #print(i, robot_id)
            if i == robot_id-1 and T_robot[i].exec_cmd == True:
                await q_initiate_task[i].put(task_opcua)
                print(f"Task Initialized for Robot {robot_id}")

        # if robot_id == 1 and T_robot[robot_id - 1].exec_cmd == True:
        #     # loop.call_soon_threadsafe(event1_chk_exec.set)
        #     # event1_chk_exec.set()
        #     # q_robot_mission[0].put_nowait("Task_robot1")
        #     await q_initiate_task[0].put(task_opcua)
        #     print("Triggered event is 1 for robot 1")
        # elif robot_id == 2 and T_robot[robot_id - 1].exec_cmd == True:
        #     # loop.call_soon_threadsafe(event2_chk_exec.set)
        #     # event2_chk_exec.set()
        #     # q_robot_mission[1].put_nowait("Task_robot2")
        #     await q_initiate_task[1].put(task_opcua)
        #     print("Triggered event is 1 for robot 2")
        # elif robot_id == 3 and T_robot[robot_id - 1].exec_cmd == True:
        #     # loop.call_soon_threadsafe(event3_chk_exec.set)
        #     # event3_chk_exec.set()
        #     # q_robot_mission[2].put_nowait("Task_robot3")
        #     await q_initiate_task[2].put(task_opcua)
        #     print("Triggered event is 1 for robot 3")
        Sim_step += 1
        # await asyncio.sleep(2)
        q_mission_release.task_done()


async def task_wait_queue(q_task_waiting, q_mission_release):
    while True:
        awaited_task = await q_task_wait.get()
        print("Task found in the waiting queue", awaited_task[0])
        # await asyncio.sleep(10)
        wait_alloted_task = Greedy_Allocator.normal_allocation(awaited_task[0], awaited_task[1],
                                                               T_robot=T_robot, data_opcua=data_opcua)
        # for task, product in zip(wait_alloted_task[0], wait_alloted_task[1]):
        if wait_alloted_task[0].allocation == True:
            # print(f"task alloted while in the waiting queue:", wait_alloted_task[0])
            await q_mission_release.put(wait_alloted_task[0])
            # print("Task released to Main Releaser")

        elif wait_alloted_task[0].allocation == False:
            # print("Task again queued in waiting list")
            await asyncio.sleep(10)
            await q_task_waiting.put([wait_alloted_task[0], wait_alloted_task[1]])


async def release_opcua_cmd(q_robot_cmd):
    while True:

        data = await q_robot_cmd.get()
        sub_task = data[0]
        target = int(sub_task[1])
        id = data[1]
        product = data[2]
        cmd = ["" for _ in range(len(T_robot))]
        print(f"Task {sub_task} received from Swarm Manager for robot {id} for execution")

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
                    # flag = asyncio.Event()
                    data_opcua["create_part"] = product
                    print("Part created", product)
                    # waiter_task = asyncio.create_task(wait_create_parrt())
                    # await waiter_task
                    run1 = 1
                    # time.sleep(0.5)
                    while run1 == 1:
                        # time.sleep(0.1)
                        # await event_1.set()
                        if data_opcua["recive_part"] == True:  # Wait until a part har been created
                            data_opcua["create_part"] = 0
                            run1 = 0
                    run2 = 1
                    while run2 == 1:
                        # time.sleep(0.1)
                        # await event_2.set()
                        if (data_opcua["recive_part"] == False):
                            run2 = 0
                    # wait_create_parrt(product=product, event_1=)
                    # print(f"product {product} created for robot {id}")
                    # Ax_station[target-10].booked = True
                    # await asyncio.sleep(0.5)

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
        print("OPCUA released command", cmd)
        # await asyncio.sleep(3)
        # t1 = time.time()
        "Wait for rob_busy"
        # waiter_task2 = asyncio.create_task(wait_rob_busy(id=id))
        # await waiter_task2
        run3 = 1
        while run3 == 1:
            # print(data_opcua["rob_busy"][id - 1])
            if data_opcua["rob_busy"][id - 1] == True:
                run3 = 0
        data_opcua["mobile_manipulator"] = ["", "", "", "", "", "", "", "", "", ""]
        print("command sent to opcuaclient", cmd)
        for i in range(len(T_robot)):
            #print(i, id)
            if i == id-1 and data_opcua["rob_busy"][i]:
                await q_exec_start[i].put("Start")
                print(f"Triggered execution_timer event for Robot {id}")

        # if id == 1 and data_opcua["rob_busy"][0]:
        #     # event1_exectime.set()
        #     await q_exec_start[0].put("Start")
        #     print("Triggered execution_timer event for robot 1")
        # elif id == 2 and data_opcua["rob_busy"][1]:
        #     # event2_exectime.set()
        #     await q_exec_start[1].put("Start")
        #     print("Triggered execution_timer event for robot 2 ")
        # elif id == 3 and data_opcua["rob_busy"][2]:
        #     # event3_exectime.set()
        #     await q_exec_start[2].put("Start")
        #     print("Triggered execution_timer event for robot 3")
        # await asyncio.sleep(2)
        q_robot_cmd.task_done()


async def main():
    # q = asyncio.Queue()
    # q2 = asyncio.Queue()
    # event = asyncio.Event()

    concurrency = 1  # consumers count

    tasks = [asyncio.create_task(release_task_execution(q_main_to_releaser))]

    tasks += [asyncio.create_task(
        T_robot[0].initiate_task(q_initiate_task=q_initiate_task[0], W_robot=W_robot, Ax_station=Ax_station,
                                 q_trigger_cmd=q_robot_to_opcua))]
    tasks += [asyncio.create_task(
        T_robot[1].initiate_task(q_initiate_task=q_initiate_task[1], W_robot=W_robot, Ax_station=Ax_station,
                                 q_trigger_cmd=q_robot_to_opcua))]
    tasks += [asyncio.create_task(
        T_robot[2].initiate_task(q_initiate_task=q_initiate_task[2], W_robot=W_robot, Ax_station=Ax_station,
                                 q_trigger_cmd=q_robot_to_opcua))]
    tasks += [asyncio.create_task(release_opcua_cmd(q_robot_to_opcua))]

    task_queue = asyncio.create_task(release_task_execution(q_mission_release=q_main_to_releaser))
    product_queue = asyncio.create_task(release_products(q_done_product=q_product_release, q_task_waiting=q_task_wait,
                                                         q_mission_release=q_main_to_releaser))
    wait_queue = asyncio.create_task(task_wait_queue(q_task_waiting=q_task_wait, q_mission_release=q_main_to_releaser))
    opcua_queue = asyncio.create_task(release_opcua_cmd(q_robot_cmd=q_robot_to_opcua))

    T1 = asyncio.create_task(
        T_robot[0].initiate_task(q_initiate_task=q_initiate_task[0], W_robot=W_robot, Ax_station=Ax_station,
                                 q_trigger_cmd=q_robot_to_opcua))
    T2 = asyncio.create_task(
        T_robot[1].initiate_task(q_initiate_task=q_initiate_task[1], W_robot=W_robot, Ax_station=Ax_station,
                                 q_trigger_cmd=q_robot_to_opcua))
    T3 = asyncio.create_task(
        T_robot[2].initiate_task(q_initiate_task=q_initiate_task[2], W_robot=W_robot, Ax_station=Ax_station,
                                 q_trigger_cmd=q_robot_to_opcua))

    T4 = asyncio.create_task(
        T_robot[0].execution_timer(q_executing_task=q_exec_start[0], q_done_product=q_product_release,
                                   q_trigger_cmd=q_robot_to_opcua, q_initiate_process=q_initiate_process,
                                   q_initiate_task=q_initiate_task[0],
                                   T_robot=T_robot, W_robot=W_robot, Ax_station=Ax_station,
                                   GreedyScheduler=GreedyScheduler,
                                   data_opcua=data_opcua))
    T5 = asyncio.create_task(
        T_robot[1].execution_timer(q_executing_task=q_exec_start[1], q_done_product=q_product_release,
                                   q_trigger_cmd=q_robot_to_opcua, q_initiate_process=q_initiate_process,
                                   q_initiate_task=q_initiate_task[1],
                                   T_robot=T_robot, W_robot=W_robot, Ax_station=Ax_station,
                                   GreedyScheduler=GreedyScheduler,
                                   data_opcua=data_opcua))
    T6 = asyncio.create_task(
        T_robot[2].execution_timer(q_executing_task=q_exec_start[2], q_done_product=q_product_release,
                                   q_trigger_cmd=q_robot_to_opcua, q_initiate_process=q_initiate_process,
                                   q_initiate_task=q_initiate_task[2],
                                   T_robot=T_robot, W_robot=W_robot, Ax_station=Ax_station,
                                   GreedyScheduler=GreedyScheduler,
                                   data_opcua=data_opcua))
    T_initiate = []

    for i in range(len(T_robot)):
        print("total robots task initialisation ", i)
        T_initiate.append(asyncio.create_task(
            T_robot[i].initiate_task(q_initiate_task=q_initiate_task[i], W_robot=W_robot, Ax_station=Ax_station,
                                     q_trigger_cmd=q_robot_to_opcua)))
    T_execution = []

    for i in range(len(T_robot)):
        print("total robots task execution ", i)
        T_execution.append(asyncio.create_task(
            T_robot[i].execution_timer(q_executing_task=q_exec_start[i], q_done_product=q_product_release,
                                       q_trigger_cmd=q_robot_to_opcua, q_initiate_process=q_initiate_process,
                                       q_initiate_task=q_initiate_task[i],
                                       T_robot=T_robot, W_robot=W_robot, Ax_station=Ax_station,
                                       GreedyScheduler=GreedyScheduler,
                                       data_opcua=data_opcua)))

    W_process = []
    for i in range(len(W_robot)):
        print("total workstation async process", i)
        W_process.append(asyncio.create_task(W_robot[i].process_execution(q_initiate_process=q_initiate_process[i],
                                                                          q_done_product=q_product_release)))

    #await asyncio.gather(task_queue, product_queue, wait_queue, opcua_queue, T1, T2, T3, T4, T5, T6, *W_process)
    await asyncio.gather(task_queue, product_queue, wait_queue, opcua_queue, *T_initiate, *T_execution, *W_process)

    # await asyncio.gather(producer(q), consumer2(q2, 1), consumer(q, 1, q2) , main_function(data_opcua))
    print("Production Ended")


if __name__ == "__main__":
    total_TRs = 3
    total_WRs = 10

    data_opcua = Manager().dict()
    q_main_to_releaser = asyncio.Queue()
    # q_initiate_task1 = asyncio.Queue()
    # q_initiate_task2 = asyncio.Queue()
    # q_initiate_task3 = asyncio.Queue()
    q_product_release = asyncio.Queue()
    q_task_wait = asyncio.Queue()
    q_initiate_task = [asyncio.Queue() for _ in range(total_TRs)]
    q_robot_to_opcua = asyncio.Queue()
    q_exec_start = [asyncio.Queue() for _ in range(total_TRs)]
    q_initiate_process = [asyncio.Queue() for _ in range(total_WRs)]

    # Initialised opcua data
    data_opcua["brand"] = "Ford"
    data_opcua["mobile_manipulator"] = ["", "", "", "", "", "", "", "", "", ""]
    data_opcua["rob_busy"] = [False, False, False, False, False, False, False, False, False, False]
    data_opcua["machine_pos"] = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], ]
    data_opcua["robot_pos"] = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    data_opcua["create_part"] = 0
    data_opcua["recive_part"] = False
    data_opcua["done_createing_part"] = False
    data_opcua["mission"] = ["", "", "", "", "", "", "", "", "", ""]
    data_opcua["all_task_time":] = ["", "", "", "", "", "", "", "", "", ""]
    data_opcua["do_reconfiguration"] = False
    data_opcua["reconfiguration_machine_pos"] = ""

    ### instantiate order and generation of task list to that order
    test_order = Task_Planning_agent(input_order=production_order)
    generated_task = test_order.task_list()
    Product_task = generated_task[0]
    Global_task = generated_task[1]
    Task_Queue = generated_task[2]

    ## Start opcua client - New Process###
    opcua_client = Process(target=start_opcua, args=(data_opcua,))
    opcua_client.start()

    while (True):

        time.sleep(2)
        print("Awaiting data from Visual Components")
        # print(data_opcua["machine_pos"])

        print(data_opcua["machine_pos"])
        # print(data_opcua["robot_pos"])
        if data_opcua["machine_pos"][0] != [0, 0]:
            global_wk_pos = data_opcua["machine_pos"]
            print("Data initialized")
            break

    T_robot = []
    W_robot = []
    Ax_station = []

    ##### Initialization of auxiliary stations#######
    for i in range(total_WRs):
        source = Auxillary_station(stn_no=i + 10, order=production_order, product=null_product)
        Ax_station.append(source)
    sink_station = Auxillary_station(stn_no=40, order=production_order, product=null_product)
    Ax_station.append(sink_station)

    for i, type in enumerate(production_order["Wk_type"]):
        if type == 1 or type == 2:
            # print("create wk", i, pt, type)
            wr = Workstation_robot(wk_no=i + 1, order=production_order, product=null_product)
            W_robot.append(wr)

    q_robot = []
    # for r in data_opcua["rob_busy"]:
    for r in range(total_TRs):
        q3 = queue.Queue()
        q_robot.append(q3)
    # for i, R in enumerate(data_opcua["rob_busy"]):
    for i in range(total_TRs):
        # print(i+1, R)
        robot = Transfer_robot(id=i + 1, global_task=Global_task, product=None, tqueue=q_robot[i],
                               machine_pos=global_wk_pos)
        T_robot.append(robot)

    print("Robots initialised numbers", len(T_robot))

    ##### Initialize Task Allocator agent #########
    Greedy_Allocator = Task_Allocator_agent()
    print("Task Allocator Initiated")

    ### Initialize Reactive Scheduler
    GreedyScheduler = Scheduling_agent(
        order=production_order,
        product_task=Product_task,
        T_robot=T_robot

    )

    ### Perform task creation and allocation process
    initial_allotment = GreedyScheduler.initialize_production()
    print("Scheduler Initiated", initial_allotment)

    ### Allocate tasks to the Robots
    alloted_initial_task = Greedy_Allocator.step_allocation(initial_allotment[0], initial_allotment[1], data_opcua,
                                                            T_robot)

    # print(len(alloted_initial_task[0]))

    ##Transfer allocated tasks to task queue####
    for task in alloted_initial_task[0]:
        print(f"tasks in the queue:", task)
        q_main_to_releaser.put_nowait(task)

    asyncio.run(main())

    # try:
    #
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #     asyncio.run(main(loop))
    #     # asyncio.run(main(loop), debug=True)
    #     # loop.run_forever()
    # except KeyboardInterrupt:
    #     pass
