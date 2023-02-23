import sys
from dataclasses import dataclass

### sink placement 12###
## Source = 0 , Cell type = 1 , Server type =2 , Sink = 3######

order = {
        "Name": "Test",
        "PV": 10,
        "sequence": [[11, 1, 3, 5, 6, 8, 9, 12],
                      [11, 2, 4, 5, 7, 8, 10, 12],
                      [11, 3, 5, 6, 8, 9, 10, 12],
                      [11, 5, 7, 8, 9, 10, 12],
                      [11, 1, 4, 5, 7, 8, 9, 10, 12],
                      [11, 2, 5, 6, 8, 10, 12],
                      [11, 3, 6, 8, 2, 4, 3, 12],
                      [11, 4, 5, 6, 8, 10, 7, 12],
                      [11, 3, 4, 6, 1, 8, 9, 10, 12],
                      [11, 2, 4, 6, 8, 5, 7, 9, 10, 12]
                      ],

        "PI"    : [1,1,1,1,1,1,1,1,1,1],
        "Wk_type" : [0,1,1,1,1,1,1,1,1,1,1,3]

}

#print(order["sequence"])
## status : Pending / Executing / Performed
@dataclass
class task:
    id : int
    type: int
    command: []
    product: int
    Status: str

class Task_PG:

    def __init__(self, order):
        self.order = order

    def task_list(self):
        task_list = []
        tl = []
        n = 0
        task_dict_list = []
        task_enum = 0
        t2 = []
        seq = self.order["sequence"]
        for i in range(len(seq)):
            tl = []
            #task_list.append([0, i+1])
            for j in range(len(seq[i]) - 1):
                # print(graph[i][j], graph[i][j+1])
                tasks = [seq[i][j], seq[i][j + 1]]
                tl.append(tasks)
            task_list.append(tl)

        for t1 in enumerate(task_list):
              for t2 in t1[1]:
                n = n+1
                #print(n,t1[0],t2[0], t2[1])
                if t2[0] == 11 or t2[1] ==11:
                    type = 1
                elif t2[0] == 12 or t2[1] ==12:
                    type = 4
                else:
                    type = 2
                task_node = task(n, type, t2, t1[0]+1, "Pending")
                task_dict_list.append(task_node)

        return task_dict_list

    #def graph(self):


### instantiate order
test_order = Task_PG(order)
task_list = test_order.task_list()

print(task_list)



