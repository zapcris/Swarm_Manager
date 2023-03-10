import asyncio
import math
from datetime import datetime
from time import sleep
from Greedy_implementation.SM04_Task_Planning_agent import Task_Planning_agent, order
from Greedy_implementation.SM05_Scheduler_agent import Scheduling_agent
from Greedy_implementation.SM10_Product_Task import Product, Task

################################# Taken from Robot_Agent###############################################################
#### Initialization data###############
q_robot_to_opcua = asyncio.Queue()
null_product = Product(pv_Id=0, pi_Id=0, task_list=[], inProduction=False, finished=False, last_instance=0, robot=0,
                       wk=0, released=False)
null_Task = Task(id=0, type=0, command=[], pV=0, pI=0, allocation=False, status="null", robot=0)
T_robot = []
W_robot = []

#################################### Robot agent code ################################################
event1 = asyncio.Event()
event2 = asyncio.Event()
event3 = asyncio.Event()
event1_opcua = asyncio.Event()
event2_opcua = asyncio.Event()
event3_opcua = asyncio.Event()
event1_1 = asyncio.Event()
event2_1 = asyncio.Event()
event3_1 = asyncio.Event()
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

def wk_event(wk):
    if wk == 1:
        return wk_1
    elif wk == 2:
        return wk_2
    elif wk == 3:
        return wk_3
    elif wk == 4:
        return wk_4
    elif wk == 5:
        return wk_5
    elif wk == 6:
        return wk_6
    elif wk == 7:
        return wk_7
    elif wk == 8:
        return wk_8
    elif wk == 9:
        return wk_9
    elif wk == 10:
        return wk_10


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
        self.data_opcua = data_opcua
        self.success_bid = None
        self.STN = None
        self.assigned_task = False
        self.assigned_product = False
        self.executing = data_opcua["rob_busy"][self.id - 1]
        self.event = asyncio.Event()
        self.task = Task(id=0, type=0, command=[], pI=0, pV=0, allocation=False, status="null", robot=1)
        self.product = product
        self.finished_product = null_product
        self.exec_cmd = False

    def __await__(self):
        async def closure():
            # print("await")
            return self

        return closure().__await__()

    def bid(self, auctioned_task):
        bid_value = 0.0
        task_cost = 0.0
        marginal_cost = 0.0
        start_loc = auctioned_task.command[0]
        end_loc = auctioned_task.command[1]
        total_ws = len(self.data_opcua["machine_pos"])
        if start_loc == 11:  ## if source node
            start_pos = [0, -1000]
        else:
            start_pos = self.data_opcua["machine_pos"][start_loc - 1]
        if end_loc == 12:  ## if source node or sink node
            end_pos = [500, 500]
        else:
            end_pos = self.data_opcua["machine_pos"][end_loc - 1]
        ### Euclidean distance for cost calculation ##########
        task_cost = math.sqrt(math.pow(end_pos[0] - start_pos[0], 2) + math.pow(
            end_pos[1] - start_pos[1], 2) * 1.0)

        # if self.data_opcua["rob_busy"][self.id-1] == False :
        if self.free == True and data_opcua["rob_busy"][self.id - 1] == False:
            marginal_cost = math.sqrt(
                math.pow(start_pos[0] - self.data_opcua["robot_pos"][self.id - 1][0], 2) + math.pow(
                    start_pos[1] - self.data_opcua["robot_pos"][self.id - 1][1], 2) * 1.0)
        else:
            marginal_cost = 99999999999
        bid_value = task_cost + marginal_cost
        # print(bid_value)
        return bid_value

    def task_assigned(self, task):
        self.assigned_task = True
        self.task = task
        self.free = False
        return self

    def prod_assigned(self, product):
        self.assigned_task = True
        self.product = product
        self.free = False
        return self

    def task_deassigned(self):
        self.assigned_task = False
        self.task = null_Task
        self.free = True
        return self

    def prod_deassigned(self):
        self.assigned_task = False
        self.product = null_product
        self.free = True
        return self

    def clr_fin_prod(self):
        self.finished_product = null_product
        return self
    def assign_product(self, product):
        self.product = product

    def trigger_task(self, task, execute):
        self.task = task
        self.exec_cmd = execute
        #event.set()
        print(f"Task triggered to robot {self.id} and execution status is {self.exec_cmd}")



    async def sendtoOPCUA(self, event:asyncio.Event):
        while True:
            #print(f"sendtoOPCUA on robot {self.id} waiting for task execution clearance and exec status is {self.exec_cmd}")
            #if self.exec_cmd == True:
            await event.wait()
            #print(f"Robot execute command initiated")

            if self.exec_cmd == True and W_robot[self.task.command[1] - 1].product_free == True:
                task = self.task
                self.Free = False
                data = [task, self.id]
                tar_wk = self.task.command[1]-1
                W_robot[tar_wk].product_free = False
                print(f"Workstation {self.task.command[1]} is booked")
                q_robot_to_opcua.put_nowait(data)
                #opc_cmd_list.append(data)
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
                Events["rob_execution"][self.id - 1] = True
                self.exec_cmd = False
                event.clear()


            else:
                #print(f"Robot {self.id} waiting for worksation to be cleared")
                pass
        # else:
        #
        #    pass



    async def execution_time(self, event, event2):

        while True:
            # print(f'waiting for robot {id} for  execution')
            await event.wait()
            print(f'Robot {self.id} execution tim'
                  f'er has started')
            # if self.id ==1 :
            #     time = 15
            # elif self.id ==2 :
            #     time = 5
            # else:
            #     time = 5
            # await asyncio.sleep(time)
            start_time = datetime.now()
            print(f"Robot {self.id} started executing at {start_time}")
            Events["rob_execution"][self.id - 1] = True
            # while Events["rob_execution"][id - 1] == True:
            #     if data_opcua["rob_busy"][id - 1] == True:
            #         # exec_time = (datetime.now() - start_time).total_seconds()
            #         # print(f"Robot {id} is running")
            #         pass
            #     elif data_opcua["rob_busy"][id - 1] == False:
            #         Events["rob_execution"][id - 1] = False
            # flag = asyncio.Event()
            await event2.wait()
            # Events["rob_execution"][id - 1] = False
            exec_time = (datetime.now() - start_time).total_seconds()
            print(f"Robot {self.id} took {exec_time:,.2f} seconds to run")
            t = self.task.command
            print(f"the product is delivered to workstation {t[1]} by robot {self.id}")
            if t[1] <= 11:  ### checking for sink node commmand#####


                a = wk_event(t[1])
                a.set()
                print("Triggered workstation is ", t[1])
                wk = t[1]-1

                W_robot[wk].assignedProduct = self.product

                await asyncio.sleep(0.5)
                self.product.remove_task()
                await self.prod_deassigned()
                print(f"The robot {self.id} free status is {self.free}")
                await self.task_deassigned()

            else:
                print(f"Product moved to sink node")
                self.product.remove_task()
                await self.task_deassigned()
                self.finished_product = self.product
            event2.clear()
            event.clear()


    async def check_rob_done(self, event: asyncio.Event, event_opcua: asyncio.Event):
        while True:
            await asyncio.sleep(2)
            await event.wait()
            if event.is_set() == True and data_opcua["rob_busy"][self.id - 1] == False:
                event_opcua.set()
                #print(f"Event 2 (opcua) for Robot {self.id} activated")
            else:
                # print("No opcua event generated")
                pass


