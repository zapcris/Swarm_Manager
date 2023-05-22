import asyncio
from datetime import datetime
from scipy.spatial import distance
from Reactive_majorversion2.SM04_Task_Planning_agent import Task_Planning_agent, generate_task
from Reactive_majorversion2.SM05_Scheduler_agent import Scheduling_agent
from Reactive_majorversion2.SM10_Product_Task import Product, Task, Transfer_time, Waiting_time, Sink, Process_time

#### Data Initialization ################

production_order = {
    "Name": "Test",
    "PV": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "sequence": [[11, 1, 5, 7, 8, 10, 50],  # [11, 1, 7, 5, 6, 8, 9, 12]
                 [12, 1, 6, 50],  # [11, 2, 6, 6, 8, 12]
                 [13, 3, 9, 50],
                 [14, 4, 8, 50],  # [11, 4, 8, 12, 9, 12]
                 [15, 10, 9, 12],
                 [16, 2, 5, 6, 8, 3, 12],
                 [17, 3, 6, 8, 2, 4, 3, 12],
                 [18, 4, 5, 6, 8, 7, 12],
                 [19, 3, 4, 6, 1, 8, 9, 12],
                 [20, 2, 4, 6, 8, 5, 7, 9, 12]
                 ],
    "PI": [2, 1, 1, 1, 1, 1, 1, 4, 5, 1],
    "Wk_type": [1, 1, 1, 2, 2, 1, 1, 2, 1, 1],
    "Process_times": [[30, 30, 20, 30, 45, 14, 15, 12, 10, 30],  # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                      [30, 30, 20, 30, 45, 14, 15, 12, 10, 30],  # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [25, 30, 20, 30, 45, 14, 15, 12, 10, 30],  # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                      ]
}

data_opcua = {
    "brand": "Ford",
    "mobile_manipulator": ["", "", "", "", "", "", "", "", "", ""],
    "rob_busy": [False, False, False, False, False, False, False, False, False, False],
    "machine_pos": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], ],
    "robot_pos": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    "create_part": 0,
    "mission": ["", "", "", "", "", "", "", "", "", ""],
    "all_task_time": ["", "", "", "", "", "", "", "", "", ""],
    "do_reconfiguration": False,
    "reconfiguration_machine_pos": "",

}

Events = {
    "brand": "Ford",
    "rob_execution": [False, False, False],
    "rob_mission": ["", "", ""],
    "rob_product": [[int, int], [int, int], [int, int]],
    "machine_status": [False for stat in range(10)],
    "machine_product": [[int, int] for product in range(10)],
    "elapsed_time": [int for et in range(10)],
    "Product_finished": []

}

capabilities = [[1, 3],
                [2, 4],
                [3, 8],
                [4, 9],
                [5, 1],
                [6, 3],
                [7, 4],
                [8, 2],
                [9, 1],
                [10, 5]
                ]

################################# Taken from Robot_Agent###############################################################
#### Initialization data###############

q_main_to_releaser = asyncio.Queue()
q_robot_to_opcua = asyncio.Queue()
q_product_done = asyncio.Queue()
q_task_wait = asyncio.Queue()

null_product = Product(pv_Id=0, pi_Id=0, task_list=[], inProduction=False, finished=False, last_instance=0, robot=99,
                       wk=0, released=False, tracking=[])
null_Task = Task(id=0, type=0, command=[], pV=0, pI=0, allocation=False, status="null", robot=99, step=0)
T_robot = []
W_robot = []
Ax_station = []

