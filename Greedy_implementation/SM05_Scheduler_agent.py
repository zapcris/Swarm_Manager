from queue import Queue
from Greedy_implementation.SM10_Product_Task import Product, Task


class Scheduling_agent:

    def __init__(self, order, product_task, T_robot):

        self.order = order
        self.robots = T_robot
        self.active_products = []
        self.remaining_order = order["PI"]
        self.product_task = product_task
        self.finished_product = []
        self.product_seq_ID = []
        self.seq_order()
        self.pCount = 0
        self.running_task = []
        self.q = Queue()

    def seq_order(self):
        for i in range(self.order["PV"]):
            self.product_seq_ID.append(i + 1)

    def process_task_executed(self, product):
        for prod in self.active_products:
            if prod.pv_Id == product.pv_Id and prod.pi_Id == product.pi_Id:
                prod = product
                print(f"Active product list updated inside Scheduler with {prod}")
            else:
                pass


    def prod_completed(self, prod_list):
        for product in prod_list:
            self.finished_product.append(product)
            for old_prod in self.active_products:
                if old_prod.pv_Id == product.pv_Id and old_prod.pi_Id == product.pi_Id:
                    del_pv = product.pv_Id
                    del_pi = product.pi_Id
                    index = self.active_products.index(old_prod)
                    if product.pi_Id == product.last_instance:
                        e = self.remaining_order[del_pv - 1]
                        self.remaining_order[del_pv - 1] = 0
                        print(f"The product variant {del_pv} removed from remaining order list inside Scheduler")
                        self.active_products.pop(index)
                        print(f"The product variant {del_pv} deleted from the Scheduler")
                        self.add_new_variant(del_pv)
                        #### added new product variant if product was last instance#####
                    else:
                        e = self.remaining_order[del_pv - 1]
                        self.remaining_order[del_pv - 1] = e - 1
                        print(f"The product instance reduced in remaining order list inside Scheduler")
                        self.active_products.pop(index)
                        print(f"The product Instance {del_pi} deleted from the Scheduler")
                        self.add_new_instance(del_pv, del_pi)
                        #### added new instance if product wasn't the last one#####
                else:
                    print("The product to be deleted not found in the active product list inside scheduler")

        tasks_for_allocation = self.task_evaluation()


        return tasks_for_allocation, self.active_products

    def add_new_variant(self, pv_Id):
        print(f"Remaining order {self.remaining_order}")
        if self.remaining_order[pv_Id - 1] == 0:
            new_active_list = self.active_products
            for i, order in enumerate(self.remaining_order):
                for product in self.active_products:
                    if product.pv_Id - 1 == i and order == 0:
                        new_active_list.remove(product)
                    else:
                        pass
            self.active_product = new_active_list
            print(f"Active product list update to variants inside Scheduler")

        else:
            print(f"The product variant {pv_Id} was not finished in the remaining order list")


        return None

    def add_new_instance(self, pv_Id, pi_Id):
        new_Inst = pi_Id+1
        ## new task list injected into the current product object ########
        product = Product(pv_Id=pv_Id, pi_Id=new_Inst, task_list=self.product_task[pv_Id-1], inProduction=True, finished=False,
                            last_instance=self.order["PI"][pv_Id-1], robot=0, wk=0, released=False)
        self.active_products.append(product)
        print(f"New Product instance {new_Inst} from Product variant {pv_Id} added to active list")


    def initialize_production(self):

        #### Initialization of Products based on total available robots ######
        if self.order["PV"] >= len(self.robots):
            for i, r in enumerate(self.robots):
                ########### encapsulated task sequence object for every product instance #######
                p = Product(pv_Id=i + 1, pi_Id=1, task_list=self.product_task[i], inProduction=True, finished=False,
                            last_instance=self.order["PI"][i], robot=0, wk=0,released=False)

                print(f"First instance of products Variant {i + 1} generated for production")
                self.active_products.append(p)
                self.pCount = i + 1
        else:  ###### if total robots greater than product variants############
            for i in range(self.order["PV"]):
                p = Product(pv_Id=i + 1, pi_Id=1, task_list=self.product_task[i], inProduction=True, finished=False,
                            last_instance=self.order["PI"][i], robot=0, wk=0,released=False)
                print(f"First instance of products Variant {i + 1} generated for production")
                self.active_products.append(p)
                self.pCount = i + 1

        initial_allocation = self.task_evaluation()

        return initial_allocation, self.active_products

    ######### Triggered after initial production queue is executed in Execution Thread###########
    # def normal_production(self):
    #     for i, product in enumerate(self.active_products):
    #
    #         if product["inProduction"] == True and len(product["task_list"]) == 0 and product["pi_Id"] == product[
    #             "last_instance"]:
    #             print(f"Product variant has been completed and to be deleted", product["pv_Id"])
    #             product.remove_from_production()
    #             product.pfinished()
    #             self.finished_product.append(product)
    #             print(self.product_seq_ID)
    #             self.product_seq_ID.remove(product["pv_Id"])
    #             self.active_products.remove(product)
    #             sleep(0.2)
    #             print("Adding new product variant to active production list")
    #             p = SM10_Product_Task.Product(pv_Id=self.pCount, pi_Id=1, task_list=self.product_task[self.pCount - 1],
    #                         inProduction=True, finished=False, last_instance=self.order["PI"][self.pCount - 1], robot=0,
    #                         wk=0,released=False)
    #             self.active_products.append(p)
    #
    #         elif product["inProduction"] == True and len(product["task_list"]) == 0 and product["pi_Id"] != product[
    #             "last_instance"]:
    #             print("Product instance upgraded and changed for same product variant")
    #             product.remove_from_production()
    #             product.pfinished()
    #             old_pi = product["pi_Id"]
    #             self.finished_product.append(product)
    #             self.active_products.remove(product)
    #             sleep(0.2)
    #             print("Adding new product instance of same variant to active production list")
    #             p = SM10_Product_Task.Product(pv_Id=self.pCount, pi_Id=old_pi + 1, task_list=self.product_task[self.pCount - 1],
    #                         inProduction=True, finished=False, last_instance=self.order["PI"][self.pCount - 1], robot=0,
    #                         wk=0,released=False)
    #             self.active_products.append(p)
    #
    #         else:
    #             print("Continue with same product variant and instance resp.", product["pv_Id"], product["pi_Id"])
    #     normal_allocation = self.initial_allocation()
    #
    #     return normal_allocation

    def normalized_production(self, product_list):
        task_for_allocation = []
        for new_product in product_list:

            for act_prod in self.active_products:
                if act_prod.pi_Id == new_product.pi_Id and act_prod.pv_Id == new_product.pv_Id:
                    act_prod = new_product
                    ###print(f" product variant {act_prod.pi_Id} and {act_prod.pv_Id} changed in Scheduler active list")
                else:
                    pass

            cmd = new_product.task_list[0]
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
    # def normalized_allocation(self):
    #     try:
    #         while True:
    #             Task_List = []
    #             Product_List = []
    #             product = self.q.get(block=False)
    #             done = False
    #             while not done:
    #                 try:
    #                     cmd = product.task_list[0]
    #                     print(f"product task flow required before", product.task_list)
    #                     if cmd[0] == 11 or cmd[1] == 11:
    #                         type = 1
    #                     elif cmd[0] == 12 or cmd[1] == 12:
    #                         type = 4
    #                     else:
    #                         type = 2
    #                     TA = Task(id=1, type=type, command=cmd, pV=product.pv_Id, pI=product.pi_Id, allocation=False,
    #                               status="Pending", robot=999)
    #                     Task_List.append(TA)
    #                     Product_List.append(product)
    #                     #Greedy_Allocator.step_allocation(TA,product_obj=Product_List)
    #                     done = True
    #                 except Exception as e:
    #                     pass  # just try again to do stuff
    #             self.q.task_done()
    #     except:
    #         pass  # no more items




    ######## Dispatch Task to Task Allocator for broadcasting ###################
    def task_evaluation(self):
        task_for_allocation = []

        ######### Initial Release ########################
        for i, product in enumerate(self.active_products):
            cmd = product.task_list[0]
            print(f"Current product task flow required for {product.pv_Id, product.pi_Id}", product.task_list)
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




