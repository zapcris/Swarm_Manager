from dataclasses import dataclass
import threading
import queue
from datetime import time


@dataclass
class Product:
    # num = int
    # PV = int
    # inProduction = False
    # current_position = []
    # start_time = time
    # finish_time = time
    # finished = False

    def __init__(self, pi_id, pv_id, product_flow, inProduction, finished):
        self.pv = pi_id
        self.pv = pv_id
        self.inProduction = inProduction
        self.finished = finished
        self.product_flow = product_flow

class Joint_Scheduler:

    def __init__(self, order, global_task, product_flow, data_opcua, T_robot):

        self.global_task = global_task
        self.data_opcua = data_opcua
        self.order = order
        self.robots = T_robot
        self.initiated_products = []
        self.product_flow = product_flow

    def product_generator(self):

        #### Initialization of Products ######
        if self.order["PV"] >= len(self.robots):
            for i, r in enumerate(self.robots):
                p = Product(i+1, 1,self.product_flow, True, False)
                print(f"First instance of products Variant {i+1} generated for production")
                self.initiated_products.append(p)
        else: ###### if total robots greater than product variants############
            for i in range(self.order["PV"]):
                p = Product(i+1, 1, self.product_flow, True, False)
                print(f"First instance of products Variant {i+1} generated for production")
                self.initiated_products.append(p)

        self.task_sequencer()

        return None

    def task_sequencer(self):
        task_for_allocation = None

        for i, product in enumerate(self.initiated_products):
            product


        return task_for_allocation

    def generate_queue(self):
        queue_list = []

        return queue_list

    def release_task(self):
        task_for_execution = []

        return task_for_execution

    def proactive_scheduler(self):
        global_STN = queue.Queue()
        ############# Future implementation ##############
        return global_STN
