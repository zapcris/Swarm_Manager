
import queue

from Greedy_implementation.SM07_Robot_agent import T_robot

task_queue = queue.Queue()

### Task Allocation to robot bidders

### GREEDY TASK ALLOCATION #####
class Task_Allocation:

    def __init__(self, global_task, data_opcua, T_robot):

        self.global_task = global_task
        #self.auctioned_task = auctioned_task
        self.data_opcua = data_opcua
        self.bid_data = []
        self.t_robot = T_robot


    def step_allocation(self, task_for_allocation, product_obj):
        for i, (task, prod) in enumerate(zip(task_for_allocation, product_obj)):
            self.bid_data =[] #### reset received bid data list for every new task ##############

            for j, tr in enumerate(self.t_robot):
                #print(i,j)

                self.broadcast_bid(j, task)

            self.assign_bid(task, prod, i)
            #print(self.bid_data)

        #task_for_allocation.append(Task(0, 0, [0, 0], 0, 0, False, "Final_Task", 999))


        return task_for_allocation, product_obj


    def bulk_allocation(self):
        for i, task in enumerate(self.global_task):
            self.bid_data =[] #### reset received bid data list for every new task ##############
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
        print(f"Minimum bid value found at Robot {min_index+1}")
        task.assign(robot=min_index + 1)
        product.to_robot(robot=min_index + 1)
        #self.t_robot[i].task_assigned()
        T_robot[i].task_assigned(task)
        T_robot[i].prod_assigned(product)

        print(f"Task allocated to robot {min_index+1}")
        print("New task status", task)
        print("New product status", product)



    def deassign_task(self):
        ### for future implementation

        return None


    def override_task(self):

        return None


