import threading
from queue import Queue
from Greedy_implementation.SM10_Product_Task import Product, Task, Source
from datetime import datetime
from Greedy_implementation.SM11_Dashboard import production_time

app_close = threading.Event()
class Scheduling_agent:

    def __init__(self, order, product_task, T_robot):

        self.order = order
        self.robots = T_robot
        self.active_products = []
        self.remaining_variant = []
        self.product_task = product_task
        self.finished_product = []
        self.product_seq_ID = []
        # self.seq_order()
        self.pCount = 0
        self.running_task = []
        self.finished_variant = []
        self.q = Queue()
        self.planned_batch = int

    # def seq_order(self):
    #     for i in range(self.order["PV"]):
    #         self.product_seq_ID.append(i + 1)

    def process_task_executed(self, product):
        for prod in self.active_products:
            if prod.pv_Id == product.pv_Id and prod.pi_Id == product.pi_Id:
                prod = product
                print(f"Active product list updated inside Scheduler with {prod}")
            else:
                pass

    def prod_completed(self, product, product_tList):
        self.finished_product.append(product)
        new_product = Product(pv_Id=0, pi_Id=0, task_list=[], inProduction=False, finished=False, last_instance=0,
                              robot=99,
                              wk=0, released=False, tracking=[])
        for old_prod in self.active_products:
            if old_prod.pv_Id == product.pv_Id and old_prod.pi_Id == product.pi_Id:
                fin_pv = product.pv_Id
                fin_pi = product.pi_Id
                index = self.active_products.index(old_prod)
                if product.pi_Id >= product.last_instance:
                    self.finished_variant.append(product.pv_Id)
                    print(f"Product Variant {fin_pv} inserted into FINISHED VARIANT LIST")
                    # e = self.remaining_order[del_pv - 1]
                    # self.remaining_order[del_pv - 1] = 0
                    # print(f"The product variant {del_pv} removed from remaining order list inside Scheduler")
                    self.active_products.pop(index)
                    print(f"The product variant {fin_pv} deleted from the Scheduler Active product list")
                    new_product = self.add_new_variant(fin_pv, product_tList)
                    #### added new product variant if product was last instance#####
                elif product.pi_Id < product.last_instance:
                    # e = self.remaining_order[del_pv - 1]
                    # self.remaining_order[del_pv - 1] = e - 1
                    print(f"The product variant {fin_pv} instance decremented in remaining order list inside Scheduler")
                    self.active_products.pop(index)
                    print(f"The product Instance {fin_pi} deleted from the Scheduler")
                    new_product = self.add_new_instance(fin_pv, fin_pi, product_tList)
                    #### added new instance if product wasn't the last one#####

            else:
                print("The product to be deleted not found in the active product list inside scheduler")

        return new_product

    def add_new_variant(self, pv_Id, product_tList):
        print(f"Remaining variants in production: {self.remaining_variant}")
        if len(self.remaining_variant) > 0:
            new_variant = self.remaining_variant.pop(0)
            new_prod_var = Product(pv_Id=new_variant, pi_Id=1, task_list=product_tList[new_variant - 1],
                                   inProduction=True,
                                   finished=False,
                                   last_instance=self.order["PI"][new_variant - 1], robot=0, wk=0, released=False,
                                   tracking=[])
            ct = Source(tstamp=datetime.now())
            new_prod_var.tracking.append(ct)

            self.active_products.append(new_prod_var)
            print(f"New Product Variant {new_variant} and {new_prod_var}  added to active list")
            return new_prod_var
        elif len(self.finished_product) == self.planned_batch:
            print("Production completed")
            for i, product in enumerate(self.finished_product):
                print(f"Finished product {i} is {product}")
                print(f"It's tracking details are {product.tracking}")
            app_close.set()
            production_time(self.finished_product)

    def add_new_instance(self, pv_Id, pi_Id, product_tList):
        ## new task list injected into the current product object ########
        print("TASK LIST ", product_tList)
        new_instance = Product(pv_Id=pv_Id, pi_Id=pi_Id + 1, task_list=product_tList[pv_Id - 1], inProduction=True,
                               finished=False,
                               last_instance=self.order["PI"][pv_Id - 1], robot=0, wk=0, released=False, tracking=[])
        ct = Source(tstamp=datetime.now())
        new_instance.tracking.append(ct)
        self.active_products.append(new_instance)
        print(f"New Product {new_instance}  added to active list")

        return new_instance

    def initialize_production(self):
        print(self.order["PV"])
        self.planned_batch = 0
        for pv, pi in zip(self.order["PV"], self.order["PI"]):
            c = pv * pi
            self.planned_batch += c
        # print("Total batch size", self.planned_batch)

        for i, pv in enumerate(self.order["PV"]):
            if pv == 1:
                self.remaining_variant.append(i + 1)
        print("Remaining order list", self.remaining_variant)
        #### Initialization of Products based on total available robots ######
        if len(self.remaining_variant) >= len(self.robots):
            for i, r in enumerate(self.robots):
                ########### encapsulated task sequence object for every product instance #######
                variant = self.remaining_variant.pop(0)
                p = Product(pv_Id=variant, pi_Id=1, task_list=self.product_task[i], inProduction=True, finished=False,
                            last_instance=self.order["PI"][i], robot=0, wk=0, released=False, tracking=[])
                ct = Source(tstamp=datetime.now())
                p.tracking.append(ct)

                print(f"First instance of product type {variant} and product {p} generated for production")
                self.active_products.append(p)
                # self.pCount = i + 1
        else:  ###### if total robots greater than product variants############
            iterate_order = self.remaining_variant
            for i in range(len(iterate_order)):
                variant = self.remaining_variant.pop(0)
                p = Product(pv_Id=variant, pi_Id=1, task_list=self.product_task[i], inProduction=True, finished=False,
                            last_instance=self.order["PI"][i], robot=0, wk=0, released=False, tracking=[])
                ct = Source(tstamp=datetime.now())
                p.tracking.append(ct)
                print(f"First instance of product type {variant} and product {p} generated for production")
                self.active_products.append(p)
                # self.pCount = i + 1

        initial_allocation = self.task_evaluation()

        return initial_allocation, self.active_products

    ## Copy of working old initialization logic#####
    # def initialize_production(self):
    #
    #     #### Initialization of Products based on total available robots ######
    #     if self.order["PV"] >= len(self.robots):
    #         for i, r in enumerate(self.robots):
    #             ########### encapsulated task sequence object for every product instance #######
    #             p = Product(pv_Id=i + 1, pi_Id=1, task_list=self.product_task[i], inProduction=True, finished=False,
    #                         last_instance=self.order["PI"][i], robot=0, wk=0, released=False)
    #
    #             print(f"First instance of product type {i+1} and product {p} generated for production")
    #             self.active_products.append(p)
    #             self.pCount = i + 1
    #     else:  ###### if total robots greater than product variants############
    #         for i in range(self.order["PV"]):
    #             p = Product(pv_Id=i + 1, pi_Id=1, task_list=self.product_task[i], inProduction=True, finished=False,
    #                         last_instance=self.order["PI"][i], robot=0, wk=0, released=False)
    #             print(f"First instance of product type {i+1} and product {p} generated for production")
    #             self.active_products.append(p)
    #             self.pCount = i + 1
    #
    #     initial_allocation = self.task_evaluation()
    #
    #     return initial_allocation, self.active_products

    def normalized_production(self, product_list):
        task_for_allocation = []
        for new_product in product_list:

            for act_prod in self.active_products:
                if act_prod.pi_Id == new_product.pi_Id and act_prod.pv_Id == new_product.pv_Id:
                    act_prod = new_product
                    ###print(f" product variant {act_prod.pi_Id} and {act_prod.pv_Id} changed in Scheduler active list")
                else:
                    pass

            cmd = new_product.mission_list[0]
            ###print(f"Current product task flow required for {new_product.pv_Id, new_product.pi_Id}", new_product.task_list)
            if cmd[0] == 11 or cmd[1] == 11:
                type = 1
            elif cmd[0] == 12 or cmd[1] == 12:
                type = 4
            else:
                type = 2
            TA = Task(id=1, type=type, command=cmd, pV=new_product.pv_Id, pI=new_product.pi_Id,
                      allocation=False,
                      status="Pending", robot=999)

            task_for_allocation.append(TA)

        return task_for_allocation, product_list

    ######## Dispatch Task to Task Allocator for broadcasting ###################
    def task_evaluation(self):
        task_for_allocation = []

        ######### Initial Release ########################
        for i, product in enumerate(self.active_products):
            cmd = product.mission_list[0]
            print(f"Current product task flow required for {product.pv_Id, product.pi_Id}", product.mission_list)
            if cmd[0] == 11 or cmd[1] == 11:
                type = 1
            elif cmd[0] == 12 or cmd[1] == 12:
                type = 4
            else:
                type = 2
            TA = Task(id=i + 1, type=type, command=cmd, pV=product.pv_Id, pI=product.pi_Id, allocation=False,
                      status="Pending", robot=999)
            # product.dequeue()
            # print(f"product task flow required after", product["task_list"])
            task_for_allocation.append(TA)

        return task_for_allocation
