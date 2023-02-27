
from time import sleep
from queue import Queue
from threading import Thread
from Task_Planner import Task, Task_PG
from Robot_agent import Transfer_robot




class Product:
    # num = int
    # PV = int
    # inProduction = False
    # current_position = []
    # start_time = time
    # finish_time = time
    # finished = False

    def __init__(self, pi_id, pv_id, task_list, inProduction, finished):
        self.pi = pi_id
        self.pv = pv_id
        self.inProduction = inProduction
        self.finished = finished
        self.task_list = task_list


    # def __str__(self):
    #     return f'The product instance is {self.pi}'
    #
    # def __repr__(self):
    #     return self

    def __getitem__(self, pi):
        return getattr(self, pi)

    # def get_task(self):
    #
    #     try:
    #        self.tqueue = self.task_queue.get(False)
    #        # Opt 1: Handle task here and call q.task_done()
    #     except queue.Empty:
    #        # Handle empty queue here
    #         pass
    #
    #     return getattr(self)

class Joint_Scheduler:

    def __init__(self, order, global_task, product_task, data_opcua, T_robot):

        self.global_task = global_task
        self.data_opcua = data_opcua
        self.order = order
        self.robots = T_robot
        self.initiated_products = []
        self.product_task = product_task


    def initialize_production(self):

        #### Initialization of Products based on total available robots ######
        if self.order["PV"] >= len(self.robots):
            for i, r in enumerate(self.robots):
         ########### encapsulated task sequence object for every product instance #######
                p = Product(i + 1, 1, self.product_task[i], True, False)

                print(f"First instance of products Variant {i+1} generated for production")
                self.initiated_products.append(p)
        else: ###### if total robots greater than product variants############
            for i in range(self.order["PV"]):
                p = Product(i + 1, 1, self.product_task[i], True, False)
                print(f"First instance of products Variant {i+1} generated for production")
                self.initiated_products.append(p)

        task_for_allocation = self.trigger_allocation()

        return task_for_allocation
######## Dispatch Task to Task Allocator for broadcasting ###################
    def trigger_allocation(self):
        task_for_allocation = []

######### Initial Release ########################
        for i, product in enumerate(self.initiated_products):
            cmd = product["task_list"][0]
            TA = Task(i+1, 1, cmd, i+1, 1, False, "Pending", 999)
            task_for_allocation.append(TA)

        return task_for_allocation





    def release_execCommand(self):
        task_for_execution = []

        return task_for_execution

    def proactive_scheduler(self):
        global_STN = Queue()
        ############# Future implementation ##############
        return global_STN
