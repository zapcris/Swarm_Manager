'The problem with Multiprocessing : '
'1. Difficult to move complex objects (GreedyScheduler)'

# SuperFastPython.com
# example of using the queue between processes with a timeout
import asyncio
import time
from time import sleep
from random import random
from multiprocessing import Process, Manager, shared_memory, Queue
from queue import Empty

from Reactive_mulitprocessing.SM02_opcua_client import start_opcua
from Reactive_mulitprocessing.SM04_Task_Planning_agent import Task_Planning_agent
from Reactive_mulitprocessing.SM05_Scheduler_agent_mp import Scheduling_agent
from Reactive_mulitprocessing.SM06_Task_allocation_mp import Task_Allocator_agent
from Reactive_mulitprocessing.SM07_Robot_agent_mp import Transfer_robot, Workstation_robot, W_robot, \
    null_product


# from Reactive_10Robots.SM07_Robot_agent import data_opcua


# generate work
def producer(queue):
    print('Producer: Running', flush=True)
    # generate work
    for i in range(10):
        # generate a value
        value = random()
        # block
        sleep(value)
        # add to the queue
        queue.put(value)
    # all done
    queue.put(None)
    print('Producer: Done', flush=True)


# consume work
def consumer(queue):
    print('Consumer: Running', flush=True)
    # consume work
    while True:
        # get a unit of work
        try:
            item = queue.get(timeout=0.5)
        except Empty:
            print('Consumer: gave up waiting...', flush=True)
            continue
        # check for stop
        if item is None:
            break
        # report
        print(f'>got {item}', flush=True)
    # all done
    print('Consumer: Done', flush=True)


### Process to create missions during the initialisation of Swarm Manager
def mission_producer(q_main_to_releaser, alloted_initial_task):
    print('Producer: Running', flush=True)
    # generate work

    ###### Task queue functions #############

    for task in alloted_initial_task[0]:
        print(f"tasks in the queue:", task)
        q_main_to_releaser.put(task)
    ## all done
    q_main_to_releaser.put(None)
    print('Producer: Done', flush=True)


### Process to trigger missions for allocated tasks in the robots
def mission_consumer(q_main_to_releaser, T_robot, GreedyScheduler):
    print('Consumer: Running', flush=True)
    # consume work
    while True:
        # get a unit of work
        try:
            task_opcua = q_main_to_releaser.get(timeout=0.5)
        except Empty:
            print('Consumer: gave up waiting...', flush=True)
            continue
        # check for stop
        if task_opcua is None:
            break
        # report
        print(f'>got {task_opcua}', flush=True)
        id = task_opcua.robot
        # print(robot_id)
        T_robot[id - 1].trigger_task(task=task_opcua)
        if id == 1 and T_robot[id - 1].exec_cmd == True:
            # loop.call_soon_threadsafe(event1_chk_exec.set)
            print("Triggered event is 1 for robot 1")
        elif id == 2 and T_robot[id - 1].exec_cmd == True:
            # loop.call_soon_threadsafe(event2_chk_exec.set)
            print("Triggered event is 1 for robot 2")
        elif id == 3 and T_robot[id - 1].exec_cmd == True:
            # loop.call_soon_threadsafe(event3_chk_exec.set)
            print("Triggered event is 1 for robot 3")
        # normal_allotment = GreedyScheduler.normalized_production(task_opcua)
        # alloted_normal_task = Greedy_Allocator.normal_allocation(normal_allotment[0], normal_allotment[1],
        #                                                        T_robot=T_robot)
    # all done
    print('mission_consumer: Done', flush=True)


