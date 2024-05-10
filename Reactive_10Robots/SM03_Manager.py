import asyncio
import queue
import time
import tkinter as tk
from multiprocessing import Process, Manager
import pymongo
from Reactive_10Robots.SM02_opcua_client import start_opcua
from Reactive_10Robots.SM04_Task_Planning_agent import Task_Planning_agent
from Reactive_10Robots.SM05_Scheduler_agent import Scheduling_agent
from Reactive_10Robots.SM06_Task_allocation import Task_Allocator_agent
from Reactive_10Robots.SM07_Robot_agent import production_order, Workstation_robot, null_product, Transfer_robot, \
    Auxillary_station, read_order
# from Reactive_10Robots.SM12_UI import read_tree, select_doc, select_top, save, optimize, Topology
from Reactive_10Robots.SM13_statusUI import MainApp
from Reactive_10Robots.SM11_Dashboard import throughput_gen


def reconfigure_topology(reconfig, default_postions, order):
    # reconfig = "-5947.8017408,1345.07016512d-5891.42134789,3066.44623999d-5801.59637732,4823.26974015d"
    if order == True or reconfig == True:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Topology_Manager"]
        mycol = mydb["Reconfigure_Topology"]
        reconfig_doc = mycol.find_one()
        reconfig_top = reconfig_doc["Topology_str"]
        positions = reconfig_doc["Topology"]

    else:
        print("MongoDB bypassed")
        pass

    if order == True:
        read_order(reconfig_doc)
    else:
        print("Production Order Selected", production_order)

    if reconfig == True:
        print("Reconfiguration Started")
        # reconfig = "0,0d10000,6000d0,12000d0,18000d20000,24000d0,30000d30000,36000d0,42000d0,48000d0,54000d0,60000d"
        print(reconfig_top)
        data_opcua["reconfiguration_machine_pos"] = reconfig_top
        time.sleep(1)
        data_opcua["do_reconfiguration"] = True
        time.sleep(3)
        data_opcua["do_reconfiguration"] = False
        time.sleep(10)
        print("Reconfiguration Ended")

    else:
        positions = default_postions
        print("No Reconfiguration Requested")
    return positions


### Product Release Async Queue####
async def release_products(q_done_product, q_task_waiting, q_mission_release):
    while True:
        done_prod = await q_done_product.get()
        # print(f"product PV={done_prod.pv_Id} and PI={done_prod.pi_Id} released from QUEUE")
        print("Done Processed Product", done_prod)
        normal_allotment = GreedyScheduler.normalized_production(new_product=done_prod, W_robot=W_robot)
        # print("normal allotment", normal_allotment)
        print("Allocation Started for task", normal_allotment[0])
        alloted_normal_task = Greedy_Allocator.normal_allocation(normal_allotment[0], normal_allotment[1],
                                                                 T_robot=T_robot, data_opcua=data_opcua)
        print("alloted normal task", alloted_normal_task)
        # for task, product in zip(alloted_normal_task[0], alloted_normal_task[1]):
        if alloted_normal_task[0].allocation == True:
            # print(f"tasks entered in the queue:", alloted_normal_task[0])
            q_mission_release.put_nowait(alloted_normal_task[0])
            # print("Task released to Main Releaser")
        elif alloted_normal_task[0].allocation == False:
            # print("Task again queued in waiting list")
            await asyncio.sleep(10)
            q_task_waiting.put_nowait([alloted_normal_task[0], alloted_normal_task[1]])
            # print("Task queued in waiting list")
        q_done_product.task_done()


### Task Release based on Products Async Queue####
async def release_task_execution(q_mission_release, q_initiate_task):
    global Sim_step
    Sim_step = 0
    # print("Simulation step initialized to 0")
    while True:

        task_opcua = await q_mission_release.get()
        robot_id = task_opcua["robot"]
        # await asyncio.sleep(1)
        print(f"Task released to robot {robot_id}")
        # print(f'>got {task_opcua["robot"]}')
        # print(robot_id)
        T_robot[robot_id - 1].trigger_task(task=task_opcua)

        for i in range(len(T_robot)):
            # print(i, robot_id)
            if i == robot_id - 1 and T_robot[i].exec_cmd == True:
                q_initiate_task[i].put_nowait(task_opcua)
                # print(f"Task Initialized for Robot {robot_id}")
        Sim_step += 1
        # await asyncio.sleep(2)
        q_mission_release.task_done()


