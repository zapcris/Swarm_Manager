import asyncio
import math
from datetime import datetime
# from scipy.spatial import distance
from Reactive_10Robots.SM04_Task_Planning_agent import generate_task
from Reactive_10Robots.SM10_Product_Task import Product, Task, Transfer_time, Waiting_time, Sink, Process_time

#### Initialization data###############

# production_order = {}

null_product = Product(pv_Id=0, pi_Id=0, mission_list=[], inProduction=False, finished=False, last_instance=0, robot=99,
                       wk=0, released=False, tracking=[], priority=1, current_mission=[], task=[])
null_Task = Task(id=0, type=0, command=[], pV=0, pI=0, allocation=False, status="null", robot=99, step=0)

p1 = Product(pv_Id=1, pi_Id=1, mission_list=[[11, 1], [2, 5]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False, tracking=[], priority=1, current_mission=[], task=[])
p2 = Product(pv_Id=1, pi_Id=1, mission_list=[[11, 2], [2, 8]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False, tracking=[], priority=1, current_mission=[], task=[])
p3 = Product(pv_Id=1, pi_Id=1, mission_list=[[11, 3], [3, 6]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False, tracking=[], priority=1, current_mission=[], task=[])
test_task = Task(id=1, type=1, command=[11, 1], pV=1, pI=1, allocation=False, status="null", robot=1, step=0)

test_product = [p1, p2, p3]

# ## Test Production Order
production_order = {
    "Name": "Test",
    "PV": [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    "PV_priority": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "sequence": [[11, 1, 2, 3, 4, 5, 50],  # [11, 1, 7, 5, 6, 8, 9, 12]
                     [12, 2, 3, 4, 5, 6, 50],  # [11, 2, 6, 6, 8, 12]
                     [13, 3, 4, 5, 6, 7, 50],
                     [14, 4, 5, 6, 7, 8, 50],  # [11, 4, 8, 12, 9, 12]
                     [15, 5, 6, 7, 8, 9, 10, 50],
                     [16, 1, 5, 7, 8, 10, 50],
                     [17, 2, 6, 8, 9, 50],
                     [18, 3, 7, 9, 2, 50],
                     [19, 4, 8, 3, 2, 10, 50],
                     [20, 5, 3, 7, 10, 1, 50]
                     ],
    # "sequence": [[11, 1, 2, 3, 4, 5, 50],  # [11, 1, 7, 5, 6, 8, 9, 12]
    #              [12, 2, 3, 50],  # [11, 2, 6, 6, 8, 12]
    #              [13, 3, 4, 50],
    #              [14, 4, 5, 50],  # [11, 4, 8, 12, 9, 12]
    #              [15, 5, 7, 50],
    #              [16, 6, 8, 50],
    #              [17, 7, 8, 50],
    #              [18, 8, 9, 50],
    #              [19, 9, 10, 50],
    #              [20, 10, 50]
    #              ],
    "PI": [2, 2, 2, 2, 2, 1, 1, 1, 1, 1],
    "Wk_type": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "WK_capabilities": [[1],
                        [2],
                        [3],
                        [4],
                        [5],
                        [6],
                        [7],
                        [8],
                        [9],
                        [10]
                        ],
    "Process_times": [[10, 10, 20, 10, 15, 20, 15, 20, 10, 20],  # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                      [10, 10, 20, 10, 15, 20, 15, 20, 10, 20],  # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [10, 10, 20, 10, 15, 20, 15, 20, 10, 20],  # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                      [10, 10, 20, 10, 15, 20, 15, 20, 10, 20],
                      [10, 10, 20, 10, 15, 20, 15, 20, 10, 20],
                      [10, 10, 20, 10, 15, 20, 15, 20, 10, 20],
                      [10, 10, 20, 10, 15, 20, 15, 20, 10, 20],
                      [10, 10, 20, 10, 15, 20, 15, 20, 10, 20],
                      [10, 10, 20, 10, 15, 20, 15, 20, 10, 20],
                      [10, 10, 20, 10, 15, 20, 15, 20, 10, 20]
                      ]
}

random_sequence = [[11, 1, 5, 7, 8, 10, 50],  # [11, 1, 7, 5, 6, 8, 9, 12]
                   [12, 2, 6, 8, 9, 50],  # [11, 2, 6, 6, 8, 12]
                   [13, 3, 7, 9, 2, 50],
                   [14, 4, 8, 3, 2, 10, 50],  # [11, 4, 8, 12, 9, 12]
                   [15, 5, 3, 7, 10, 1, 50],
                   [16, 2, 5, 7, 3, 50],
                   [17, 3, 6, 8, 2, 4, 3, 50],
                   [18, 8, 5, 7, 50],
                   [19, 7, 4, 1, 50],
                   [20, 5, 4, 9, 50]
                   ],

combined_sequence = [[11, 1, 2, 3, 4, 5, 50],  # [11, 1, 7, 5, 6, 8, 9, 12]
                     [12, 2, 3, 4, 5, 6, 50],  # [11, 2, 6, 6, 8, 12]
                     [13, 3, 4, 5, 6, 7, 50],
                     [14, 4, 5, 6, 7, 8, 50],  # [11, 4, 8, 12, 9, 12]
                     [15, 5, 6, 7, 8, 9, 10, 50],
                     [16, 1, 5, 7, 8, 10, 50],
                     [17, 2, 6, 8, 9, 50],
                     [18, 3, 7, 9, 2, 50],
                     [19, 4, 8, 3, 2, 10, 50],
                     [20, 5, 3, 7, 10, 1, 50]
                     ],

old_process_times = [[10, 10, 20, 10, 15, 14, 15, 12, 10, 10],  # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                     [10, 30, 20, 10, 45, 14, 15, 12, 10, 10],  # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                     [15, 10, 20, 10, 15, 14, 15, 12, 10, 30],  # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                     [20, 30, 40, 50, 20, 40, 10, 70, 30, 10],
                     [20, 30, 40, 10, 20, 10, 20, 10, 10, 10],
                     [20, 30, 40, 30, 20, 40, 80, 70, 30, 60],
                     [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                     [20, 30, 40, 30, 20, 40, 10, 70, 30, 10],
                     [20, 30, 40, 50, 20, 40, 10, 70, 30, 10],
                     [20, 30, 40, 20, 20, 40, 10, 70, 30, 10]
                     ]

linear_sequence = [[11, 1, 2, 3, 4, 5, 50],  # [11, 1, 7, 5, 6, 8, 9, 12]
                   [12, 2, 3, 50],  # [11, 2, 6, 6, 8, 12]
                   [13, 3, 4, 50],
                   [14, 4, 5, 50],  # [11, 4, 8, 12, 9, 12]
                   [15, 5, 7, 50],
                   [16, 6, 8, 50],
                   [17, 7, 8, 50],
                   [18, 8, 9, 50],
                   [19, 9, 10, 50],
                   [20, 10, 50]
                   ],

WK_capabilities = [[1, 3],  ##[[1, 3],
                   [2, 4],  ##[2, 4],
                   [3, 8],  ##[3, 8],
                   [4, 9],  ##[4, 9],
                   [5, 1],  ##[5, 1],
                   [6, 3],  ##[6, 3],
                   [7, 4],  ##[7, 4],
                   [8, 2],  ##[8, 2],
                   [9, 1],  ##[9, 1],
                   [10, 5]  ##[10, 5]
                   ],

wk_cap_2 = [[1, 3, 6],
            [2, 4, 7],
            [3, 8, 9],
            [4, 9, 2],
            [5, 1, 7],
            [6, 3, 1],
            [7, 4, 6],
            [8, 2, 1, 9],
            [9, 1, 5],
            [10, 5, 7]
            ],


def read_order(reconfig_doc):
    production_order["Name"] = "Test"
    production_order["PV"] = [1 if i == True else 0 for i in reconfig_doc["Product_active"]]
    production_order["sequence"] = reconfig_doc["Production_Sequence"]
    production_order["PI"] = reconfig_doc["Production_volume"]
    production_order["Wk_type"] = reconfig_doc["WK_type"]
    production_order["PV_priority"] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    production_order["WK_capabilities"] = reconfig_doc["WK_capabilities"]
    production_order["Process_times"] = reconfig_doc["Process_times"]

    print("Name", production_order["Name"])
    print("Products", production_order["PV"])
    print("Volume", production_order["PI"])
    print("Sequence", production_order["sequence"])
    for times in production_order["Process_times"]:
        print(times)


multi_capability = [[1, 3, 6],
                    [2, 4, 7],
                    [3, 8, 9],
                    [4, 9, 2],
                    [5, 1, 7],
                    [6, 3, 1],
                    [7, 4, 6],
                    [8, 2, 1, 9],
                    [9, 1, 5],
                    [10, 5, 7]
                    ]


################################# Taken from Robot_Agent###############################################################


#################################### Robot agent code ################################################


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
        self.q3 = False
        self.event_toopcua = False
        self.event_frommain = False
        self.anchor = False
        # self.waitTime = Waiting_time(stime=datetime.now(), etime=datetime.now(), dtime=0, pickup=99, drop=99,
        #                              tr_no=self.id)
        # print("The values of workstation positions are", self.machine_pos)

    def __await__(self):
        async def closure():
            # print("await")
            return self

        return closure().__await__()

    def bid(self, auctioned_task, data_opcua):
        bid_value = 0.0
        task_cost = 0.0
        marginal_cost = 0.0
        machine_pos = [[3569, 5526], [11989, 5176], [5401, -1414], [14936, -1658], [25615, -2503], [3077, 12153],
                       [15434, 16900], [12432, 10650], [22123, 10581], [27500, 3630]]
        # print("The broadcasted task is", auctioned_task)

        start_loc = auctioned_task[0]
        end_loc = auctioned_task[1]
        # total_ws = len(data_opcua["machine_pos"])
        # print("Bid started", start_loc, end_loc)

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
        elif start_loc == 16:  ## if source node
            start_pos = [-6000, -12000]
        elif start_loc == 17:  ## if source node
            start_pos = [-6000, -14000]
        elif start_loc == 18:  ## if source node
            start_pos = [-6000, -16000]
        elif start_loc == 19:  ## if source node
            start_pos = [-6000, -18000]
        elif start_loc == 20:  ## if source node
            start_pos = [-6000, -20000]
        else:
            # start_pos = data_opcua["machine_pos"][start_loc - 1]
            # print("Check this error", start_loc)
            # print(len(self.machine_pos))
            start_pos = self.machine_pos[start_loc - 1]

        # print("Start_position", start_pos)
        if end_loc == 50:  ## if source node or sink node
            end_pos = [24517, 11716]  ### position of sink node
        else:
            # end_pos = data_opcua["machine_pos"][end_loc - 1]
            end_pos = self.machine_pos[end_loc - 1]

            # print("Target position values", end_pos)
        # print("End_position", end_pos)
        # print("Start position values", start_pos)
        # print("Target position values", end_pos)
        task_cost = math.dist(start_pos, end_pos)
        # print("Cleared bid mid-function")
        # if self.data_opcua["rob_busy"][self.id-1] == False :
        # print(f"Robot bid ID {self.id}")
        # print(data_opcua["robot_pos"])
        if self.free == True and data_opcua["rob_busy"][self.id - 1] == False:
            # marginal_cost = math.dist(start_pos, data_opcua["robot_pos"][self.id - 1])
            marginal_cost = math.dist(start_pos, data_opcua["robot_pos"][self.id - 1])
        else:
            marginal_cost = 9999999
        bid_value = int(marginal_cost)
        print(
            f"Robot {self.id} Free Status: {self.free} and busy status {data_opcua["rob_busy"][self.id - 1]} at position {data_opcua["robot_pos"][self.id - 1]} and auctioned task is {auctioned_task}")
        print(
            f"Bid submitted by Robot {self.id} for task {auctioned_task} is {bid_value} with workstation position {start_pos}")
        return bid_value

    def trigger_task(self, task):
        self.task = task
        self.exec_cmd = True
        self.free = False

        # print(f"Task triggered to robot {self.id} and execution status is {self.exec_cmd}")

    async def initiate_task(self, q_initiate_task: asyncio.Queue, W_robot, Ax_station, q_trigger_cmd: asyncio.Queue):
        while True:

            task_opcua = await q_initiate_task.get()
            print(f"Robot{self.id} received task {task_opcua}")
            print(task_opcua)
            # self.anchor = False
            # print(f"Robot{self.id} activated")
            self.event_frommain = True
            # print(f"Robot {self.id} task initiated")
            self.task_initiated = True
            # self.task_step += 1
            # print(f"OPCUA command initiated at robot {self.id}")
            pickup = self.task.command[0]
            drop = self.task.command[1]
            self.new_prod = self.task.pV
            # print(self.task.step)
            # print(f"Task Step value is {self.task.step}")
            match self.task.step:
                case 1:  ### Start New task cycle on robot
                    # print("Case1 activated", pickup, self.event_toopcua, Ax_station[
                    #    pickup - 11].booked)
                    ########Pickup part from source position########
                    if self.id not in Ax_station[pickup - 11].wait_q:
                        Ax_station[pickup - 11].wait_q.append(self.id)
                    else:
                        print(f"Robot {self.id} already queued for source part {pickup}")
                    if 11 <= pickup <= 20 and self.event_toopcua == False and Ax_station[
                        pickup - 11].booked == False and Ax_station[pickup - 11].wait_q[0] == self.id:
                        self.opcua_cmd = ["pick", str(pickup - 1)]
                        self.path_clear = True
                        self.task.step = 2
                        Ax_station[pickup - 11].booked = True
                        Ax_station[pickup - 11].wait_q.pop(0)  ## clear queue entry

                    # elif 1 <= pickup <= 10 and W_robot[pickup - 1].robot_free == True:
                    #     self.task.step = 7
                    # print(
                    #    f" Path clearance condition 2 activated for robot {self.id} for task{self.task.command}")

                case 3:  ##Robot at source pickup and ready for drop to workstation
                    robot = (production_order["PV_priority"][self.product.pv_Id - 1], self.id)
                    queue_pos = 0
                    ##Check for position of robot in the process queue###
                    if self.id not in W_robot[drop - 1].pqueue:
                        W_robot[drop - 1].pqueue.append(self.id)
                        print(f" Workstation {drop} Queue updated {W_robot[drop - 1].pqueue}")
                        print(f"Robot Inserted in workstation {drop} queue")
                    else:
                        print(f"Robot {self.id} already in workstation {drop} queue")

                    if self.id in W_robot[drop - 1].pqueue:
                        queue_pos = W_robot[drop - 1].pqueue.index(self.id) + 1
                    if queue_pos >= 4:
                        self.q3 = True

                    ### New logic to shuffle order of queue based on priority####

                    ##Check for Robots queue in workstation's process queue
                    # if queue_pos == 1 or (not W_robot[drop - 1].pqueue and (self.q1 or self.q2)):
                    if queue_pos == 1 or (queue_pos == 2 and self.q1 == True):
                        print(f"Robot {self.id} queued for workstation {drop} base")
                        print(f"Status WK_book {W_robot[drop - 1].booked}")
                        print(f"Status WK_Product_Free {W_robot[drop - 1].product_free}")
                        print(f"Status WK_Robot_Free {W_robot[drop - 1].robot_free}")
                        print("Workstation queue", W_robot[drop - 1].pqueue)
                        if W_robot[drop - 1].booked == False and W_robot[drop - 1].product_free == True and \
                                W_robot[drop - 1].robot_free == True:
                            W_robot[drop - 1].booked = True
                            self.opcua_cmd = ["drop", str(drop - 1)]
                            self.path_clear = True
                            print("Path cleared for base position")
                            ## Remove from the queue as soon the task is cleared###
                            # W_robot[drop - 1].pqueue.pop(0)
                            self.task.step = 4  ##robot cleared for move to drop base workstation####

                    'Allow Robot to move to second queue'
                    'Case:1 when robot id is 2nd in process queue'
                    'Case:2 when robot id is 3rd in wait queue'
                    if queue_pos == 2 or (queue_pos == 3 and self.q2 == True):
                        print(f"Robot {self.id} queued for workstation {drop} Q1")
                        print(f"Status WK_Q1empty {W_robot[drop - 1].q1_empty}")
                        print(f"Status WK_Q2empty {W_robot[drop - 1].q2_empty}")
                        print("Workstation queue", W_robot[drop - 1].pqueue)
                        if W_robot[drop - 1].q1_empty == True:
                            self.opcua_cmd = ["q1", str(drop - 1)]
                            self.path_clear = True
                            print("Path cleared for Q1 position")
                            W_robot[drop - 1].q1_empty = False
                            self.task.step = 5  ##robot cleared for move to drop Q1 workstation####

                    'Allow Robot to move to second queue'
                    'Case:1 when robot id is 3rd in process queue'
                    'Case:2 when robot id is 1st in wait queue'
                    if queue_pos == 3 or (queue_pos == 4 and self.q3 == True):
                        print(f"Robot {self.id} queued for workstation {drop} Q2")
                        print(f"Status WK_Q2empty {W_robot[drop - 1].q2_empty}")
                        print("Workstation queue", W_robot[drop - 1].pqueue)
                        if W_robot[drop - 1].q2_empty == True:
                            self.opcua_cmd = ["q2", str(drop - 1)]
                            self.path_clear = True
                            print("Path cleared for Q2 position")
                            W_robot[drop - 1].q2_empty = False
                            ## wait_q removed from code
                            # if W_robot[drop - 1].wait_q:
                            #     W_robot[drop - 1].wait_q.pop(0)
                            self.task.step = 6  ##robot cleared for move to drop Q2 workstation####

                case 7:  # This case is for pickup processed product from workstations
                    print(f"Robot {self.id} is at workstation {self.wk_loc}")
                    print(f"Workstation {pickup} Robot Free status is {W_robot[pickup - 1].robot_free}")
                    if (self.wk_loc == pickup and self.base == True) or (
                            self.wk_loc != pickup and W_robot[pickup - 1].robot_free == True):
                        W_robot[pickup - 1].booked = True
                        self.opcua_cmd = ["pick", str(pickup - 1)]
                        self.path_clear = True
                        print(f"Path cleared for Robot {self.id} for pickup at workstation {pickup}")
                        self.task.step = 8  ###Clearance for task execution
                    ## Reserved case 8,9,10 for queuing pickup worksation mission###

                case 11:  ## Case for dropping product to Sink Station###
                    if self.id not in Ax_station[10].wait_q:
                        Ax_station[10].wait_q.append(self.id)
                    else:
                        print(f"Robot {self.id} already in sink queue")
                    print(f"Robot {self.id} queued for sink {Ax_station[10].wait_q}")
                    if (drop == 50 and self.event_toopcua == False and Ax_station[10].booked == False
                            and Ax_station[10].wait_q[0] == self.id):
                        self.opcua_cmd = ["sink", str(pickup - 1)]
                        self.path_clear = True
                        self.task.step = 12
                        Ax_station[10].booked = True
                        Ax_station[10].wait_q.pop(0)

                case 13:
                    ##Move to Base Station#####
                    # Ax_station[10].product_clearance()
                    self.task.step = 14
                    self.path_clear = True

            if self.event_frommain == True and self.path_clear == True:
                self.event_toopcua = True
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
                self.event_frommain = False
                run = 0
                # print(f"Robot{self.id} Path Clearance Check Finished for case {self.task.step}")
                # self.free = False
                data = [self.opcua_cmd, self.id, self.new_prod]
                # print(data)
                q_trigger_cmd.put_nowait(data)
                # print(f"Robot{self.id} Triggered OPCUA command", data)
                self.event_toopcua = False  ## Clear flag for transfer to opcua command
                q_initiate_task.task_done()
            else:
                # print(
                # f"Robot{self.id} at WK {self.wk_loc} awaiting for path to be cleared for task {self.task.command}")
                if self.wait == False:
                    wTime = Waiting_time(stime=datetime.now(), etime=datetime.now(), dtime=0, pickup=pickup, drop=drop,
                                         tr_no=self.id)
                    self.wait = True
                else:
                    pass
                await asyncio.sleep(5)
                q_initiate_task.put_nowait(task_opcua)

    async def execution_timer(self, q_executing_task: asyncio.Queue, q_done_product: asyncio.Queue,
                              q_trigger_cmd: asyncio.Queue, q_initiate_process,
                              q_initiate_task: asyncio.Queue,
                              data_opcua, GreedyScheduler, T_robot, W_robot, Ax_station):
        while True:
            await q_executing_task.get()
            # print(f'Robot {self.id} execution timer has started')
            self.executing = True
            ## Clearance of booking of current location ####
            if 1 <= self.wk_loc <= 10:
                if self.base == True and self.task.command[1] != 50:
                    W_robot[self.wk_loc - 1].booked = False
                    ##indicate robot vacating the current wk location
                    W_robot[self.wk_loc - 1].robot_free = True
                    print(
                        f"Robot{self.id} cleared wk location {self.wk_loc} with robot free {W_robot[self.wk_loc - 1].robot_free}")
                elif self.base == True and self.task.command[1] == 50:
                    ## Adding sleep to compensate delay in simulation during move to sink operation###
                    W_robot[self.wk_loc - 1].booked = False
                    # await asyncio.sleep(4)
                    W_robot[self.wk_loc - 1].robot_free = True
            elif 11 <= self.wk_loc <= 20:
                Ax_station[self.wk_loc - 11].booked = False
            # print(f" Source station {Ax_station[self.wk_loc - 11]} unbooked")
            elif self.wk_loc == 50:
                Ax_station[10].booked = False

            ## Clear Workstation queue flags ####
            start_time = datetime.now()
            tTime = Transfer_time(stime=start_time, etime=start_time, dtime=0, pickup=self.task.command[0],
                                  drop=self.task.command[1], tr_no=self.id)
            # print(f"Robot {self.id} started executing at {start_time}")

            ##Run loop until Robot is done executing
            while self.executing == True:
                # await asyncio.sleep(0)
                if data_opcua["rob_busy"][self.id - 1] == False:
                    break
                else:
                    # await for concurrency###
                    await asyncio.sleep(2)

            ### Log execution time into product's transfer time####
            if self.task.step < 12:
                tTime.calc_time()
                self.product.tracking.append(tTime)
            self.executing = False
            exec_time = (datetime.now() - start_time).total_seconds()
            # print(f"Robot {self.id} took {exec_time:,.2f} seconds to run for the task step {self.task.step}")
            self.wk_loc = int(self.opcua_cmd[1]) + 1
            # print(
            #     f"Robot {self.id} internal opcua command is {self.opcua_cmd} with product {self.product.pv_Id} {self.product.pi_Id}")
            # print(f"Robot {self.id} is at Station {self.wk_loc} with status : base {self.base}, q1 {self.q1}, q2 {self.q2}")
            # print(f"Task Step value is {self.task.step}")
            # print(self.task.step)
            match self.task.step:
                case 2:
                    ##Robot at source pickup location
                    self.task.step = 3
                    self.exec_cmd = True
                    ##Next step to load in workstation
                    q_initiate_task.put_nowait(self.task)

                case 4:
                    ##Robot loaded product at Drop Workstation Base###
                    if self.q1 == True:
                        W_robot[self.wk_loc - 1].q1_empty = True
                    self.q1 = False
                    self.base = True
                    self.q2 = False
                    self.q3 = False
                    if W_robot[self.wk_loc - 1].type == 1:
                        self.free = True
                        print(f"Robot {self.id} FREED")
                    else:
                        self.anchor = True
                        print(f"Robot {self.id} is anchored")
                    self.assigned_task = False
                    W_robot[self.wk_loc - 1].product_free = False
                    W_robot[self.wk_loc - 1].robot_free = False
                    for wks in W_robot:
                        if wks.id == self.task.command[1]:
                            q_initiate_process[wks.id - 1].put_nowait(self.product)
                            print(f"Robot{self.id} delivered to Workstation {wks.id}")
                    ## Workstation occupied when robot performing drop mission
                    # W_robot[self.wk_loc - 1].assingedProduct = self.product
                    # data = W_robot[self.wk_loc - 1].process_queue.get_nowait()
                    if W_robot[self.wk_loc - 1].type == 1:

                        ##NEW implementation for saturating products####
                        new_task_list = generate_task(order=production_order)
                        new_product = GreedyScheduler.robot_done(product=self.product, product_tList=new_task_list)
                        print(
                            f"The product status after loading by robot {self.id} in workstation {self.wk_loc}is {new_product}")

                        ### Check for new product in remaining list once product loaded into the workstation
                        if new_product == None or (new_product.pv_Id == 0 and new_product.pi_Id == 0):
                            # print("No new product to generate")
                            pass
                        else:
                            q_done_product.put_nowait(new_product)

                        # print("New product introduced byt the scheduler")
                    # data = W_robot[self.wk_loc - 1].pqueue.pop(0)
                    # print(f"The robot extracted from wk {W_robot[self.wk_loc - 1]} process queue is {data}")

                case 5:
                    ##Robot loaded with product at Drop Workstation Q1###
                    if self.q2 == True:
                        W_robot[self.wk_loc - 1].q2_empty = True
                    self.q2 = False
                    self.q1 = True
                    self.base = False
                    self.q3 = False
                    self.task.step = 3
                    self.exec_cmd = True
                    ## Send task back to task initialization routine###
                    q_initiate_task.put_nowait(self.task)

                case 6:
                    ##Robot loaded with product at Drop Workstation Q2###
                    self.base = False
                    self.q1 = False
                    self.q2 = True
                    self.q3 = False
                    self.task.step = 3
                    self.exec_cmd = True
                    ## Send task back to task initialization routine###
                    q_initiate_task.put_nowait(self.task)

                case 8:  ## Robot at pickup workstation###
                    ## Robot carrying away product from workstation now ready to dequeue###
                    W_robot[self.wk_loc - 1].pqueue.pop(0)
                    if self.q1 == True:
                        W_robot[self.wk_loc - 1].q1_empty = True
                    self.base = True
                    self.q1 = False
                    self.q2 = False
                    W_robot[self.wk_loc - 1].product_free = True
                    W_robot[self.wk_loc - 1].robot_free = False
                    if self.task.command[1] == 50:  ##if target is sink
                        self.task.step = 11
                    else:
                        self.task.step = 3
                    # await asyncio.sleep(5)  ##giving time for visual animation of pickup action
                    ## Send task back to task initialization routine###
                    self.exec_cmd = True
                    q_initiate_task.put_nowait(self.task)

                case 9:  ## Robot at pickup Q1workstation###
                    if self.q2 == True:
                        W_robot[self.wk_loc - 1].q2_empty = True
                    self.base = True
                    self.q1 = False
                    self.q2 = False
                    self.task.step = 7
                    self.exec_cmd = True
                    ## Send task back to task initialization routine###
                    q_initiate_task.put_nowait(self.task)

                case 10:  ## Robot at pickup Q2 workstation###
                    self.base = True
                    self.q1 = False
                    self.q2 = False
                    self.task.step = 7
                    self.exec_cmd = True
                    ## Send task back to task initialization routine###
                    q_initiate_task.put_nowait(self.task)

                case 12:  ## Robot at Sink Station
                    # print(f"Robot{self.id} at Sink Station")
                    # print(
                    #    f"Product {self.product.pv_Id} and Instance {self.product.pi_Id}  moved to sink node by Robot {self.id}")
                    Ax_station[10].booked = False
                    self.base = True
                    self.q1 = False
                    self.q2 = False
                    st = Sink(tstamp=datetime.now())
                    self.product.tracking.append(st)
                    self.assigned_task = False
                    self.finished_product = self.product
                    # print(f"Robot {self.id} unloaded completed product {self.product} to Sink")
                    self.opcua_cmd = ["base", "99"]
                    data = [self.opcua_cmd, self.id, self.new_prod]
                    q_trigger_cmd.put_nowait(data)
                    sink_task_list = generate_task(order=production_order)
                    sink_product = GreedyScheduler.prod_completed(product=self.product, product_tList=sink_task_list)
                    if sink_product == None or (sink_product.pv_Id == 0 and sink_product.pi_Id == 0):
                        # print("No new product to generate")
                        pass
                    else:
                        q_done_product.put_nowait(sink_product)
                        # print("No new product to generate")
                        pass
                    self.task.step = 13
                    # print(f"Robot {self.id} moving to Base Station")
                    self.exec_cmd = True
                    #########opcua_cmd_event(id=self.id, loop=loop)
                    q_initiate_task.put_nowait(self.task)

                case 14:
                    ##Robot at Base Station####
                    self.free = True
                    self.wk_loc = 99
                    # if all(robot.wk_loc == 99 for robot in T_robot):
                    #     GreedyScheduler.production_end()
                    ## Check if all products are finished to generate results###
                    GreedyScheduler.production_end()
                    self.task.step = 15
                    # self.task = null_Task  ## Clear Task after drop operation###

            q_executing_task.task_done()


class Workstation_robot:

    def __init__(self, wk_no, order, product: Product):
        self.id = wk_no
        self.process_done = True
        self.order = order
        # self.assigned_prod = False
        self.assingedProduct = product
        self.done_product = Product
        self.type = order["Wk_type"][self.id - 1]
        self.product_free = True
        self.robot_free = True
        self.booked = False
        self.capability = order["WK_capabilities"][self.id - 1]
        self.q1_empty = True
        self.q2_empty = True
        self.processing = False
        self.pqueue = []
        # self.wait_q = []

    def __await__(self):
        async def closure():
            # print("await")
            return self

        return closure().__await__()

    # def product_clearance(self):
    #     self.product_free = True
    #     self.robot_free = True
    #     self.booked = False
    #     # print(f"The workstation {self.id} is Product Free")

    async def process_execution(self, q_initiate_process: asyncio.Queue, q_done_product: asyncio.Queue, T_robot,
                                GreedyScheduler, q_initiate_task):
        while True:
            # await asyncio.sleep(2)
            # print(f"Workstation {self.id} execution task re-initialized")
            rob_product = await q_initiate_process.get()
            # print("Received data from robot on Workstation", prod)
            # print(f" Workstation ID {self.id}")
            self.assingedProduct = rob_product
            ##process_time = production_order["Process_times"][self.assingedProduct.pv_Id - 1][self.id - 1]
            ## New process time as per the process number ###
            process_no = self.assingedProduct.current_mission[1]
            print(f"Current Process to be performed on workstation {self.id} is {process_no}")
            process_time = production_order["Process_times"][self.assingedProduct.pv_Id - 1][process_no - 1]
            # process_time = 20
            # print(f"Product received by Workstation{self.id} is {self.assingedProduct}")
            self.process_done = False
            self.product_free = False
            # print(f"Process task executing at workstation {self.id}")
            pt = Process_time(stime=datetime.now(), etime=datetime.now(), dtime=0, wk_no=self.id)
            self.processing = True
            await asyncio.sleep(process_time)
            ### Remove robot from queue only when product is processed and ready to be moved ########
            # data = self.pqueue.pop(0)
            # print(f"Workstation {self.id} removed robot {data} from the process queue")
            self.processing = False
            print(f"Process task on workstation {self.id} finished")
            ### Decrement task inside product object after successful process execution###
            # self.assingedProduct.mission_list.pop(0)
            self.assingedProduct.process_done(wk_id=self.id)
            # print(f"Current process task removed from product {self.product.pv_Id,self.product.pi_Id}")
            # print(f"Done workstation {self.id}")
            self.process_done = True
            # print(f"The Workstation {self.id} free status is {self.process_done}")
            # print("done product", self.done_product)
            pt.calc_time()
            self.assingedProduct.tracking.append(pt)
            self.assingedProduct.released = True
            ##Check if the next mission for product is satisfied by the same Workstation####
            next_process = self.assingedProduct.current_mission[1]
            if next_process in self.capability and next_process != 50:
                print(f"Next Process {next_process} found in self workstation {self.id}")
                q_initiate_process.put_nowait(self.assingedProduct)
            else:
                print(f"Next Process {next_process} for product at wk {self.id} sent for allocation")
                self.done_product = self.assingedProduct
                # a = [self.done_product]
                if self.type == 1:
                    q_done_product.put_nowait(self.done_product)
                # print(f"Product {self.done_product} added into done queue")
                else:
                    ## Assign the product and Task to the anchored robot
                    task, product = GreedyScheduler.normalized_production(new_product=self.assingedProduct,
                                                                          W_robot=None)
                    for robot in T_robot:
                        ## check for workstation anchored on the workstations###
                        if robot.wk_loc == self.id and robot.anchor == True and robot.base == True:
                            T_robot[robot.id - 1].assigned_task = True
                            T_robot[robot.id - 1].task = task
                            T_robot[robot.id - 1].free = False
                            print(f"Task {task} Allocated to robot {robot.id}")
                            T_robot[robot.id - 1].product = product
                            T_robot[robot.id - 1].trigger_task(task=task)
                            q_initiate_task[robot.id - 1].put_nowait(task)
                            T_robot[robot.id - 1].anchor = False
                        else:
                            print(f"Robot not found anchored or at workstation")
                # event.clear()
                q_initiate_process.task_done()


class Auxillary_station:

    def __init__(self, stn_no, order, product: Product):
        self.id = stn_no
        self.order = order
        self.product = product
        self.product_free = True
        self.robot_free = True
        self.booked = False
        self.wait_q = []

    def source_station(self, product):
        return None

    def product_clearance(self):
        self.product_free = True
        self.robot_free = True
        self.booked = False
        # print(f"The Sink Station {self.id} is Free")
