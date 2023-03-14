from Greedy_implementation.SM07_Robot_agent import T_robot, W_robot


class Task_Allocator_agent:

    def __init__(self):
        #self.global_task = global_task
        self.bid_data = []
        self.t_robot = T_robot


    def step_allocation(self, task_for_allocation, product_obj):
        for i, (task, prod) in enumerate(zip(task_for_allocation, product_obj)):
            #### reset received bid data list for every new task ##############
            self.bid_data = []
            for j, tr in enumerate(self.t_robot):
                #print(i,j)
                self.broadcast_bid(j, task)
            self.assign_bid(task, prod, i)
            #print(self.bid_data)
        #task_for_allocation.append(Task(0, 0, [0, 0], 0, 0, False, "Final_Task", 999))
        return task_for_allocation, product_obj


    def bulk_allocation(self):
        for i, task in enumerate(self.t_robot):
            #### reset received bid data list for every new task ##############
            self.bid_data = []
            for j, tr in enumerate(self.t_robot):
                #print(i,j)
                self.broadcast_bid(j, task)
            #self.assign_bid(task, i)
            #print(self.bid_data)
            if i == 2:
                break
        return None

    def broadcast_bid(self, i, task):
        bid = self.t_robot[i].bid(task)
        print(f"{bid} Bid Received from Robot {i+1} for task {task}")
        self.bid_data.append(bid)
        return self.bid_data



    def assign_bid(self, task, product, i):
        print(self.bid_data)
        min_val = min(self.bid_data)
        min_index = self.bid_data.index(min_val)
        target_wk = task.command[1]
        if min_val <= 99999999999:
            print(f"Minimum bid value found at Robot {min_index+1}")
            task.assign(robot=min_index + 1)
            product.to_robot(robot=min_index + 1)
            #self.t_robot[i].task_assigned()
            ### assigned task and product to robot agents here ####
            T_robot[i].task_assigned(task)
            T_robot[i].prod_assigned(product)


            print(f"Task and Product assigned to robot {min_index+1}")
            print("New task status", task)
            print("New product status", product)

        else:
            print(f"No minimum bidder found")

    def deassign_task(self):
        ### for future implementation
        return None


    def override_task(self):

        return None

