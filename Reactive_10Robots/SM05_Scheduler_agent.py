from Reactive_10Robots.SM10_Product_Task import Product, Task, Source
from datetime import datetime
from Reactive_10Robots.SM11_Dashboard import production_time
from time import sleep

class Scheduling_agent:

    def __init__(self, order, product_missions, T_robot):

        self.order = order
        self.robots = T_robot
        self.active_products = []
        self.remaining_variant = []
        self.remaining_instance = []
        self.product_missions = product_missions
        self.finished_product = []
        self.product_seq_ID = []
        # self.seq_order()
        self.pCount = 0
        self.running_task = []
        self.finished_variant = []
        # self.q = Queue()
        self.planned_batch = 0
        self.planned_variants = []
        self.total_prod = 0
        self.mission_q = []

    def prod_completed(self, product, product_tList):
        self.finished_product.append(product)
        self.total_prod = self.planned_batch - sum(self.remaining_instance)
        print(f"Product {product} added to the completed list")
        new_product = Product(pv_Id=0, pi_Id=0, mission_list=[], inProduction=False, finished=False, last_instance=0,
                              robot=0,
                              wk=0, released=False, tracking=[], priority=0,
                              current_mission=[], task=[])
        for old_prod in self.active_products:
            if old_prod.pv_Id == product.pv_Id and old_prod.pi_Id == product.pi_Id:  ### and self.total_prod < len(self.robots) - 2:
                fin_pv = product.pv_Id
                fin_pi = product.pi_Id
                index = self.active_products.index(old_prod)
                if product.pi_Id >= product.last_instance and len(self.remaining_variant) > 0:
                    print(
                        f"Sinked Product {product.pv_Id} Instance {product.pi_Id} has last instance {product.last_instance}")
                    print("Trying to add new variant into production")
                    print("Active Active products:", self.active_products)
                    print("Active Finished Products:", self.finished_product)
                    print("Active Finished Variants", self.finished_variant)
                    print("Remaining product list", self.remaining_instance)
                    self.finished_variant.append(product.pv_Id)
                    # print(f"Product Variant {fin_pv} inserted into FINISHED VARIANT LIST")
                    self.active_products.pop(index)
                    # print(f"The product variant {fin_pv} deleted from the Scheduler Active product list")
                    new_product = self.add_new_variant(product_tList)
                    break
                    #### added new product variant if product was last instance#####
                elif product.pi_Id < product.last_instance and sum(self.remaining_instance) > 0:
                    print(
                        f"Sinked Product {product.pv_Id} Instance {product.pi_Id} has last instance {product.last_instance}")
                    print("Trying to add new instance into production")
                    # print(f"The product variant {fin_pv} instance decremented in remaining order list inside Scheduler")
                    self.active_products.pop(index)
                    # print(f"The product Instance {fin_pi} deleted from the Scheduler")
                    new_product = self.add_new_instance(fin_pv, fin_pi, product_tList)
                    break
                    #### added new instance if product wasn't the last one#####

            else:
                #print("The product to be deleted not found in the active product list inside scheduler")
                new_product = None

        return new_product

    def robot_done(self, product, product_tList):
        """
        :param product: The product handled by the robot recently
        :param product_tList: The global task list
        :return: The next product to be handled after product task is executed, The priority is given to next variant
                (as the product flow will be different and less chance of waiting in the queue workstation)
                if no new variant waiting for initialization then select the instance from other already initialized variant,
                 The last priority is to new instance of self variant.
        """
        product_added = False
        self.total_prod = self.planned_batch - sum(self.remaining_instance)
        if len(self.remaining_variant) > 0:  ####and self.total_prod < len(self.robots) - 2:
            new_product = self.add_new_variant(product_tList)
            # print("New product added", new_product)
            print("Scheduler returned from 1", new_product)
            return new_product
        elif len(self.remaining_variant) == 0:
            for i, var in enumerate(self.remaining_instance):
                for act in self.active_products:
                    if act.pv_Id != i + 1 and var > 0 and product_added == False:  ###and self.total_prod < len(self.robots) - 2:
                        curr_inst = self.order["PI"][i] - var
                        new_product = self.add_new_instance(i + 1, curr_inst, product_tList)
                        product_added = True
                        print("Scheduler returned from 2", new_product)
                        return new_product
                        # print("New product added into production", new_product)
                    elif act.pv_Id == i + 1 and var > 0 and product.pv_Id != i + 1 and product_added == False:  ### and self.total_prod < len(
                        ## self.robots) - 2:
                        curr_inst = self.order["PI"][i] - var
                        new_product = self.add_new_instance(i + 1, curr_inst, product_tList)
                        product_added = True
                        print("Scheduler returned from 3", new_product)
                        return new_product
                    elif act.pv_Id == i + 1 and var > 0 and product.pv_Id == i + 1 and product_added == False:  ### and self.total_prod < len(
                        ###   self.robots) - 2:
                        new_product = self.add_new_instance(product.pv_Id, product.pi_Id, product_tList)
                        # print("Next instance of same product variant is preferred")
                        product_added = True
                        print("Scheduler returned from 4", new_product)
                        return new_product

        else:
            # print("No product to be added in the production")
            return None

    def add_new_variant(self, product_tList):
        # print(f"Remaining variants in production: {self.remaining_variant}")
        # print("Remaining instances in production", self.remaining_instance)
        if len(self.remaining_variant) > 0:
            new_variant = self.remaining_variant.pop(0)
            self.remaining_instance[new_variant - 1] -= 1
            new_prod_var = Product(pv_Id=new_variant, pi_Id=1, mission_list=product_tList[new_variant - 1],
                                   inProduction=True,
                                   finished=False,
                                   last_instance=self.order["PI"][new_variant - 1], robot=99, wk=new_variant+10,
                                   released=False, tracking=[], priority=self.order["PV_priority"][new_variant - 1],
                                   current_mission=product_tList[new_variant - 1][0], task=[99, 99])
            ct = Source(tstamp=datetime.now())
            new_prod_var.tracking.append(ct)

            self.active_products.append(new_prod_var)
            # print(f"New Product Variant {new_variant} and {new_prod_var}  added to active list")
            return new_prod_var

    def production_end(self):
        # print("Production completed")
        # for i, product in enumerate(self.finished_product):
        #     a =100
        # print(f"Finished product {i} is {product}")
        # print(f"It's tracking details are {product.tracking}")
        print("Total Finished products", len(self.finished_product))
        print("Total Planned Batch is", self.planned_batch)
        if len(self.finished_product) >= self.planned_batch:
            sleep(2)
            production_time(self.finished_product)
        # print("Production Stats generating")
        # app_close.set()

    def add_new_instance(self, pv_Id, pi_Id, product_tList):
        ## new task list injected into the current product object ########
        # print(f"Remaining variants in production: {self.remaining_variant}")
        # print("Remaining instances in production", self.remaining_instance)
        self.planned_variants.index(pv_Id)
        self.remaining_instance[pv_Id - 1] -= 1
        # print("Remaining instance list", self.remaining_instance)
        # print("TASK LIST ", product_tList)
        new_instance = Product(pv_Id=pv_Id, pi_Id=pi_Id + 1, mission_list=product_tList[pv_Id - 1], inProduction=True,
                               finished=False,
                               last_instance=self.order["PI"][pv_Id - 1], robot=99, wk=pv_Id+10, released=False,
                               tracking=[], priority=self.order["PV_priority"][pv_Id - 1],
                               current_mission=product_tList[pv_Id - 1][0], task=[99, 99])
        ct = Source(tstamp=datetime.now())
        new_instance.tracking.append(ct)
        self.active_products.append(new_instance)
        # print(f"New Product {new_instance}  added to active list")
        return new_instance

    def initialize_production(self, W_robot):
        # print(self.order["PV"])
        # self.planned_batch = 0
        for pv, pi in zip(self.order["PV"], self.order["PI"]):
            c = pv * pi
            self.planned_batch += c
        # print("Total batch size", self.planned_batch)
        for i, (pv, pi) in enumerate(zip((self.order["PV"]), (self.order["PI"]))):
            if pv == 1:
                self.remaining_variant.append(i + 1)
                self.planned_variants.append(i + 1)
                self.remaining_instance.append(pi)
            else:
                self.remaining_instance.append(0)
        # print("Remaining order list", self.remaining_variant)
        # print("Remaining instance list", self.remaining_instance)
        #### Initialization of Products based on total available robots ######
        if len(self.remaining_variant) >= len(self.robots):
            for i, r in enumerate(self.robots):
                if i <= len(self.robots):  ###- 3:  ## Only allow total robots -2 products###
                    ########### encapsulated task sequence object for every product instance #######
                    variant = self.remaining_variant.pop(0)
                    self.remaining_instance[variant - 1] -= 1
                    # print("Remaining instance list", self.remaining_instance)
                    p = Product(pv_Id=variant, pi_Id=1, mission_list=self.product_missions[variant-1], inProduction=True,
                                finished=False,
                                last_instance=self.order["PI"][i], robot=99, wk=variant+10, released=False,
                                tracking=[], priority=self.order["PV_priority"][variant - 1],
                                current_mission=self.product_missions[variant-1][0], task=[99, 99])
                    ct = Source(tstamp=datetime.now())
                    p.tracking.append(ct)
                    # print(f"First instance of product type {variant} and product {p} generated for production")
                    self.active_products.append(p)
                    # self.pCount = i + 1
        else:  ###### if total robots greater than product variants############
            iterate_order = self.remaining_variant
            for i in range(len(iterate_order)):
                variant = self.remaining_variant.pop(0)
                self.remaining_instance[variant - 1] -= 1
                # print("Remaining instance list", self.remaining_instance)
                p = Product(pv_Id=variant, pi_Id=1, mission_list=self.product_missions[variant-1], inProduction=True,
                            finished=False,
                            last_instance=self.order["PI"][i], robot=99, wk=variant+10, released=False,
                            tracking=[], priority=self.order["PV_priority"][variant - 1],
                            current_mission=self.product_missions[variant-1][0], task=[99, 99])
                ct = Source(tstamp=datetime.now())
                p.tracking.append(ct)
                # print(f"First instance of product type {variant} and product {p} generated for production")
                self.active_products.append(p)
                # self.pCount = i + 1
        initial_allocation = self.initial_evaluation(W_robot=W_robot)
        return initial_allocation, self.active_products

    def normalized_production(self, new_product, W_robot):

        ## Old logic here
        print("Check this error", new_product)
        ## old logic -without capability
        #cmd = new_product.mission_list[0]

        ## Generate Task command based on the capabilities of the Workstations
        cmd = self.generate_task(product=new_product, W_robot=W_robot)

        ###print(f"Current product task flow required for {new_product.pv_Id, new_product.pi_Id}", new_product.task_list)
        if 11 <= cmd[0] <= 20:
            type = 1  ## Task initiate from Source###
        elif (1 <= cmd[0] <= 10) or (1 <= cmd[1] <= 10):
            type = 7  ### Task Initiate Workstation###
        else:
            type = 11  ### Task Initiate for Sink###
        TA = Task(id=1, type=type, command=cmd, pV=new_product.pv_Id, pI=new_product.pi_Id,
                  allocation=False,
                  status="Pending", robot=999, step=type)
        # print("New task created ", TA)

        task_for_allocation = TA
        return task_for_allocation, new_product

    ######## Dispatch Task to Task Allocator for broadcasting ###################
    def initial_evaluation(self, W_robot):
        tasks_for_allocation = []
        ######### Initial Release ########################
        for i, product in enumerate(self.active_products):
            #cmd = product.mission_list[0]

            ## New capability based task assignment
            cmd = self.generate_task(product=product, W_robot=W_robot)

            # print(f"Current product task flow required for {product.pv_Id, product.pi_Id}", product.task_list)
            if 11 <= cmd[0] <= 20:
                type = 1  ### Task initiate from Source###
            elif (1 <= cmd[0] <= 10) or (1 <= cmd[1] <= 10):
                type = 7  ### Task Initiate Workstation###
            else:
                type = 11  ### Task Initiate for Sink###
            TA = Task(id=i + 1, type=type, command=cmd, pV=product.pv_Id, pI=product.pi_Id, allocation=False,
                      status="Pending", robot=999, step=1)
            tasks_for_allocation.append(TA)
        print("Check Task", tasks_for_allocation)

        return tasks_for_allocation

    def generate_task(self, product, W_robot):
        cmd = [0, 0]
        self.mission_q = [99 for _ in range(3)]  ## 99 denoting empty mission
        mission = product.current_mission
        print(f"Generated mission is {mission} for {product}")
        'Testing code for Capability based task assignment'
        cmd[0] = product.wk
        if 1 <= mission[1] <= 10:
            wk_options = [99 for _ in W_robot]
            print(wk_options)
            for wk in W_robot:
                if mission[1] in wk.capability:
                    ## Check for length of process queue and store in list##
                    wk_options.insert((wk.id-1), len(wk.pqueue))
                    print(f"The queue size for {wk.id} is {len(wk.pqueue)}")
            least_busy = min(wk_options)
            best_fit = wk_options.index(least_busy)
            ## Preference to same workstation and process number ####
            if not W_robot[mission[1]-1].pqueue:
                cmd[1] = mission[1]
            elif least_busy != 99 and W_robot[mission[1]-1].pqueue:
                cmd[1] = best_fit+1
                print(f"Workstation {cmd[1]} has the least queue size {least_busy}")
            else:
                raise Exception(f"ERROR : TASK not generated for the mission {mission}")
        else:
            ## No multi-capabilties for auxillary stations (source/sink)
            cmd[1] = mission[1]

        print(f"Task {cmd} generated for mission {mission}")
        product.current_mission = mission
        product.task = cmd
        return cmd
