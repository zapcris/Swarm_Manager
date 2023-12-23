import asyncio
from datetime import datetime
from scipy.spatial import distance
from Reactive_10Robots.SM04_Task_Planning_agent import generate_task
from Reactive_10Robots.SM10_Product_Task import Product, Task, Transfer_time, Waiting_time, Sink, Process_time

production_order = {
    "Name": "Test",
    "PV": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "sequence": [[11, 1, 5, 7, 8, 10, 50],  # [11, 1, 7, 5, 6, 8, 9, 12]
                 [12, 1, 6, 50],  # [11, 2, 6, 6, 8, 12]
                 [13, 7, 9, 50],
                 [14, 4, 8, 50],  # [11, 4, 8, 12, 9, 12]
                 [15, 10, 9, 50],
                 [16, 2, 5, 7, 3, 50],
                 [17, 3, 6, 8, 2, 4, 3, 50],
                 [18, 4, 5, 3, 7, 50],
                 [19, 3, 4, 1, 8, 9, 50],
                 [20, 2, 4, 5, 7, 9, 50]
                 ],
    "PI": [1, 2, 1, 2, 2, 1, 1, 1, 1, 1],
    "Wk_type": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Process_times": [[10, 10, 20, 10, 15, 14, 15, 12, 10, 10],  # [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
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
}

# Events = {
#     "brand": "Ford",
#     "rob_execution": [False, False, False],
#     "rob_mission": ["", "", ""],
#     "rob_product": [[int, int], [int, int], [int, int]],
#     "machine_status": [False for stat in range(10)],
#     "machine_product": [[int, int] for product in range(10)],
#     "elapsed_time": [int for et in range(10)],
#     "Product_finished": []
#
# }

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


# q_robot_to_opcua = asyncio.Queue()
# q_product_done = asyncio.Queue()
# q_task_wait = asyncio.Queue()

null_product = Product(pv_Id=0, pi_Id=0, mission_list=[], inProduction=False, finished=False, last_instance=0, robot=99,
                       wk=0, released=False, tracking=[])
null_Task = Task(id=0, type=0, command=[], pV=0, pI=0, allocation=False, status="null", robot=99, step=0)

