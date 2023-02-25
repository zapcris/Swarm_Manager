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

    def __init__(self, pi_id, pv_id, inProduction, finished):
        self.pv = pi_id
        self.pv = pv_id
        self.inProduction = inProduction
        self.finished = finished

class Joint_Scheduler:

    def __init__(self, order, global_task, data_opcua, T_robot):
        self.global_task = global_task
        self.data_opcua = data_opcua
        self.order = order
        self.robots = T_robot

    def product_generator(self):
        tasks_for_allocation = []
        total_instances = []

        #### Initialization of Products ######
        if self.order["PV"] >= len(self.robots):
            for i, r in enumerate(self.robots):
                p = Product(i+1, 1, True, False)
                print(f"First instance of products Variant {i+1} generated for production")
                total_instances.append(p)
        else: ###### if total robots greater than product variants############
            for i in range(self.order["PV"]):
                p = Product(i+1, 1, True, False)
                print(f"First instance of products Variant {i+1} generated for production")
                total_instances.append(p)

        print(total_instances)

        return tasks_for_allocation

    def task_sequencer(self):


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