### Task Wait based on unallocated Tasks Async Queue####
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
            q_mission_release.put_nowait(wait_alloted_task[0])
            # print("Task released to Main Releaser")

        elif wait_alloted_task[0].allocation == False:
            # print("Task again queued in waiting list")
            await asyncio.sleep(10)
            q_task_waiting.put_nowait([wait_alloted_task[0], wait_alloted_task[1]])


### OPCUA command to Visual Components Async Queue####
async def release_opcua_cmd(q_robot_cmd, q_exec_start):
    while True:

        data = await q_robot_cmd.get()
        # print("Check this error", data)
        sub_task = data[0]
        target = int(sub_task[1])
        id = data[1]
        product = data[2]
        cmd = ["" for _ in range(len(T_robot))]

        # print(f"Task {sub_task} received from Swarm Manager for robot {id} for execution")

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
                # y_pos = 4032 - ((id - 1) * 2000)  ##old -1700 , 5000
                # c = "m" + "," + "-10662" + "," + str(y_pos) + "," + "0"
                x_pos = 10000 - ((id - 1) * 2000)
                c = "m" + "," + str(x_pos) + "," + "10000" + "," + "0"

                cmd.insert((int(id) - 1), c)
        opcua_cmd = cmd[:10]
        data_opcua["mobile_manipulator"] = opcua_cmd
        # print("OPCUA released command", opcua_cmd)
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
        # print("command sent to opcuaclient", opcua_cmd)
        for i in range(len(T_robot)):
            # print(i, id)
            if i == id - 1 and data_opcua["rob_busy"][i]:
                q_exec_start[i].put_nowait("Start")
                # print(f"Triggered execution_timer event for Robot {id}")
        q_robot_cmd.task_done()


async def collect_data(scheduler):
    while True:
        total_products = []
        active_products = []
        finished_products = []
        for product in scheduler.active_products:
            t_p = [product.pv_Id, product.pi_Id]
            total_products.append(t_p)
        for fin_prod in scheduler.finished_product:
            f_p =[fin_prod.pv_Id, fin_prod.pi_Id]
            finished_products.append(f_p)
        for product in total_products:
            if product not in finished_products:
                active_products.append(product)
        print("Active Product List", active_products)
        for wk in W_robot:
            print(f"Workstation {wk.id} Queue is {wk.pqueue}")
        await throughput_gen(active_products)
        await asyncio.sleep(10)


async def async_main():
    task_queue = asyncio.create_task(release_task_execution(q_mission_release=q_main_to_releaser,
                                                            q_initiate_task=q_initiate_task))
    product_queue = asyncio.create_task(release_products(q_done_product=q_product_release, q_task_waiting=q_task_wait,
                                                         q_mission_release=q_main_to_releaser))
    wait_queue = asyncio.create_task(task_wait_queue(q_task_waiting=q_task_wait, q_mission_release=q_main_to_releaser))
    opcua_queue = asyncio.create_task(release_opcua_cmd(q_robot_cmd=q_robot_to_opcua, q_exec_start=q_exec_start))
    data_capture = asyncio.create_task(collect_data(scheduler=GreedyScheduler))

    T_initiate = []

    for i in range(len(T_robot)):
        # print("total robots task initialisation ", i)
        T_initiate.append(asyncio.create_task(
            T_robot[i].initiate_task(q_initiate_task=q_initiate_task[i], W_robot=W_robot, Ax_station=Ax_station,
                                     q_trigger_cmd=q_robot_to_opcua)))
    T_execution = []

    for i in range(len(T_robot)):
        # print("total robots task execution ", i)
        T_execution.append(asyncio.create_task(
            T_robot[i].execution_timer(q_executing_task=q_exec_start[i], q_done_product=q_product_release,
                                       q_trigger_cmd=q_robot_to_opcua, q_initiate_process=q_initiate_process,
                                       q_initiate_task=q_initiate_task[i],
                                       T_robot=T_robot, W_robot=W_robot, Ax_station=Ax_station,
                                       GreedyScheduler=GreedyScheduler,
                                       data_opcua=data_opcua)))

    W_process = []
    for i in range(len(W_robot)):
        # print("total workstation async process", i)
        W_process.append(asyncio.create_task(W_robot[i].process_execution(q_initiate_process=q_initiate_process[i],
                                                                          q_done_product=q_product_release,
                                                                          T_robot=T_robot,
                                                                          GreedyScheduler=GreedyScheduler,
                                                                          q_initiate_task=q_initiate_task)))

    # await asyncio.gather(task_queue, product_queue, wait_queue, opcua_queue, T1, T2, T3, T4, T5, T6, *W_process)
    await asyncio.gather(task_queue, product_queue, wait_queue, opcua_queue, data_capture, *T_initiate, *T_execution, *W_process)


