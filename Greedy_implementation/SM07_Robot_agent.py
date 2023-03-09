import asyncio
import math
from datetime import datetime
from queue import Queue, Empty
from threading import Thread
from time import sleep

from Greedy_implementation.SM04_Task_Planner import order, Task

#################################### Robot agent code ################################################
# manager = Manager()
# data_opcua = manager.dict()
event1 = asyncio.Event()
event2 = asyncio.Event()
event3 = asyncio.Event()
event1_opcua = asyncio.Event()
event2_opcua = asyncio.Event()
event3_opcua = asyncio.Event()
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
    "robot_exec": [False, False, False]
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


class Transfer_robot:

    def __init__(self, id, global_task, data_opcua, tqueue):
        self.id = id
        self.free = bool
        # self.start_robot(tqueue)
        self.global_task = global_task
        # self.auctioned_task = auctioned_task
        self.data_opcua = data_opcua
        self.success_bid = None
        self.STN = None
        self.assigned_task = False
        self.executing = data_opcua["rob_busy"][self.id - 1]
        self.event = asyncio.Event()
        self.task = Task(id=1, type=1, command=[11,2], pI=1, pV=1, allocation= True,status="first",robot=1)

    def __await__(self):
        async def closure():
            print("await")
            return self

        return closure().__await__()

    def bid(self, auctioned_task):
        bid_value = 0.0
        task_cost = 0.0
        marginal_cost = 0.0
        start_loc = auctioned_task["command"][0]
        end_loc = auctioned_task["command"][1]
        total_ws = len(self.data_opcua["machine_pos"])
        if start_loc == 11:  ## if source node
            start_pos = [100, 100]
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
        if self.assigned_task == False and data_opcua["rob_busy"][self.id - 1] == False:
            marginal_cost = math.sqrt(
                math.pow(start_pos[0] - self.data_opcua["robot_pos"][self.id - 1][0], 2) + math.pow(
                    start_pos[1] - self.data_opcua["robot_pos"][self.id - 1][1], 2) * 1.0)
        else:
            marginal_cost = 999999999
        bid_value = task_cost + marginal_cost
        # print(bid_value)
        return bid_value

    def task_assigned(self):
        self.assigned_task = True
        return self

    def task_deassigned(self):
        self.assigned_task = False
        return self

    def node_function(self, tqueue):
        while True:
            try:
                taken_task = tqueue.get(False)
                self.sendtoOPCUA(taken_task)
                # Opt 1: Handle task here and call q.task_done()
            except Empty:
                # Handle empty queue here
                # print("Queue was empty")
                pass

    def start_robot(self, tqueue):
        t = Thread(target=self.node_function, args=(tqueue,))
        t.start()

    def simulate(self, q_in: Queue):
        return None

    async def sendtoOPCUA(self, task):
        self.Free = False
        self.task = task
        cmd = ["" for _ in range(2)]
        print(f"Task {task} received from Swarm Manager for execution")
        await asyncio.sleep(1)

        if task["command"][1] == 12:
            c = str(task["command"][0]) + "," + str("s")

        else:
            c = str(task["command"][0]) + "," + str(task["command"][1])
        cmd.insert((int(self.id) - 1), c)
        if task["command"][0] == 11:
            # sleep(3)
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
            sleep(0.7)
            data_opcua["mobile_manipulator"] = ["", "", ""]
            data_opcua["robot_exec"][self.id - 1] = False
            data_opcua["rob_busy"][self.id - 1] = True

        # print(f"robot {self.id} busy status is ", data_opcua["rob_busy"][self.id-1])
        Events["rob_execution"][self.id - 1] = True

        return None

    async def execution_time(self, event, id):

        while True:

            # print(f'waiting for robot {id} for  execution')
            await event.wait()
            print(f'Robot {id} execution timer has started')
            # await asyncio.sleep(3)
            start_time = datetime.now()
            Events["rob_execution"][id - 1] = True
            while Events["rob_execution"][id - 1] == True:
                if data_opcua["rob_busy"][id - 1] == True:
                    # exec_time = (datetime.now() - start_time).total_seconds()
                    # print(f"Robot {id} is running")
                    pass
                elif data_opcua["rob_busy"][id - 1] == False:
                    Events["rob_execution"][id - 1] = False
            exec_time = (datetime.now() - start_time).total_seconds()
            print(f"Robot {id} took {exec_time:,.2f} seconds to run")
            t = self.task.command
            print(f"the product is delivered to workstation {t[1]}")
            a = wk_event(t[1])
            # a.set()
            print("Triggered workstation is  is", t[1])
            event.clear()

    def execute_typ1cmd(self, fromscheduler):
        self.data_opcua["mobile_manipulator"] = fromscheduler

    def execute_typ2cmd(self, fromscheduler):
        self.data_opcua["mobile_manipulator"] = fromscheduler

    def execute_typ4cmd(self, fromscheduler):
        self.data_opcua["mobile_manipulator"] = fromscheduler


class Workstation_robot:

    def __init__(self, wk_no, order, data_opcua):
        self.id = wk_no
        self.free = True

        # self.processtime = process_times
        # self.auctioned_task = auctioned_task
        self.data_opcua = data_opcua

    async def process_execution(self, event, wk, product):
        process_time = order["Process_times"][product.pv_Id][wk - 1]
        await event.wait()
        self.free = False
        print(f"Process task executing at {wk}")
        await asyncio.sleep(process_time)
        print("Process task on workstation ", wk)
        event.clear()

        return None
