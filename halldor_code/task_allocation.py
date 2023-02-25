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
        for i, tr in enumerate(T_robot):
            for j, task in enumerate(self.global_task):
                #print(i,j)
                self.broadcast_bid(i, task, T_robot)

            self.Allocate_bid()
            #break

        return None

    def broadcast_bid(self,i,task,T_robot):
        bid = T_robot[i].bid(task)
        #print(bid)
        self.bid_data.append(bid)
        #print(self.bid_data)
        return self.bid_data



    def Allocate_bid(self):
        print("Minimal bid ", min(self.bid_data))

        send to scheduler queue





### PROACTIVE TASK ALLOCATION#####