def run_simulation():
    ### Perform task creation and allocation process
    initial_allotment = GreedyScheduler.initialize_production(W_robot=W_robot)
    # print("Scheduler Initiated", initial_allotment)

    ### Allocate tasks to the Robots
    alloted_initial_task = Greedy_Allocator.step_allocation(initial_allotment[0], initial_allotment[1], data_opcua,
                                                            T_robot)
    # print(len(alloted_initial_task[0]))

    ##Transfer allocated tasks to task queue####
    for task in alloted_initial_task[0]:
        # print(f"tasks in the queue:", task)
        q_main_to_releaser.put_nowait(task)

    asyncio.run(async_main())


def testing_UI(T_robots, W_robots):
    root = tk.Tk()
    app = MainApp(root, T_robots=T_robots, W_robots=W_robots)
    root.mainloop()


if __name__ == "__main__":
    # window = tk.Tk()
    # window.title('Swarm Manager')
    # window.geometry('1920x1080')
    total_TRs = 10
    total_WRs = 10
    T_robot = []
    W_robot = []
    Ax_station = []
    q_robot = []
    Wk_positions = []
    data_opcua = Manager().dict()
    q_main_to_releaser = asyncio.Queue()
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

    ## Start opcua client - New Process###
    opcua_client = Process(target=start_opcua, args=(data_opcua,))
    opcua_client.start()

    while True:
        time.sleep(2)
        print("Awaiting data from Visual Components")
        # print(data_opcua["machine_pos"])
        print(data_opcua["machine_pos"])
        # print(data_opcua["robot_pos"])
        if data_opcua["machine_pos"][0] != [0, 0]:
            initial_wk_pos = data_opcua["machine_pos"]
            # print("Data initialized")
            break

    # # do reconfiguration based on chosen topology from UI
    Wk_positions = reconfigure_topology(reconfig=True, default_postions=initial_wk_pos, order=False)
    print("Before Reconfiguration", Wk_positions)
    print("After Reconfiguration", data_opcua["machine_pos"])

    ### instantiate order and generation of task list to that order
    test_order = Task_Planning_agent(input_order=production_order)
    generated_missions = test_order.task_list()
    Product_missions = generated_missions[0]
    Global_missions = generated_missions[1]
    mission_Queue = generated_missions[2]

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

    # for r in data_opcua["rob_busy"]:
    for r in range(total_TRs):
        q3 = queue.Queue()
        q_robot.append(q3)
    # for i, R in enumerate(data_opcua["rob_busy"]):
    for i in range(total_TRs):
        # print(i+1, R)
        robot = Transfer_robot(id=i + 1, global_task=Global_missions, product=None, tqueue=q_robot[i],
                               machine_pos=Wk_positions)
        T_robot.append(robot)

    # print("Robots initialised numbers", len(T_robot))

    ##### Initialize Task Allocator agent #########
    Greedy_Allocator = Task_Allocator_agent()
    # print("Task Allocator Initiated")

    ### Initialize Reactive Scheduler
    GreedyScheduler = Scheduling_agent(
        order=production_order,
        product_missions=Product_missions,
        T_robot=T_robot
    )

    "## Code moved to subroutine#####"
    ### Perform task creation and allocation process
    initial_allotment = GreedyScheduler.initialize_production(W_robot=W_robot)
    print("Scheduler Initiated", initial_allotment)

    ### Allocate tasks to the Robots
    alloted_initial_task = Greedy_Allocator.step_allocation(initial_allotment[0], initial_allotment[1], data_opcua,
                                                            T_robot)

    print(len(alloted_initial_task[0]))

    ##Transfer allocated tasks to task queue####
    for task in alloted_initial_task[0]:
        print(f"tasks in the queue:", task)
        q_main_to_releaser.put_nowait(task)

    # robots_sts = Manager().list()
    # workstation_sts = Manager().list()
    #
    # for robot, wk in zip(T_robot, W_robot):
    #     robots_sts.append(serialise_robot(robot))
    #     workstation_sts.append(serialise_workstation(wk))

    ## Start Testing tkinter UI - New Process###
    # testing_client = Process(target=testing_UI, args=(T_robot, W_robot,))
    # testing_client.start()

    asyncio.run(async_main())
    opcua_client.join()
    # testing_client.join()
