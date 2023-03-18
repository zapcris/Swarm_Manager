import asyncio
import math
from datetime import datetime

from scipy.spatial import distance

from Greedy_implementation.SM04_Task_Planning_agent import Task_Planning_agent, order
from Greedy_implementation.SM05_Scheduler_agent import Scheduling_agent
from Greedy_implementation.SM10_Product_Task import Product, Task

################################# Taken from Robot_Agent###############################################################
#### Initialization data###############

q_main_to_releaser = asyncio.Queue()
q_robot_to_opcua = asyncio.Queue()
q_product_done = asyncio.Queue()

null_product = Product(pv_Id=0, pi_Id=0, task_list=[], inProduction=False, finished=False, last_instance=0, robot=99,
                       wk=0, released=False)
null_Task = Task(id=0, type=0, command=[], pV=0, pI=0, allocation=False, status="null", robot=99)
T_robot = []
W_robot = []

p1 = Product(pv_Id=1, pi_Id=1, task_list=[[11, 1], [2, 5]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False)
p2 = Product(pv_Id=1, pi_Id=1, task_list=[[11, 2], [2, 8]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False)
p3 = Product(pv_Id=1, pi_Id=1, task_list=[[11, 3], [3, 6]], inProduction=False, finished=False, last_instance=1,
             robot=0,
             wk=0, released=False)
test_task = Task(id=1, type=1, command=[11, 1], pV=1, pI=1, allocation=False, status="null", robot=1)

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


data_opcua = {
    "brand": "Ford",
    "mobile_manipulator": ["", "", ""],
    "rob_busy": [False, False, False],
    "machine_pos": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], ],
    "robot_pos": [[0, 0], [0, 0], [0, 0]],
    "create_part": 0,
    "mission": ["", "", "", "", "", "", "", "", "", ""],

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

### instantiate order and generation of task list to that order
test_order = Task_Planning_agent(input_order=order)
generate_task = test_order.task_list()
Product_task = generate_task[0]
Global_task = generate_task[1]
Task_Queue = generate_task[2]

# for a in Product_task:
#     print(a)

### Initialize Reactive Scheduler
GreedyScheduler = Scheduling_agent(
    order=order,
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

    def __init__(self, id, global_task, product, tqueue):
        self.id = id
        self.free = True
        # self.start_robot(tqueue)
        self.global_task = global_task
        # self.auctioned_task = auctioned_task
        self.success_bid = None
        self.STN = None
        self.assigned_task = False
        self.assigned_product = False
        self.executing = data_opcua["rob_busy"][self.id - 1]
        self.event = asyncio.Event()
        self.task = Task(id=0, type=0, command=[], pI=0, pV=0, allocation=False, status="null", robot=1)
        self.product = product
        self.finished_product = Product
        self.exec_cmd = False
        self.path_clear = False
        self.wk_loc = 99  ### 99 - arbitrary position #####
        self.base_move = False

    def __await__(self):
        async def closure():
            # print("await")
            return self

        return closure().__await__()

    def bid(self, auctioned_task):
        bid_value = 0.0
        task_cost = 0.0
        marginal_cost = 0.0
        print(auctioned_task)
        start_loc = auctioned_task.command[0]
        end_loc = auctioned_task.command[1]
        total_ws = len(data_opcua["machine_pos"])
        if start_loc == 11:  ## if source node
            start_pos = [0, -1000]
        else:
            start_pos = data_opcua["machine_pos"][start_loc]
        if end_loc == 12:  ## if source node or sink node
            end_pos = [500, 500]
        else:
            end_pos = data_opcua["machine_pos"][end_loc]
        ### Euclidean distance for cost calculation ##########
        # task_cost = math.sqrt(math.pow(end_pos[0] - start_pos[0], 2) + math.pow(
        #     end_pos[1] - start_pos[1], 2) * 1.0)
        task_cost = distance.euclidean(start_pos, end_pos)

        # if self.data_opcua["rob_busy"][self.id-1] == False :
        if self.free == True and data_opcua["rob_busy"][self.id - 1] == False:
            # marginal_cost = math.sqrt(
            #     math.pow(start_pos[0] - data_opcua["robot_pos"][self.id - 1][0], 2) + math.pow(
            #         start_pos[1] - data_opcua["robot_pos"][self.id - 1][1], 2) * 1.0)
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

    # def task_deassign(self):
    #     self.assigned_task = False
    #     self.task = null_Task
    #     self.free = True

    # def product_deassign(self):
    #     self.assigned_task = False
    #     self.product = null_product
    #     self.free = True

    # def clr_fin_prod(self):
    #     self.finished_product = null_product
    ### removed function#####
    # def path_free_status(self):
    #     # if self.task.command[0] >= 11 and self.task.command[1] <= 10:
    #     #     self.path_clear = W_robot[self.task.command[1] - 1].product_free
    #     # elif self.task.command[0] <= 10 and self.task.command[1] >= 11:
    #     #     self.path_clear = W_robot[self.task.command[0] - 1].product_free
    #     # else:
    #     #     self.path_clear = W_robot[self.task.command[0] - 1].product_free and W_robot[
    #     #         self.task.command[1] - 1].product_free
    #     pickup = self.task.command[0]
    #     drop = self.task.command[1]
    #
    #     if pickup != 11 and drop != 12:
    #         rob_pos = data_opcua["robot_pos"][self.id - 1]
    #         pickup_pos = data_opcua["machine_pos"][pickup]
    #         drop_pos = data_opcua["machine_pos"][drop]
    #         dist = distance.euclidean(rob_pos, pickup_pos)
    #         if dist <= 1000:
    #             ## check only for drop wk free status ###
    #             self.path_clear = W_robot[drop - 1].product_free
    #             print(f"Path clear robot {self.id} condition 1")
    #         elif dist > 1000:
    #             self.path_clear = W_robot[drop - 1].product_free and W_robot[pickup - 1].product_free
    #             print(f"Path clear robot {self.id} condition 2")
    #
    #     elif pickup == 11 and drop != 12:
    #         ## check only for drop wk free status ###
    #         self.path_clear = W_robot[drop - 1].product_free
    #         # print(f"Path clear robot {self.id} condition 3")
    #     elif pickup != 11 and drop == 12:
    #         ## check only for pickup wk free status ###
    #         self.path_clear = W_robot[pickup - 1].product_free
    #         # print(f"Path clear robot {self.id} condition 4")

    def trigger_task(self, task, execute):
        self.task = task
        self.exec_cmd = execute
        # event.set()
        print(f"Task triggered to robot {self.id} and execution status is {self.exec_cmd}")

    async def check_path_clear(self, event_frommain: asyncio.Event, event_toopcua: asyncio.Event):
        while True:

            await event_frommain.wait()
            # print(f"OPCUA command initiated at robot {self.id}")
            pickup = self.task.command[0]
            drop = self.task.command[1]
            # self.path_clear = False

            # if pickup < 11 and drop < 11:
            #     if self.wk_loc == pickup and W_robot[drop - 1].booked == False:
            #         self.path_clear = True
            #         print(f" Path clearance condition 1.1 activated for robot {self.id}")
            #     elif self.wk_loc != pickup and W_robot[pickup - 1].robot_free == True and W_robot[
            #         drop - 1].booked == False:
            #         self.path_clear = True
            #         print(f" Path clearance condition 1.2 activated for robot {self.id}")
            # elif pickup == 11 and drop < 11:
            #     if W_robot[drop - 1].booked == False:
            #         self.path_clear = True
            #         print(f" Path clearance condition 2 activated for robot {self.id}")
            # elif pickup < 11 and drop == 12:
            #     if self.wk_loc == pickup:
            #         self.path_clear = True
            #         print(f" Path clearance condition 3.1 activated for robot {self.id}")
            #     elif self.wk_loc != pickup and W_robot[pickup - 1].robot_free == True:
            #         self.path_clear = True
            #         print(f" Path clearance condition 3.2 activated for robot {self.id}")
            #
            # else:
            #     pass

            if pickup < 11 and event_toopcua.is_set() == False:
                if self.wk_loc == pickup and W_robot[drop - 1].booked == False:
                    self.path_clear = True
                    print(f" Path clearance condition 1.1 activated for robot {self.id} for task{self.task.command}")
                elif self.wk_loc != pickup and W_robot[pickup - 1].robot_free == True and W_robot[
                    drop - 1].booked == False:
                    self.path_clear = True
                    print(f" Path clearance condition 1.2 activated for robot {self.id} for task{self.task.command}")
            elif pickup == 11 and event_toopcua.is_set() == False:
                if W_robot[drop - 1].booked == False:
                    self.path_clear = True
                    print(f" Path clearance condition 2 activated for robot {self.id} for task{self.task.command}")

            else:
                pass

            if event_frommain.is_set() == True and self.path_clear == True:
                event_toopcua.set()
                #await asyncio.sleep(1)
                self.exec_cmd = False
                self.path_clear = False
                # await asyncio.sleep(0.2)
                event_frommain.clear()

            else:

                print(f"Robot{self.id} awaiting for path to be cleared for task {self.task.command}")
                await asyncio.sleep(4)
                pass

    async def sendtoOPCUA(self, event_fromchkpath: asyncio.Event):
        while True:
            # print(f"sendtoOPCUA on robot {self.id} waiting for task execution clearance and exec status is {self.exec_cmd}")
            # if self.exec_cmd == True:
            # print(f"Robot execute command initiated")
            #await asyncio.sleep(2)
            # await event_tochkpath.wait()
            # self.path_free_status()
            await event_fromchkpath.wait()
            #await event_tochkpath.wait()
            pickup = self.task.command[0]
            drop = self.task.command[1]
            # while event_tochkpath_is
            # if pickup < 11:
            #     if self.wk_loc == pickup and W_robot[drop - 1].booked == False:
            #         self.path_clear = True
            #         print(f" Path clearance condition 1.1 activated for robot {self.id} for task{self.task.command}")
            #     elif self.wk_loc != pickup and W_robot[pickup - 1].robot_free == True and W_robot[
            #         drop - 1].booked == False:
            #         self.path_clear = True
            #         print(f" Path clearance condition 1.2 activated for robot {self.id} for task{self.task.command}")
            # elif pickup == 11:
            #     if W_robot[drop - 1].booked == False:
            #         self.path_clear = True
            #         print(f" Path clearance condition 2 activated for robot {self.id} for task{self.task.command}")
            #
            # else:
            #     pass
            #
            # if event_frommain.is_set() == True and self.path_clear == True:
            #     event_toopcua.set()
            #     await asyncio.sleep(1)
            #     self.exec_cmd = False
            #     # await asyncio.sleep(0.2)
            #     event_frommain.clear()
            #
            # else:
            #
            #     print(f"Robot{self.id} awaiting for path to be cleared")
            #     await asyncio.sleep(2)
            #     pass



            task = self.task
            self.Free = False
            data = [task, self.id]
            tar_wk = self.task.command[1] - 1
            q_robot_to_opcua.put_nowait(data)
            # opc_cmd_list.append(data)
            print(f"Task entered in opcua queue for robot {self.id}")

            ###This part is moved to new task releaser thread####
            # cmd = ["" for _ in range(2)]
            # print(f"Task {task} received from Swarm Manager for robot {self.id} for execution")
            # await asyncio.sleep(1)
            # if task["command"][1] == 12:
            #     c = str(task["command"][0]) + "," + str("s")
            #
            # else:
            #     c = str(task["command"][0]) + "," + str(task["command"][1])
            # cmd.insert((int(self.id) - 1), c)
            #
            #
            #
            #
            # if task["command"][0] == 11:
            #     # sleep(3)
            #     data_opcua["create_part"] = task["pV"]
            #     # write_opcua(task["pV"], "create_part", None)
            #     await asyncio.sleep(0.7)
            #     print(f"part created for robot {self.id},", task["pV"])
            #     data_opcua["create_part"] = 0
            #     await asyncio.sleep(0.7)
            #     data_opcua["mobile_manipulator"] = cmd
            #     await asyncio.sleep(0.7)
            #     data_opcua["mobile_manipulator"] = ["", "", ""]
            #     print("command sent to opcuaclient", cmd)
            #
            # else:
            #
            #     data_opcua["mobile_manipulator"] = cmd
            #     sleep(0.7)
            #     data_opcua["mobile_manipulator"] = ["", "", ""]
            #     #data_opcua["robot_exec"][self.id - 1] = False
            #     #data_opcua["rob_busy"][self.id - 1] = True
            #     W_robot[task.command[0]-1].product_clearance()

            # # print(f"robot {self.id} busy status is ", data_opcua["rob_busy"][self.id-1])
            # Events["rob_execution"][self.id - 1] = True
            # self.exec_cmd = False
            #self.path_clear = False
            event_fromchkpath.clear()

            #event_tochkpath.clear()


    async def execution_time(self, event, loop: asyncio.AbstractEventLoop):
        while True:
            # print(f'waiting for robot {id} for  execution')
            await event.wait()
            print(f'Robot {self.id} execution tim'
                f'er has started')
            start_time = datetime.now()
            print(f"Robot {self.id} started executing at {start_time}")
            while event.is_set() == True:
                await asyncio.sleep(1)
                if data_opcua["rob_busy"][self.id - 1] == False:
                    break
                else:
                    continue
            #await event2.wait()
            Events["rob_execution"][self.id - 1] = False
            exec_time = (datetime.now() - start_time).total_seconds()
            print(f"Robot {self.id} took {exec_time:,.2f} seconds to run")
            t = self.task.command
            #print(f"the product is delivered to workstation {t[1]} by robot {self.id}")
            self.wk_loc = t[1]
            print(f"Robot {self.id} is at {self.wk_loc}")
            W_robot[t[1] - 1].product_free = False
            W_robot[t[1] - 1].robot_free = False
            if t[1] <= 11:  ### checking for sink node commmand#####
                print(f"the product is delivered to workstation {t[1]} by robot {self.id}")
                print(f"Robot {self.id} is at {self.wk_loc}")
                #print("Triggered workstation is ", t[1])
                wk = t[1] - 1
                # print(f"product on robot {self.id}", self.product)
                W_robot[wk].assingedProduct = self.product
                print(f"Robot {self.id} assigned product to Workstation{t[1]} is {self.product}")
                ### self Product deassign ####
                self.assigned_task = False
                # self.product = null_product
                # self.task_deassign()
                ### self task deassign####
                self.assigned_task = False
                # self.task = null_Task
                self.free = True
                print(f"The robot {self.id} is Product and Task free")
                wk_process_event(wk=t[1], loop=loop)
                #await W_robot[wk].process_execution()
                #event2.clear()
                event.clear()

            else:
                print(f"Product moved to sink node")
                # self.product.remove_task()
                # self.task_deassign()
                ### self task deassign####
                if self.base_move == False:
                    self.assigned_task = False
                    #self.task = null_Task
                    self.free = True
                    self.finished_product = self.product
                    W_robot[11].sink_station(self.product)
                    print(f"Robot {self.id} unloaded completed product {self.product} to Sink")
                    self.base_move = True
                    cmd = []
                    if self.id == 1:
                        cmd = ['m,0,-2772,-3081', '', '']
                    elif self.id == 2:
                        cmd = ['', 'm,0,-2772,2293', '']
                    else:
                        cmd = ['', '', 'm,0,-2772,6752']
                    ### move to base station #####
                    data_opcua["mobile_manipulator"] = cmd
                    await asyncio.sleep(2)
                    data_opcua["mobile_manipulator"] = ["", "", ""]
                    print(f"Robot moving to Base Station")
                elif self.base_move == True:
                    print(f"Robot reached Base Station")
                    self.base_move = False
                    self.wk_loc = 99 ### 0 --> Base/arbitrary location for
                    W_robot[11].product_clearance()
                    #event2.clear()
                    event.clear()




    ###3 Redundant async task to check if robot busy status is False while executing#####
    # async def check_rob_done(self, event: asyncio.Event, event_opcua: asyncio.Event):
    #     while True:
    #         await asyncio.sleep(2)
    #         await event.wait()
    #         await asyncio.sleep(2)
    #         if event.is_set() == True and data_opcua["rob_busy"][self.id - 1] == False:
    #             event_opcua.set()
    #             # print(f"Event 2 (opcua) for Robot {self.id} activated")
    #         else:
    #             # print("No opcua event generated")
    #             pass


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

    def __await__(self):
        async def closure():
            # print("await")
            return self

        return closure().__await__()

    # def product_assign(self, product: Product):
    #     self.assingedProduct = product

    # def clr_done_prod(self):
    #     self.done_product = null_product
    def source_station(self):
        return None
    def sink_station(self, product):

        return None

    def product_clearance(self):
        self.product_free = True
        self.robot_free = True
        self.booked = False
        print(f"The workstation {self.id} is Product Free")

    # async def process_executed(self):
    #     print(f"Product {self.assingedProduct} released from workstation {self.id}")
    #     self.assingedProduct.set_Release()
    #     self.done_product = self.assingedProduct

    async def process_execution(self, event):
        while True:
            await asyncio.sleep(2)
            print(f"Workstation {self.id} execution task re-initialized")
            await event.wait()
            print(f" Workstation ID {self.id}")
            process_time = order["Process_times"][self.assingedProduct.pv_Id - 1][self.id - 1]
            # process_time = 20
            print(f"Product received by Workstation{self.id} is {self.assingedProduct}")
            self.process_done = False
            self.product_free = False
            print(f"Process task executing at workstation {self.id}")
            await asyncio.sleep(process_time)
            print(f"Process task on workstation {self.id} finished")
            # GreedyScheduler.process_task_executed(self.assingedProduct)
            # await asyncio.sleep(0.5)
            # self.assingedProduct.remove_task()
            ### Remove current from product###
            self.assingedProduct.task_list.pop(0)
            # print(f"Current process task removed from product {self.product.pv_Id,self.product.pi_Id}")
            print(f"Done workstation {self.id}")
            self.process_done = True
            print(f"The Workstation {self.id} free status is {self.process_done}")
            print("done product", self.done_product)
            # await asyncio.sleep(0.5)
            # await self.process_executed()
            self.assingedProduct.released = True
            ### Remove current from product###
            self.assingedProduct.released = True
            self.done_product = self.assingedProduct
            a = [self.done_product]
            q_product_done.put_nowait(a)
            print(f"Product {self.done_product} added into done queue")
            event.clear()