### Process to keep task waiting during non clearance####
def mission_wait(q_main_to_releaser, q_task_wait, Greedy_Allocator):
    print('Task Wait: Running', flush=True)
    # consume work
    while True:
        # get a unit of work
        try:
            awaited_task = q_task_wait.get(timeout=0.5)
        except Empty:
            # print('Consumer: gave up waiting...', flush=True)
            continue
        # check for stop
        if awaited_task is None:
            break
        # report
        print(f'>got {awaited_task}', flush=True)
        wait_alloted_task = Greedy_Allocator.normal_allocation(awaited_task[0], awaited_task[1])
        if wait_alloted_task[0].allocation == True:
            # print(f"task alloted while in the waiting queue:", wait_alloted_task[0])
            q_main_to_releaser.put_nowait(wait_alloted_task[0])
        elif wait_alloted_task[0].allocation == False:
            # print("Task again queued in waiting list")
            sleep(10)
            q_task_wait.put_nowait([wait_alloted_task[0], wait_alloted_task[1]])
    # all done
    print('Task wait: Done', flush=True)


### Process to create new producrs(variants/Instance) during the runtime production####
def product_release(q_product_done, q_task_wait, q_main_to_releaser, Greedy_Allocator, T_robot):
    print('Task Wait: Running', flush=True)
    # consume work
    while True:
        # get a unit of work
        try:
            done_prod = q_product_done.get(timeout=0.5)

        except Empty:
            # print('Consumer: gave up waiting...', flush=True)
            continue
        # check for stop
        if done_prod is None:
            break
        # report
        print(f'>got {done_prod}', flush=True)
        # normal_allocation(done_prod)

    # all done
    print('Product Release: Done', flush=True)