p1 = Product(pv_Id=1, pi_Id=1, task_list=[[11, 1], [2, 5]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False, tracking=[])
p2 = Product(pv_Id=1, pi_Id=1, task_list=[[11, 2], [2, 8]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False, tracking=[])
p3 = Product(pv_Id=1, pi_Id=1, task_list=[[11, 3], [3, 6]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False, tracking=[])
test_task = Task(id=1, type=1, command=[11, 1], pV=1, pI=1, allocation=False, status="null", robot=1, step=0)

test_product = [p1, p2, p3]
#################################### Robot agent code ################################################
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
wk_1 = asyncio.Event()
wk_2 = asyncio.Event()
wk_3 = asyncio.Event()
wk_4 = asyncio.Event()
wk_5 = asyncio.Event()
wk_6 = asyncio.Event()
wk_7 = asyncio.Event()
wk_8 = asyncio.Event()
wk_9 = asyncio.Event()
wk_10 = asyncio.Event()

opc_cmd_list = []
wk_proc_event = 99


def opcua_cmd_event(id, loop):
    # id = task.robot
    print("Triggered opcua robot id is:", id)
    if id == 1 and T_robot[id - 1].exec_cmd == True:
        loop.call_soon_threadsafe(event1_chk_exec.set)
        print("Triggered event is 1 for robot 1")
    elif id == 2 and T_robot[id - 1].exec_cmd == True:
        loop.call_soon_threadsafe(event2_chk_exec.set)
        print("Triggered event is 1 for robot 2")
    elif id == 3 and T_robot[id - 1].exec_cmd == True:
        loop.call_soon_threadsafe(event3_chk_exec.set)
        print("Triggered event is 1 for robot 3")


def wk_process_event(wk, loop: asyncio.AbstractEventLoop):
    if wk == 1:
        loop.call_soon_threadsafe(wk_1.set)
        print("Triggered wk process execution for Workstation1")
        wk_proc_event = 99
        # return wk_1
    elif wk == 2:
        loop.call_soon_threadsafe(wk_2.set)
        print("Triggered wk process execution for Workstation2")
        wk_proc_event = 99
        # return wk_2
    elif wk == 3:
        loop.call_soon_threadsafe(wk_3.set)
        print("Triggered wk process execution for Workstation3")
        wk_proc_event = 99
        # return wk_3
    elif wk == 4:
        loop.call_soon_threadsafe(wk_4.set)
        print("Triggered wk process execution for Workstation4")
        wk_proc_event = 99
        # return wk_4
    elif wk == 5:
        loop.call_soon_threadsafe(wk_5.set)
        print("Triggered wk process execution for Workstation5")
        wk_proc_event = 99
        # return wk_5
    elif wk == 6:
        loop.call_soon_threadsafe(wk_6.set)
        print("Triggered wk process execution for Workstation6")
        wk_proc_event = 99
        # return wk_6
    elif wk == 7:
        loop.call_soon_threadsafe(wk_7.set)
        print("Triggered wk process execution for Workstation7")
        wk_proc_event = 99
        # return wk_7
    elif wk == 8:
        loop.call_soon_threadsafe(wk_8.set)
        print("Triggered wk process execution for Workstation8")
        wk_proc_event = 99
        # return wk_8
    elif wk == 9:
        loop.call_soon_threadsafe(wk_9.set)
        print("Triggered wk process execution for Workstation9")
        wk_proc_event = 99
        # return wk_9
    elif wk == 10:
        loop.call_soon_threadsafe(wk_10.set)
        print("Triggered wk process execution for Workstation10")
        wk_proc_event = 99
        # return wk_10


### instantiate order and generation of task list to that order
test_order = Task_Planning_agent(input_order=production_order)
generated_task = test_order.task_list()
Product_task = generated_task[0]
Global_task = generated_task[1]
Task_Queue = generated_task[2]

### Initialize Reactive Scheduler
GreedyScheduler = Scheduling_agent(
    order=production_order,
    product_task=Product_task,
    T_robot=T_robot

)


async def bg_tsk(flag, condn):
    while True:
        if condn == True:

            pass
        else:

            flag.set()
            break


class Transfer_robot:

    def __init__(self, id, global_task, product, tqueue, machine_pos):
        self.id = id
        self.free = True
        # self.start_robot(tqueue)
        self.global_task = global_task
        # self.auctioned_task = auctioned_task
        self.success_bid = None
        self.STN = None
        self.assigned_task = False
        self.assigned_product = False
        self.executing = False
        self.event = asyncio.Event()
        self.task = Task(id=0, type=0, command=[], pI=0, pV=0, allocation=False, status="null", robot=1, step=0)
        self.product = product
        self.finished_product = Product
        self.exec_cmd = False
        self.path_clear = False
        self.wk_loc = 99  ### 99 - arbitrary position #####
        self.base_move = False
        self.wait = False
        self.task_initiated = False
        # self.task_step = int
        self.opcua_cmd = []
        self.new_prod = int
        self.machine_pos = machine_pos
        self.base = False
        self.q1 = False
        self.q2 = False
        # print("The values of workstation positions are", self.machine_pos)

    def __await__(self):
        async def closure():
            # print("await")
            return self

        return closure().__await__()

    def bid(self, auctioned_task: Task):
        bid_value = 0.0
        task_cost = 0.0
        marginal_cost = 0.0
        machine_pos = [[3569, 5526], [11989, 5176], [5401, -1414], [14936, -1658], [25615, -2503], [3077, 12153],
                       [15434, 16900], [12432, 10650], [22123, 10581], [27500, 3630]]
        # print("The broadcasted task is", auctioned_task)

        start_loc = auctioned_task.command[0]
        end_loc = auctioned_task.command[1]
        # total_ws = len(data_opcua["machine_pos"])
        # print("Bid started")

        if start_loc == 11:  ## if source node
            start_pos = [-6000, -2000]
        elif start_loc == 12:  ## if source node
            start_pos = [-6000, -4000]
        elif start_loc == 13:  ## if source node
            start_pos = [-6000, -6000]
        elif start_loc == 14:  ## if source node
            start_pos = [-6000, -8000]
        elif start_loc == 15:  ## if source node
            start_pos = [-6000, -10000]
        else:
            # start_pos = data_opcua["machine_pos"][start_loc - 1]
            start_pos = self.machine_pos[start_loc - 1]

        # print("Start_position", start_pos)
        if end_loc == 50:  ## if source node or sink node
            end_pos = [24517, 11716]
        else:
            # end_pos = data_opcua["machine_pos"][end_loc - 1]
            end_pos = self.machine_pos[end_loc - 1]
            print("Target position values", end_pos)
        # print("End_position", end_pos)
        # print("Start position values", start_pos)
        # print("Target position values", end_pos)
        task_cost = distance.euclidean(start_pos, end_pos)
        # print("Cleared bid mid-function")
        # if self.data_opcua["rob_busy"][self.id-1] == False :
        if self.free == True and data_opcua["rob_busy"][self.id - 1] == False:
            marginal_cost = distance.euclidean(start_pos, data_opcua["robot_pos"][self.id - 1])
        else:
            marginal_cost = 99999999999
        bid_value = task_cost + marginal_cost
        print(bid_value)
        return bid_value

    def task_assign(self, task):
        self.assigned_task = True
        self.task = task
        self.free = False

    def product_assign(self, product):
        self.assigned_task = True
        self.product = product
        self.free = False

    def trigger_task(self, task):
        self.task = task
        self.exec_cmd = True

        print(f"Task triggered to robot {self.id} and execution status is {self.exec_cmd}")

    async def initiate_task(self, event_frommain: asyncio.Event, event_toopcua: asyncio.Event):
        while True:
            await event_frommain.wait()
            self.task_initiated = True
            # self.task_step += 1
            # print(f"OPCUA command initiated at robot {self.id}")
            pickup = self.task.command[0]
            drop = self.task.command[1]
            self.new_prod = self.task.pV
            print(f"Task Step value is {self.task.step}")

            match self.task.step:
                case 1:
                    ########Pickup part from source position########
                    if 11 <= pickup <= 20 and event_toopcua.is_set() == False and Ax_station[
                        pickup - 11].booked == False:
                        self.opcua_cmd = ["pick", str(pickup - 1)]
                        self.path_clear = True
                        Ax_station[pickup - 11].booked = True
                        # self.task.step = 2

                        print(f" Path clearance condition 2 activated for robot {self.id} for task{self.task.command}")

                case 2:
                    print(f"Drop station {drop} status, booking : {W_robot[drop - 1].booked}, "
                          f"Queue1 {W_robot[drop - 1].q1_empty}, Queue2 {W_robot[drop - 1].q2_empty}")
                    ########To drop workstation########
                    if 1 <= drop <= 10 and event_toopcua.is_set() == False:
                        if W_robot[drop - 1].booked == False and W_robot[drop - 1].product_free == True and W_robot[
                            drop - 1].robot_free == True:
                            self.opcua_cmd = ["drop", str(drop - 1)]
                            self.path_clear = True
                            self.task.step = 5  ## Last step ####
                            W_robot[drop - 1].booked = True
                        elif (W_robot[drop - 1].booked == True or W_robot[drop - 1].product_free == False or W_robot[
                            drop - 1].robot_free == False) \
                                and (W_robot[drop - 1].q1_empty == True):
                            self.opcua_cmd = ["q1", str(drop - 1)]
                            self.path_clear = True
                            self.task.step = 3
                            W_robot[drop - 1].q1_empty = False
                        elif (W_robot[drop - 1].booked == True or W_robot[drop - 1].product_free == False or W_robot[
                            drop - 1].robot_free == False) \
                                and (W_robot[drop - 1].q1_empty == False) and (W_robot[drop - 1].q2_empty == True) and (
                                self.wk_loc != drop):
                            self.opcua_cmd = ["q2", str(drop - 1)]
                            self.path_clear = True
                            self.task.step = 4
                            W_robot[drop - 1].q2_empty = False

                case 6:
                    print(f"Pickup station {pickup} status, booking : {W_robot[pickup - 1].booked}, "
                          f"Queue1 {W_robot[pickup - 1].q1_empty}, Queue2 {W_robot[pickup - 1].q2_empty}")
                    #######To Pickup from Workstation #######
                    if 1 <= pickup <= 10 and event_toopcua.is_set() == False:

                        if (W_robot[pickup - 1].booked == False and W_robot[pickup - 1].robot_free == True) or \
                                (self.wk_loc == pickup and self.base == True):
                            self.opcua_cmd = ["pick", str(pickup - 1)]
                            self.path_clear = True
                            self.task.step = 1
                            W_robot[pickup - 1].booked = True

                        elif (W_robot[pickup - 1].booked == True or W_robot[pickup - 1].robot_free == False) and (
                                W_robot[pickup - 1].q1_empty == True):
                            self.opcua_cmd = ["q1", str(pickup - 1)]
                            self.path_clear = True
                            self.task.step = 7
                            W_robot[pickup - 1].q1_empty = False
                        elif (W_robot[pickup - 1].booked == True or W_robot[pickup - 1].robot_free == False) and (
                                W_robot[pickup - 1].q1_empty == False) \
                                and (W_robot[pickup - 1].q2_empty == True) and (self.wk_loc != pickup):
                            self.opcua_cmd = ["q2", str(pickup - 1)]
                            self.path_clear = True
                            self.task.step = 8
                            W_robot[pickup - 1].q2_empty = False

                case 10:
                    ## To Drop at Sink Station #####
                    if drop == 50 and event_toopcua.is_set() == False and Ax_station[10].booked == False:
                        self.opcua_cmd = ["sink", str(pickup - 1)]
                        self.path_clear = True
                        self.task.step = 11
                        Ax_station[10].booked = True

                case 12:
                    #Ax_station[10].product_clearance()
                    self.path_clear = True


            if event_frommain.is_set() == True and self.path_clear == True:
                event_toopcua.set()
                # await asyncio.sleep(1)
                self.exec_cmd = False
                self.path_clear = False
                # await asyncio.sleep(0.2)
                if self.wait == True:
                    wTime.calc_time()
                    self.product.tracking.append(wTime)
                    self.wait = False
                else:
                    pass
                event_frommain.clear()
            else:
                print(
                    f"Robot{self.id} at WK {self.wk_loc} awaiting for path to be cleared for task {self.task.command}")
                self.wait = True
                wTime = Waiting_time(stime=datetime.now(), etime=datetime.now(), dtime=0, pickup=pickup, drop=drop,
                                     tr_no=self.id)
                await asyncio.sleep(10)
                # for wk in W_robot:
                #     print(f"WK{wk.id}, booking {wk.booked} with q1 empty {wk.q1_empty}, q2 empty {wk.q2_empty}, "
                #           f"robot_Free {wk.robot_free}, product_free {wk.product_free}")

                wTime.stop_timer()
                pass

    async def sendtoOPCUA(self, event_fromchkpath: asyncio.Event):
        while True:
            await event_fromchkpath.wait()
            cmd = self.opcua_cmd
            self.Free = False
            data = [cmd, self.id, self.new_prod]
            q_robot_to_opcua.put_nowait(data)
            print(f"Sub-task command {cmd} entered in opcua queue for robot {self.id}")
            event_fromchkpath.clear()

    async def execution_timer(self, event_main: asyncio.Event, event_init_task: asyncio.Event,
                              loop: asyncio.AbstractEventLoop):
        while True:
            await event_main.wait()
            print(f'Robot {self.id} execution timer has started')
            ## Clearance of booking of current location ####
            if 1 <= self.wk_loc <= 10:
                if self.base == True:
                    W_robot[self.wk_loc - 1].booked = False
                elif self.q1 == True:
                    W_robot[self.wk_loc - 1].q1_empty = True
                elif self.q2 == True:
                    W_robot[self.wk_loc - 1].q2_empty = True
            elif 11 <= self.wk_loc <= 20:
                Ax_station[self.wk_loc - 11].booked = False
                print(f" Source station {Ax_station[self.wk_loc - 11]} unbooked")
            elif self.wk_loc == 50:
                Ax_station[10].booked = False

            ## Clear Workstation queue flags ####

            start_time = datetime.now()
            tTime = Transfer_time(stime=datetime.now(), etime=datetime.now(), dtime=0, pickup=self.task.command[0],
                                  drop=self.task.command[1], tr_no=self.id)
            print(f"Robot {self.id} started executing at {start_time}")
            while event_main.is_set() == True:
                # await asyncio.sleep(0)
                if data_opcua["rob_busy"][self.id - 1] == False:
                    break
                else:
                    continue
            Events["rob_execution"][self.id - 1] = False
            self.executing = False
            exec_time = (datetime.now() - start_time).total_seconds()
            print(f"Robot {self.id} took {exec_time:,.2f} seconds to run")
            self.wk_loc = int(self.opcua_cmd[1]) + 1
            if self.opcua_cmd[0] == "pick" or "drop" or "sink":
                self.base = True
                self.q1 = False
                self.q2 = False
            elif self.opcua_cmd[0] == "q1":
                self.base = False
                self.q1 = True
                self.q2 = False
            elif self.opcua_cmd[0] == "q2":
                self.base = False
                self.q1 = False
                self.q2 = True
            print(f"Robot {self.id} is at Station {self.wk_loc}")
            print(f"Task Step value is {self.task.step}")
            # self.locate_robot()
            match self.task.step:
                case 1:
                    # loop.call_soon_threadsafe(event_init_task.set())
                    if self.task.command[1] == 50:
                        self.task.step = 10
                    else:
                        self.task.step = 2
                    self.exec_cmd = True
                    print(f"Robot{self.id} picked up the product and will movie to drop wk")
                    if 1 <= self.task.command[0] <= 10:
                        W_robot[self.wk_loc - 1].product_free = True
                    # print(f"Robot {self.id} will move to drop workstation")
                    opcua_cmd_event(id=self.id, loop=loop)

                case 3:
                    # event_chkpath.set()
                    print(f"Robot{self.id} at Drop {self.wk_loc} queue1 position")
                    self.task.step = 2
                    if self.q1 == True:
                        W_robot[self.wk_loc - 1].q1_empty = True
                    elif self.q2 == True:
                        W_robot[self.wk_loc - 1].q2_empty = True
                    self.exec_cmd = True
                    opcua_cmd_event(id=self.id, loop=loop)

                case 4:
                    # event_chkpath.set()
                    print(f"Robot{self.id} at Drop {self.wk_loc} queue2 position")
                    self.task.step = 2
                    self.exec_cmd = True
                    opcua_cmd_event(id=self.id, loop=loop)

                case 5:
                    self.free = True
                    W_robot[self.wk_loc - 1].assingedProduct = self.product
                    print(f"Robot{self.id} at Drop workstation")
                    self.assigned_task = False
                    W_robot[self.wk_loc - 1].q1_empty = True
                    W_robot[self.wk_loc - 1].q2_empty = True
                    ##NEW implementation for saturating products####
                    new_task_list = generate_task(order=production_order)
                    # print("Generated TASK from new function", new_task_list)
                    new_product = GreedyScheduler.robot_done(product=self.product, product_tList=new_task_list)
                    if new_product != None:
                        q_product_done.put_nowait(new_product)
                        # print("No new product to generate")
                    else:
                        pass
                    wk_process_event(wk=self.task.command[1], loop=loop)

                case 7:
                    # event_chkpath.set()
                    print(f"Robot{self.id} at pickup {self.wk_loc} queue1 workstation")
                    self.task.step = 6
                    self.exec_cmd = True
                    # W_robot[self.wk_loc - 1].q2_empty = True
                    opcua_cmd_event(id=self.id, loop=loop)

                case 8:
                    # event_chkpath.set()
                    print(f"Robot{self.id} at pickup {self.wk_loc} queue2 workstation")
                    self.task.step = 6
                    self.exec_cmd = True
                    opcua_cmd_event(id=self.id, loop=loop)

                case 11:
                    print(f"Robot{self.id} at Sink Station")
                    print(f"Product moved to sink node")
                    st = Sink(tstamp=datetime.now())
                    self.product.tracking.append(st)
                    self.assigned_task = False
                    #self.free = True
                    self.finished_product = self.product
                    print(f"Robot {self.id} unloaded completed product {self.product} to Sink")
                    #self.base_move = True
                    self.opcua_cmd = ["base", "99"]
                    data = [self.opcua_cmd, self.id, self.new_prod]
                    q_robot_to_opcua.put_nowait(data)
                    self.task.step = 12
                    Ax_station[10].sink_station(self.product)
                    Ax_station[10].booked = False
                    print(f"Robot moving to Base Station")
                    self.exec_cmd = True
                    opcua_cmd_event(id=self.id, loop=loop)


                case 12:
                    await asyncio.sleep(15)
                    print(f"Robot {self.id} ")
                    self.free = True
                    self.base_move = False
                    self.wk_loc = 99

            event_main.clear()

    async def execution_time(self, event, loop: asyncio.AbstractEventLoop):
        while True:
            # print(f'waiting for robot {id} for  execution')
            await event.wait()
            t = self.task.command
            print(f'Robot {self.id} execution tim'
                  f'er has started')
            start_time = datetime.now()
            tTime = Transfer_time(stime=datetime.now(), etime=datetime.now(), dtime=0, pickup=self.task.command[0],
                                  drop=self.task.command[1], tr_no=self.id)
            print(f"Robot {self.id} started executing at {start_time}")

            while event.is_set() == True:
                await asyncio.sleep(1)
                if data_opcua["rob_busy"][self.id - 1] == False:
                    break
                else:
                    continue
            # await event2.wait()
            Events["rob_execution"][self.id - 1] = False
            exec_time = (datetime.now() - start_time).total_seconds()
            print(f"Robot {self.id} took {exec_time:,.2f} seconds to run")
            await asyncio.sleep(1)
            # print(f"the product is delivered to workstation {t[1]} by robot {self.id}")
            # for wk, wk_loc in enumerate(data_opcua["machine_pos"]):
            #     dist = distance.euclidean(wk_loc, data_opcua["robot_pos"][self.id - 1])
            #     print("Distance to target position is:", dist)
            #     if dist <= 800:
            #         self.wk_loc = wk + 1
            #     elif dist > 800:
            #         self.wk_loc = 99
            #         print("Error: Robot at unknown position")
            # self.wk_loc = t[1]
            print(f"Robot {self.id} is at Workstation {self.wk_loc}")
            W_robot[t[1] - 1].product_free = False
            W_robot[t[1] - 1].robot_free = False
            if t[1] <= 11:  ### if Task for normal workstation#####
                print(f"the product is delivered to workstation {t[1]} by robot {self.id}")
                print(f"Robot {self.id} is at {self.wk_loc}")
                wk = t[1] - 1
                W_robot[wk].assingedProduct = self.product
                print(f"Robot {self.id} assigned product to Workstation{t[1]} is {self.product}")
                ### self Product deassign ####
                self.assigned_task = False
                self.assigned_task = False
                self.free = True
                print(f"The robot {self.id} is Product and Task free")
                tTime.calc_time()
                self.product.tracking.append(tTime)
                wk_process_event(wk=t[1], loop=loop)
                ##NEW implementation for saturating products####
                new_task_list = generate_task(order=production_order)
                print("Generated TASK from new function", new_task_list)
                new_product = GreedyScheduler.robot_done(product=self.product, product_tList=new_task_list)
                if new_product != None:
                    q_product_done.put_nowait([new_product])
                else:
                    pass
                event.clear()

            else:  ### If task for Sink node#####
                print(f"Product moved to sink node")
                st = Sink(tstamp=datetime.now())
                self.product.tracking.append(st)
                ### self task deassign####
                if self.base_move == False:
                    self.assigned_task = False
                    self.free = True
                    self.finished_product = self.product
                    print(f"Robot {self.id} unloaded completed product {self.product} to Sink")
                    self.base_move = True
                    cmd = []
                    if self.id == 1:
                        cmd = ['m,-1644,-3211,0', '', '']
                    elif self.id == 2:
                        cmd = ['', 'm,-1575,455,0', '']
                    elif self.id == 3:
                        cmd = ['', '', 'm,-1711,5033,0']
                    ### move to base station #####
                    data_opcua["mobile_manipulator"] = cmd
                    await asyncio.sleep(2)
                    data_opcua["mobile_manipulator"] = ["", "", ""]
                    print(f"Robot moving to Base Station")
                elif self.base_move == True:
                    W_robot[11].product_clearance()
                    await asyncio.sleep(15)
                    print(f"Robot reached Base Station")
                    self.free = True
                    self.base_move = False
                    self.wk_loc = 99  ### 0 --> Base/arbitrary location for
                    W_robot[11].sink_station(self.product)
                    event.clear()

    async def direct_exec_channel(self, task, product, cmd):
        if task["command"][1] == 12:
            c = str(task["command"][0]) + "," + str("s")
        else:
            c = str(task["command"][0]) + "," + str(task["command"][1])
        cmd.insert((int(self.id) - 1), c)
        if task["command"][0] == 11:
            data_opcua["create_part"] = task["pV"]
            # write_opcua(task["pV"], "create_part", None)
            await asyncio.sleep(0.7)
            print(f"part created for robot {self.id},", task["pV"])
            data_opcua["create_part"] = 0
            await asyncio.sleep(0.7)
            data_opcua["mobile_manipulator"] = cmd
            await asyncio.sleep(0.7)
            data_opcua["mobile_manipulator"] = ["", "", ""]
            print("command sent to opcuaclient", cmd)
        else:
            data_opcua["mobile_manipulator"] = cmd
            await asyncio.sleep(0.7)
            data_opcua["mobile_manipulator"] = ["", "", ""]
            # data_opcua["robot_exec"][self.id - 1] = False
            # data_opcua["rob_busy"][self.id - 1] = True
            W_robot[task.command[0] - 1].product_clearance()


class Workstation_robot:

    def __init__(self, wk_no, order, product: Product):
        self.id = wk_no
        self.process_done = True
        self.order = order
        # self.assigned_prod = False
        self.assingedProduct = product
        self.done_product = Product
        self.product_free = True
        self.robot_free = True
        self.booked = False
        self.capability = []
        self.q1_empty = True
        self.q2_empty = True

    def __await__(self):
        async def closure():
            # print("await")
            return self

        return closure().__await__()

    def product_clearance(self):
        self.product_free = True
        self.robot_free = True
        self.booked = False
        print(f"The workstation {self.id} is Product Free")

    async def process_execution(self, event):
        while True:
            await asyncio.sleep(2)
            print(f"Workstation {self.id} execution task re-initialized")
            await event.wait()
            print(f" Workstation ID {self.id}")
            process_time = production_order["Process_times"][self.assingedProduct.pv_Id - 1][self.id - 1]
            # process_time = 20
            #print(f"Product received by Workstation{self.id} is {self.assingedProduct}")
            self.process_done = False
            self.product_free = False
            print(f"Process task executing at workstation {self.id}")
            pt = Process_time(stime=datetime.now(), etime=datetime.now(), dtime=0, wk_no=self.id)
            await asyncio.sleep(process_time)
            print(f"Process task on workstation {self.id} finished")
            self.assingedProduct.task_list.pop(0)
            # print(f"Current process task removed from product {self.product.pv_Id,self.product.pi_Id}")
            print(f"Done workstation {self.id}")
            self.process_done = True
            print(f"The Workstation {self.id} free status is {self.process_done}")
            print("done product", self.done_product)
            pt.calc_time()
            self.assingedProduct.tracking.append(pt)
            self.assingedProduct.released = True
            ### Remove current from product###
            self.assingedProduct.released = True
            self.done_product = self.assingedProduct
            # a = [self.done_product]
            q_product_done.put_nowait(self.done_product)
            print(f"Product {self.done_product} added into done queue")
            event.clear()


class Auxillary_station:

    def __init__(self, stn_no, order, product: Product):
        self.id = stn_no
        self.order = order
        self.product = product
        self.product_free = True
        self.robot_free = True
        self.booked = False

    def source_station(self, product):
        return None

    def sink_station(self, product):
        new_task_list = generate_task(order=production_order)
        print("Generated TASK from new function", new_task_list)
        new_product = GreedyScheduler.prod_completed(product=product, product_tList=new_task_list)
        q_product_done.put_nowait([new_product])

    def product_clearance(self):
        self.product_free = True
        self.robot_free = True
        self.booked = False
        print(f"The Sink Station {self.id} is Free")
