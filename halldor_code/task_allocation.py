from dataclasses import dataclass
import queue

task_queue = queue.Queue()

### Task Allocation to robot bidders

### GREEDY TASK ALLOCATION #####
class Task_Allocation:

    def __init__(self, global_task, data_opcua):

        self.global_task = global_task
        #self.auctioned_task = auctioned_task
        self.data_opcua = data_opcua
        self.bid_data = []


    def bid_counter(self, T_robot):
        for i, task in enumerate(self.global_task):
            self.bid_data =[] #### reset received bid data list for every new task ##############
            for j, tr in enumerate(T_robot):
                #print(i,j)
                self.broadcast_bid(j, task, T_robot)

            self.Allocate_bid(task)
            #print(self.bid_data)
            if i == 1:
                break

        return None

    def broadcast_bid(self,i,task,T_robot):
        if self.data_opcua["rob_busy"][i] == False:
            bid = T_robot[i].bid(task)
        else:
            bid = 99999999 ## inifite bid value if robot is busy ######
        print(f"{bid} Bid Received from Robot {i+1} for task {task}")
        self.bid_data.append(bid)

        return self.bid_data



    def Allocate_bid(self,task):
        print(self.bid_data)
        min_val = min(self.bid_data)
        min_index = self.bid_data.index(min_val)
        print(f"Minimum bid value found at Robot {min_index+1}")
        task.assign(robot=min_index+1)
        print(f"Task allocated to robot {min_index+1}")
        print("New task status", task)


        #send to scheduler queue





### PROACTIVE TASK ALLOCATION#####