p1 = Product(pv_Id=1, pi_Id=1, mission_list=[[11, 1], [2, 5]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False, tracking=[])
p2 = Product(pv_Id=1, pi_Id=1, mission_list=[[11, 2], [2, 8]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False, tracking=[])
p3 = Product(pv_Id=1, pi_Id=1, mission_list=[[11, 3], [3, 6]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False, tracking=[])
test_task = Task(id=1, type=1, command=[11, 1], pV=1, pI=1, allocation=False, status="null", robot=1, step=0)

test_product = [p1, p2, p3]


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
        self.event_toopcua = False
        self.event_frommain = False
        # print("The values of workstation positions are", self.machine_pos)

    def __await__(self):
        async def closure():
            # print("await")
            return self

        return closure().__await__()

    def bid(self, auctioned_task: Task, data_opcua):
        bid_value = 0.0
        task_cost = 0.0
        marginal_cost = 0.0
        machine_pos = [[3569, 5526], [11989, 5176], [5401, -1414], [14936, -1658], [25615, -2503], [3077, 12153],
                       [15434, 16900], [12432, 10650], [22123, 10581], [27500, 3630]]
        # print("The broadcasted task is", auctioned_task)

        start_loc = auctioned_task.command[0]
        end_loc = auctioned_task.command[1]
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
            end_pos = [24517, 11716]
        else:
            # end_pos = data_opcua["machine_pos"][end_loc - 1]
            end_pos = self.machine_pos[end_loc - 1]
            # print("Target position values", end_pos)
        # print("End_position", end_pos)
        # print("Start position values", start_pos)
        # print("Target position values", end_pos)
        task_cost = distance.euclidean(start_pos, end_pos)
        # print("Cleared bid mid-function")
        # if self.data_opcua["rob_busy"][self.id-1] == False :
        # print(f"Robot bid ID {self.id}")
        # print(data_opcua["robot_pos"])
        if self.free == True and data_opcua["rob_busy"][self.id - 1] == False:
            marginal_cost = distance.euclidean(start_pos, data_opcua["robot_pos"][self.id - 1])
        else:
            marginal_cost = 99999999999
        bid_value = task_cost + marginal_cost
        # print(bid_value)
        return bid_value

    def task_assign(self, task):
        self.assigned_task = True
        self.task = task
        self.free = False

    def product_assign(self, product):
        self.assigned_task = True
        self.product = product
        self.free = False

    async def trigger_task(self, task):
        self.task = task
        self.exec_cmd = True

        # print(f"Task triggered to robot {self.id} and execution status is {self.exec_cmd}")

    async def initiate_task(self, q_initiate_task: asyncio.Queue, W_robot, Ax_station, q_trigger_cmd: asyncio.Queue):
        while True:

            task_opcua = await q_initiate_task.get()
            # print(task_opcua)
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
            run = 1
            while run == 1:

                match self.task.step:
                    case 1:
                        # print("Case1 activated", pickup, self.event_toopcua, Ax_station[
                        #    pickup - 11].booked)
                        ########Pickup part from source position########
                        if 11 <= pickup <= 20 and self.event_toopcua == False and Ax_station[
                            pickup - 11].booked == False:
                            self.opcua_cmd = ["pick", str(pickup - 1)]
                            self.path_clear = True
                            Ax_station[pickup - 11].booked = True
                            # self.task.step = 2
                            # print(
                            #    f" Path clearance condition 2 activated for robot {self.id} for task{self.task.command}")

                    case 2:
                        # print(f"Drop station {drop} status, booking : {W_robot[drop - 1].booked}, Queue1 {W_robot[drop - 1].q1_empty}, Queue2 {W_robot[drop - 1].q2_empty}")
                        # print("Case 2", drop, self.event_toopcua)
                        ########To drop workstation########
                        if 1 <= drop <= 10 and self.event_toopcua == False:
                            if (W_robot[drop - 1].booked == False and W_robot[drop - 1].product_free == True and
                                    W_robot[drop - 1].robot_free == True and ((self.q2 == False and self.q1 == True) or (self.q2 == False and self.q1 == False))):
                                self.opcua_cmd = ["drop", str(drop - 1)]
                                self.path_clear = True
                                self.task.step = 5  ## Last step ####
                                W_robot[drop - 1].booked = True
                                print(
                                    f"Robot{self.id} moved to Drop workstation {drop} with positions Q1 {self.q1} and Q2 {self.q2}")
                            elif (W_robot[drop - 1].booked == True or W_robot[drop - 1].product_free == False or
                                  W_robot[drop - 1].robot_free == False) and (W_robot[drop - 1].q1_empty == True):
                                self.opcua_cmd = ["q1", str(drop - 1)]
                                self.path_clear = True
                                self.task.step = 3
                                W_robot[drop - 1].q1_empty = False


                                # print(f"Robot{self.id} moved to q1 workstation")
                            elif (W_robot[drop - 1].booked == True or W_robot[drop - 1].product_free == False or
                                  W_robot[drop - 1].robot_free == False) \
                                    and (W_robot[drop - 1].q1_empty == False) and (
                                    W_robot[drop - 1].q2_empty == True) and (
                                    self.wk_loc != drop):
                                self.opcua_cmd = ["q2", str(drop - 1)]
                                self.path_clear = True
                                self.task.step = 4
                                W_robot[drop - 1].q2_empty = False
                                # print(f"Robot{self.id} moved to q2 workstation")


                    case 6:
                        # print(f"Pickup station {pickup} status, booking : {W_robot[pickup - 1].booked}, "
                        # f"Queue1 {W_robot[pickup - 1].q1_empty}, Queue2 {W_robot[pickup - 1].q2_empty}")
                        #######To Pickup from Workstation #######
                        if 1 <= pickup <= 10 and self.event_toopcua == False:

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
                        if drop == 50 and self.event_toopcua == False and Ax_station[10].booked == False:
                            self.opcua_cmd = ["sink", str(pickup - 1)]
                            self.path_clear = True
                            self.task.step = 11
                            Ax_station[10].booked = True

                    case 12:
                        ##Move to Base Station#####
                        # Ax_station[10].product_clearance()
                        self.task.step = 13
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
                    self.free = False
                    data = [self.opcua_cmd, self.id, self.new_prod]
                    # print(data)
                    await q_trigger_cmd.put(data)
                    # print(f"Robot{self.id} Triggered OPCUA command", data)
                    self.event_toopcua = False  ## Clear flag for transfer to opcua command
                    q_initiate_task.task_done()
                else:
                    # print(
                    # f"Robot{self.id} at WK {self.wk_loc} awaiting for path to be cleared for task {self.task.command}")
                    self.wait = True
                    wTime = Waiting_time(stime=datetime.now(), etime=datetime.now(), dtime=0, pickup=pickup, drop=drop,
                                         tr_no=self.id)
                    await asyncio.sleep(10)
                    wTime.stop_timer()
                    pass

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
                if self.base == True:
                    W_robot[self.wk_loc - 1].booked = False
                    ##indicate robot vacating the current wk location
                    W_robot[self.wk_loc - 1].robot_free = True
                # elif self.q1 == True:
                #     W_robot[self.wk_loc - 1].q1_empty = True
                # elif self.q2 == True:
                #     W_robot[self.wk_loc - 1].q2_empty = True
            elif 11 <= self.wk_loc <= 20:
                Ax_station[self.wk_loc - 11].booked = False
                # print(f" Source station {Ax_station[self.wk_loc - 11]} unbooked")
            elif self.wk_loc == 50:
                Ax_station[10].booked = False

            ## Clear Workstation queue flags ####

            start_time = datetime.now()
            tTime = Transfer_time(stime=datetime.now(), etime=datetime.now(), dtime=0, pickup=self.task.command[0],
                                  drop=self.task.command[1], tr_no=self.id)
            # print(f"Robot {self.id} started executing at {start_time}")
            ##Run loop until Robot is done executing
            while self.executing == True:
                # await asyncio.sleep(0)
                if data_opcua["rob_busy"][self.id - 1] == False:
                    break
                else:
                    await asyncio.sleep(2)
            if self.task.step < 12:
                tTime.calc_time()
                self.product.tracking.append(tTime)
            # Events["rob_execution"][self.id - 1] = False
            self.executing = False
            exec_time = (datetime.now() - start_time).total_seconds()
            # print(f"Robot {self.id} took {exec_time:,.2f} seconds to run for the task step {self.task.step}")
            self.wk_loc = int(self.opcua_cmd[1]) + 1
            # if 1 <= self.wk_loc <= 10 :
            #     W_robot[self.wk_loc - 1].robot_free = False ## Indicating robot occupied target wk location
            print(f"Robot {self.id} internal opcua command is {self.opcua_cmd}")
            #print(f"Robot {self.id} is at Station {self.wk_loc} with status : base {self.base}, q1 {self.q1}, q2 {self.q2}")
            # print(f"Task Step value is {self.task.step}")
            # self.locate_robot()
            # print(self.task.step)
            match self.task.step:
                case 1:
                    self.base = True
                    self.q1 = False
                    self.q2 = False
                    # loop.call_soon_threadsafe(event_init_task.set())
                    if self.task.command[1] == 50:
                        self.task.step = 10
                    else:
                        self.task.step = 2
                    ## Robot occupying the workstation space when performing pickup task
                    if 1 <= self.task.command[0] <= 10:
                        W_robot[self.wk_loc - 1].robot_free = False
                    # print(f"Robot{self.id} picked up the product and will movie to drop wk")
                    await asyncio.sleep(5) ##giving time for visual animation of pickup action
                    self.exec_cmd = True
                    if 1 <= self.task.command[0] <= 10:
                        W_robot[self.wk_loc - 1].product_free = True
                    # print(f"Robot {self.id} will move to drop workstation")
                    #########opcua_cmd_event(id=self.id, loop=loop)
                    q_initiate_task.put_nowait(self.task)
                    #print(f"Task Continued in Robot {self.id}")

                case 3:
                    # event_chkpath.set()
                    # print(f"Robot{self.id} at Drop {self.wk_loc} queue1 position")
                    self.task.step = 2
                    if self.q2 == True:
                        W_robot[self.wk_loc - 1].q2_empty = True
                    self.base = False
                    self.q1 = True
                    self.q2 = False
                    # elif self.q2 == True:
                    #     W_robot[self.wk_loc - 1].q2_empty = True
                    self.exec_cmd = True
                    ########opcua_cmd_event(id=self.id, loop=loop)
                    q_initiate_task.put_nowait(self.task)

                case 4:
                    # event_chkpath.set()
                    # print(f"Robot{self.id} at Drop {self.wk_loc} queue2 position")
                    self.task.step = 2
                    self.base = False
                    self.q1 = False
                    self.q2 = True
                    self.exec_cmd = True
                    #######opcua_cmd_event(id=self.id, loop=loop)
                    q_initiate_task.put_nowait(self.task)

                case 5:
                    if self.q1 == True:
                        W_robot[self.wk_loc - 1].q1_empty = True
                    self.base = True
                    self.q1 = False
                    self.q2 = False
                    self.free = True
                    ## Workstation occupied when robot performing drop mission
                    W_robot[self.wk_loc - 1].robot_free = False
                    W_robot[self.wk_loc - 1].assingedProduct = self.product
                    # print(f"Robot{self.id} at Drop workstation")
                    self.assigned_task = False
                    # W_robot[self.wk_loc - 1].q1_empty = True
                    # W_robot[self.wk_loc - 1].q2_empty = True
                    ##NEW implementation for saturating products####
                    new_task_list = generate_task(order=production_order)
                    # print("Generated TASK from new function", new_task_list)
                    new_product = GreedyScheduler.robot_done(product=self.product, product_tList=new_task_list)
                    if new_product != None:
                        q_done_product.put_nowait(new_product)
                        # print("No new product to generate")
                    else:
                        pass
                    #########wk_process_event(wk=self.task.command[1], loop=loop)
                    for wks in W_robot:
                        if wks.id == self.task.command[1]:
                            await q_initiate_process[wks.id - 1].put("Start")
                            # print(f"Robot{self.id} delivered to Workstation {wks.id}")

                case 7:
                    # event_chkpath.set()
                    # print(f"Robot{self.id} at pickup {self.wk_loc} queue1 workstation")
                    self.task.step = 6
                    self.exec_cmd = True
                    # W_robot[self.wk_loc - 1].q2_empty = True
                    ########opcua_cmd_event(id=self.id, loop=loop)
                    q_initiate_task.put_nowait(self.task)

                case 8:
                    # event_chkpath.set()
                    # print(f"Robot{self.id} at pickup {self.wk_loc} queue2 workstation")
                    self.task.step = 6
                    self.exec_cmd = True
                    #######opcua_cmd_event(id=self.id, loop=loop)
                    q_initiate_task.put_nowait(self.task)

                case 11:
                    # print(f"Robot{self.id} at Sink Station")
                    # print(
                    #    f"Product {self.product.pv_Id} and Instance {self.product.pi_Id}  moved to sink node by Robot {self.id}")
                    self.base = True
                    self.q1 = False
                    self.q2 = False
                    st = Sink(tstamp=datetime.now())
                    self.product.tracking.append(st)
                    self.assigned_task = False
                    # self.free = True
                    self.finished_product = self.product
                    # print(f"Robot {self.id} unloaded completed product {self.product} to Sink")
                    # self.base_move = True
                    self.opcua_cmd = ["base", "99"]
                    data = [self.opcua_cmd, self.id, self.new_prod]
                    q_trigger_cmd.put_nowait(data)

                    sink_task_list = generate_task(order=production_order)
                    sink_product = GreedyScheduler.prod_completed(product=self.product, product_tList=sink_task_list)
                    if sink_product != None:
                        q_done_product.put_nowait(sink_product)
                        # print("No new product to generate")
                    else:
                        pass
                    Ax_station[10].booked = False
                    self.task.step = 12
                    # print(f"Robot {self.id} moving to Base Station")
                    self.exec_cmd = True
                    #########opcua_cmd_event(id=self.id, loop=loop)
                    q_initiate_task.put_nowait(self.task)

                case 13:
                    self.free = True
                    # await asyncio.sleep(5)
                    # print(f"Robot {self.id} ")
                    # self.base_move = False
                    self.wk_loc = 99
                    # self.exec_cmd = False
                    # print(f"Robot{self.id} at Base Station")
                    # if T_robot[0].wk_loc == 99 and T_robot[1].wk_loc == 99 and T_robot[2].wk_loc == 99:
                    #     await GreedyScheduler.production_end()
                    # all_based = False
                    # for robot in T_robot:
                    #     if robot.wk_loc == 99:
                    #         all_based = True
                    #     elif robot.wk_loc != 99:
                    #         all_based = False

                    if all(robot.wk_loc == 99 for robot in T_robot):
                        GreedyScheduler.production_end()
                        self.task.step = 14

            q_executing_task.task_done()


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
        self.processing = False

    def __await__(self):
        async def closure():
            # print("await")
            return self

        return closure().__await__()

    def product_clearance(self):
        self.product_free = True
        self.robot_free = True
        self.booked = False
        # print(f"The workstation {self.id} is Product Free")

    async def process_execution(self, q_initiate_process: asyncio.Queue, q_done_product: asyncio.Queue):
        while True:
            # await asyncio.sleep(2)
            # print(f"Workstation {self.id} execution task re-initialized")
            prod = await q_initiate_process.get()
            # print("Received data from robot on Workstation", prod)
            # print(f" Workstation ID {self.id}")
            process_time = production_order["Process_times"][self.assingedProduct.pv_Id - 1][self.id - 1]
            # process_time = 20
            # print(f"Product received by Workstation{self.id} is {self.assingedProduct}")
            self.process_done = False
            self.product_free = False
            # print(f"Process task executing at workstation {self.id}")
            pt = Process_time(stime=datetime.now(), etime=datetime.now(), dtime=0, wk_no=self.id)
            self.processing = True
            await asyncio.sleep(process_time)
            self.processing = False
            # print(f"Process task on workstation {self.id} finished")
            self.assingedProduct.mission_list.pop(0)
            # print(f"Current process task removed from product {self.product.pv_Id,self.product.pi_Id}")
            # print(f"Done workstation {self.id}")
            self.process_done = True
            # print(f"The Workstation {self.id} free status is {self.process_done}")
            # print("done product", self.done_product)
            pt.calc_time()
            self.assingedProduct.tracking.append(pt)
            self.assingedProduct.released = True
            ### Remove current from product###
            self.assingedProduct.released = True
            self.done_product = self.assingedProduct
            # a = [self.done_product]
            q_done_product.put_nowait(self.done_product)
            # print(f"Product {self.done_product} added into done queue")
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

    def source_station(self, product):
        return None

    def product_clearance(self):
        self.product_free = True
        self.robot_free = True
        self.booked = False
        # print(f"The Sink Station {self.id} is Free")