# entry point
if __name__ == '__main__':

    # create the shared queue
    queue = Queue()
    q_main_to_releaser = Queue()
    q_task_wait = Queue()
    q_product_done = Queue()
    # shared dict for multiprocessing

    shm_a = shared_memory.SharedMemory(create=True, size=100)
    type(shm_a.buf)

    data_opcua = Manager().dict()
    production_order = Manager().dict()
    Greedy_Allocator = Manager().Namespace()
    GreedyScheduler = Manager().Namespace()
    Product_task = Manager().list()
    Global_task = Manager().list()
    # T_robot = Manager().Namespace()
    # T_robot = multiprocessing.Array('i', range(3))

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

    production_order["brand"] = "Test"
    production_order["PV"] = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
    production_order["sequence"] = [[11, 1, 5, 7, 8, 10, 50],  # [11, 1, 7, 5, 6, 8, 9, 12]
                                    [12, 1, 6, 50],  # [11, 2, 6, 6, 8, 12]
                                    [13, 3, 9, 50],
                                    [14, 4, 8, 50],  # [11, 4, 8, 12, 9, 12]
                                    [15, 10, 9, 50],
                                    [16, 2, 5, 6, 8, 3, 50],
                                    [17, 3, 6, 8, 2, 4, 3, 50],
                                    [18, 4, 5, 6, 8, 7, 50],
                                    [19, 3, 4, 6, 1, 8, 9, 50],
                                    [20, 2, 4, 6, 8, 5, 7, 9, 50]
                                    ]
    production_order["PI"] = [1, 1, 1, 1, 1, 1, 1, 4, 5, 1]
    production_order["Wk_type"] = [1, 1, 1, 2, 2, 1, 1, 2, 1, 1]
    production_order["Process_times"] = [[10, 10, 20, 10, 15, 14, 15, 12, 10, 10],
                                         # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                                         [10, 30, 20, 10, 45, 14, 15, 12, 10, 10],
                                         # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                                         [15, 10, 20, 10, 15, 14, 15, 12, 10, 30],
                                         # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                                         [20, 30, 40, 50, 20, 40, 10, 70, 30, 10],
                                         [20, 30, 40, 50, 20, 10, 20, 10, 10, 10],
                                         [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                                         [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                                         [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                                         [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                                         [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                                         ]

    ## Start opcua client###
    opcua_client = Process(target=start_opcua, args=(data_opcua,))
    opcua_client.start()

    while (True):
        time.sleep(2)
        print("Awaiting data from Visual Components")
        print(data_opcua)
        # print(data_opcua["robot_pos"])
        if data_opcua["machine_pos"][0] != [0, 0]:
            global_wk_pos = data_opcua["machine_pos"]
            break

    print("The values of workstation positions are", data_opcua["machine_pos"])

    ### instantiate order and generation of task list to that order
    test_order = Task_Planning_agent(input_order=production_order)
    generated_task = test_order.task_list()
    Product_task = generated_task[0]
    print(Product_task)
    Global_task = generated_task[1]
    Task_Queue = generated_task[2]

    for i, type in enumerate(production_order["Wk_type"]):
        if type == 1 or type == 2:
            # print("create wk", i, pt, type)
            wr = Workstation_robot(wk_no=i + 1, order=production_order, product=null_product)
            W_robot.append(wr)

    ########## Initialization of Carrier robots######################################################
    # for r in data_opcua["rob_busy"]:
    T_robot = []
    for i in range(3):
        # print(i+1, R)
        robot = Transfer_robot(id=i + 1, global_task=Global_task, product=None,
                               machine_pos=global_wk_pos)
        T_robot.append(robot)

    print("Total transfer robots", len(T_robot))

    ##### Initialize Task Allocator agent #########
    Greedy_Allocator = Task_Allocator_agent()

    GreedyScheduler = Scheduling_agent()
    # order=production_order,
    # product_task=Product_task,
    # T_robot=T_robot

    ### Perform task creation and allocation process
    initial_allotment = GreedyScheduler.initialize_production(order=production_order, robots=T_robot, product_task=Product_task)
    for i in initial_allotment:
        print(i)
    print(data_opcua["machine_pos"])
    alloted_initial_task = Greedy_Allocator.step_allocation(initial_allotment[0], initial_allotment[1], data_opcua,
                                                            T_robot)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    event1_exectime = asyncio.Event()
    event2_exectime = asyncio.Event()
    event3_exectime = asyncio.Event()
    event1_opcua = asyncio.Event()
    event2_opcua = asyncio.Event()
    event3_opcua = asyncio.Event()
    event1_chk_exec = asyncio.Event()
    event2_chk_exec = asyncio.Event()
    event3_chk_exec = asyncio.Event()
    event1_pth_clr = asyncio.Event()
    event2_pth_clr = asyncio.Event()
    event3_pth_clr = asyncio.Event()

    ##### Producer Task Release Thread################
    task_producer = Process(target=mission_producer, args=(q_main_to_releaser, alloted_initial_task,))
    task_producer.start()

    ##### Consumer Task Release Thread################
    task_consumer = Process(target=mission_consumer, args=(q_main_to_releaser, T_robot, GreedyScheduler,))
    task_consumer.start()

    ##### Task wait Release Thread################
    task_wait = Process(target=mission_wait, args=(q_main_to_releaser, q_task_wait, Greedy_Allocator,))
    task_wait.start()

    ##### Product Release Thread################
    generate_product = Process(target=product_release,
                               args=(q_product_done, q_task_wait, q_main_to_releaser, Greedy_Allocator, T_robot))
    generate_product.start()

    # ###### Task queue functions #############
    #
    # for task in alloted_initial_task[0]:
    #     print(f"tasks in the queue:", task)
    #     q_main_to_releaser.put(task)

    # ##### Task waiting Thread ################
    # task_waiting_thread = Process(target=task_wait, daemon=True)
    # task_waiting_thread.start()
    # ##### Start OPCUA Command Thread################
    # opcuacmd_thread = Process(target=opcua_release, daemon=True, args=(loop,))
    # opcuacmd_thread.start()
    # ##### Start done product Thread################
    # done_product_thread = Process(target=done_release, daemon=True)
    # done_product_thread.start()

    # start the consumer
    # consumer_process = Process(target=consumer, args=(queue,))
    # consumer_process.start()
    # # start the producer
    # producer_process = Process(target=producer, args=(queue,))
    # producer_process.start()
    # wait for all processes to finish
    opcua_client.join()
    # task_releaser.join()
    # producer_process.join()
    # consumer_process.join()
    task_producer.join()
    task_consumer.join()
    task_wait.join()
    generate_product.join()