class Workstation_robot:

    def __init__(self, wk_no, order, product: Product):
        self.id = wk_no
        self.process_done = True
        self.order = order
        #self.assigned_prod = False
        self.assingedProduct = product
        self.done_product = null_product
        self.product_free = True
    def __await__(self):
        async def closure():
            # print("await")
            return self

        return closure().__await__()

    # def prod_assigned(self, product: Product):
    #     #self.assigned_prod = True
    #     self.product = product


    def clr_done_prod(self):
        self.done_product = null_product


    def product_clearance(self):
        self.product_free = True
        print(f"The workstation {self.id} is Product Free")
    def prod_deassigned(self):
        print(f"Product {self.assingedProduct} released from workstation {self.id}")
        self.assingedProduct.set_Release()
        self.done_product = self.assingedProduct
        #self.assigned_prod = False
        #GreedyScheduler.normalized_production(self.product)



    async def process_execution(self, event: asyncio.Event):
        process_time = order["Process_times"][self.assingedProduct.pv_Id][self.id - 1]
        await event.wait()
        self.process_done = False
        self.product_free = False
        print(f"Process task executing at workstation {self.id}")
        await asyncio.sleep(process_time)
        print(f"Process task on workstation {self.id} finished")
        self.assingedProduct.remove_task()
        # print(f"Current process task removed from product {self.product.pv_Id,self.product.pi_Id}")
        GreedyScheduler.process_task_executed(self.assingedProduct)
        print(f"Done workstation {self.id}")
        self.prod_deassigned()
        self.process_done = True
        print(f"The Workstation {self.id} free status is {self.process_done}")
        event.clear()
