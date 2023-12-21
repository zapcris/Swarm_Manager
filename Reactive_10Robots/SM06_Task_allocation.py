class Task_Allocator_agent:

    def __init__(self):
        # self.global_task = global_task
        self.bid_data = []
        # self.t_robot = total_tr

    def step_allocation(self, task_for_allocation, product_obj, data_opcua, T_robot):
        # print("Step allocation started for robots", len(T_robot))
        for i, (tasks, prod) in enumerate(zip(task_for_allocation, product_obj)):
            #### reset received bid data list for every new task ##############
            self.bid_data = []
            task = tasks.command
            for j, tr in enumerate(T_robot):
                # print(i,j)
                bid = self.broadcast_task(j, task, data_opcua, T_robot)
                self.bid_data.append(bid)
            print("The Bid data list", self.bid_data)
            self.assign_bid(tasks, prod, T_robot)
            # print(self.bid_data)
        # task_for_allocation.append(Task(0, 0, [0, 0], 0, 0, False, "Final_Task", 999))
        return task_for_allocation, product_obj

    def normal_allocation(self, task_for_allocation, product_obj, data_opcua, T_robot):
        # print("bid data", self.bid_data)
        self.bid_data = []
        task = task_for_allocation.command
        for i, tr in enumerate(T_robot):
            # print("First allocation ",i)

            bid = self.broadcast_task(i, task, data_opcua, T_robot)
            self.bid_data.append(bid)
            # print("Broadcast robot no", i+1)
        print("The Bid data list", self.bid_data)
        self.assign_bid(task_for_allocation, product_obj, T_robot)
        return task_for_allocation, product_obj

    def broadcast_task(self, i, task, data_opcua, T_robot):
        # bid = self.t_robot[i].bid(task)
        # print("Broadcast started for robot", i+1)
        # print(data_opcua)
        #bid_data = []
        bid = T_robot[i].bid(auctioned_task=task, data_opcua=data_opcua)
        # print(f"{bid} Bid Received from Robot {i+1} for task {task}")
        #bid_data.append(bid)
        return bid

    def assign_bid(self, task, product, T_robot):
        # print("bid data", self.bid_data)
        min_val = min(self.bid_data)
        min_index = self.bid_data.index(min_val)
        target_wk = task.command[1]
        if min_val <= 999999:
            print(f"Minimum bid value found at Robot {min_index+1 }")
            task.assign(robot=min_index + 1)
            product.to_robot(robot=min_index + 1)
            # self.t_robot[i].task_assigned()
            ### assigned task and product to robot agents here ####
            # T_robot[i].task_assign(task)
            T_robot[min_index].assigned_task = True
            T_robot[min_index].task = task
            T_robot[min_index].free = False
            print(f"Task Allocated to robot {min_index + 1} is {task}")
            ## assign product to robot####
            # T_robot[i].product_assign(product)
            T_robot[min_index].product = product
            # print(f"Product Allocated to robot {min_index + 1} is {product}")

            # print("New task status", task)
            # print("New product status", product)

        else:
            print(f"No minimum bidder found")

    # def deassign_task(self):
    #     ### for future implementation
    #     return None

    def override_task(self):

        return None
