from dataclasses import dataclass
from time import sleep
from queue import Queue
from threading import Thread
from Task_Planner import Task, Task_PG
from Robot_agent import Transfer_robot



@dataclass
class Product:
    pv_Id: int
    pi_Id: int
    task_list: []
    inProduction: False
    finished: False
    last_instance: int
    # current_position = []
    # start_time = time
    # finish_time = time


    # def __init__(self, pi_Id, pv_Id, task_list, inProduction, finished, last_instance):
    #     self.pi_ID = pi_Id
    #     self.pv_ID = pv_Id
    #     self.inProduction = inProduction
    #     self.produced = finished
    #     self.task_list = task_list
    #     self.last_instance = last_instance



    # def __str__(self):
    #     return f'The product instance is {self.pi}'
    #
    # def __repr__(self):
    #     return self

    def __getitem__(self, pv_Id):
        return getattr(self, pv_Id)

    def remove_from_production(self):
        object.__setattr__(self, 'inProduction', False)


    def pfinished(self):
        object.__setattr__(self, 'finished', True)
    #
    # def reset_Instance(self):
    #     object.__setattr__(self, 'last_instance', 0)

    def dequeue(self):
        if len(self.task_list) > 0 :
            self.task_list.pop(0)
        return (self)


class Joint_Scheduler:

    def __init__(self, order, global_task, product_task, data_opcua, T_robot):

        self.global_task = global_task
        self.data_opcua = data_opcua
        self.order = order
        self.robots = T_robot
        self.active_products = []
        self.product_task = product_task
        self.finished_product = []
        self.product_seq_ID = []
        self.seq_order()
        self.pCount = 0
        self.running_task = []



    def seq_order(self):
        for i in range(self.order["PV"]):
            self.product_seq_ID.append(i+1)


    def initialize_production(self):

        #### Initialization of Products based on total available robots ######
        if self.order["PV"] >= len(self.robots):
            for i, r in enumerate(self.robots):
         ########### encapsulated task sequence object for every product instance #######
                p = Product(pv_Id=i + 1, pi_Id=1, task_list=self.product_task[i], inProduction=True, finished=False, last_instance=self.order["PI"][i])


                print(f"First instance of products Variant {i+1} generated for production")
                self.active_products.append(p)
                self.pCount = i+1
        else: ###### if total robots greater than product variants############
            for i in range(self.order["PV"]):
                p = Product(pv_Id=i + 1, pi_Id=1, task_list=self.product_task[i], inProduction=True, finished=False, last_instance=self.order["PI"][i])
                print(f"First instance of products Variant {i+1} generated for production")
                self.active_products.append(p)
                self.pCount = i+1


        initial_allocation = self.initial_allocation()

        return initial_allocation

 ######### Triggered after initial production queue is executed in Execution Thread###########
    def normal_production(self):
        for i, product in enumerate(self.active_products):

            if  product["inProduction"] == True and len(product["task_list"]) == 0 and product["pi_Id"] == product["last_instance"]:
                print(f"Product variant has been completed and to be deleted", product["pv_Id"])
                product.remove_from_production()
                product.pfinished()
                self.finished_product.append(product)
                print(self.product_seq_ID)
                self.product_seq_ID.remove(product["pv_Id"])
                self.active_products.remove(product)
                sleep(0.2)
                print("Adding new product variant to active production list")
                p = Product(pv_Id=self.pCount, pi_Id=1, task_list=self.product_task[self.pCount-1],
                            inProduction=True, finished=False, last_instance=self.order["PI"][self.pCount-1])
                self.active_products.append(p)

            elif product["inProduction"] == True and len(product["task_list"]) == 0 and product["pi_Id"] != product["last_instance"]:
                print("Product instance upgraded and changed for same product variant")
                product.remove_from_production()
                product.pfinished()
                old_pi = product["pi_Id"]
                self.finished_product.append(product)
                self.active_products.remove(product)
                sleep(0.2)
                print("Adding new product instance of same variant to active production list")
                p = Product(pv_Id=self.pCount, pi_Id=old_pi+1, task_list=self.product_task[self.pCount-1],
                            inProduction=True, finished=False, last_instance=self.order["PI"][self.pCount-1])
                self.active_products.append(p)

            else:
                print("Continue with same product variant and instance resp.",product["pv_Id"], product["pi_Id"])
        normal_allocation = self.initial_allocation()

        return normal_allocation



######## Dispatch Task to Task Allocator for broadcasting ###################
    def initial_allocation(self):
        task_for_allocation = []

        ######### Initial Release ########################
        for i, product in enumerate(self.active_products):
            cmd = product["task_list"][0]
            print(f"product task flow required before", product["task_list"])
            TA = Task(i+1, 1, cmd, i+1, 1, False, "Pending", 999)
            product.dequeue()
            print(f"product task flow required after", product["task_list"])
            task_for_allocation.append(TA)

        return task_for_allocation

    # def normal_allocation(self):
    #     task_normal_allocation = []
    #     if last task executed ?
    #
    #     then allocate the next task to queue
    #
    #
    #
    #     return task_for_allocation





    def release_execCommand(self):
        task_for_execution = []

        return task_for_execution

    def proactive_scheduler(self):
        global_STN = Queue()
        ############# Future implementation ##############
        return global_STN
