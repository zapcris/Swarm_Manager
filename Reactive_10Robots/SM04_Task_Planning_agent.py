import queue



def generate_task(order):
    product_task = []
    seq = order["sequence"]
    for i in range(len(seq)):
        tl = []
        q = queue.Queue()
        # task_list.append([0, i+1])
        for j in range(len(seq[i]) - 1):
            # print(graph[i][j], graph[i][j+1])
            tasks_arr = [seq[i][j], seq[i][j + 1]]
            tl.append(tasks_arr)
            q.put_nowait(tasks_arr)

        product_task.append(tl)

    return product_task


class Task_Planning_agent:

    def __init__(self, input_order):
        self.order = input_order

    def task_list(self):
        product_task = []
        task_queue = []
        tl = []
        n = 0
        global_task = []
        task_enum = 0
        t2 = []
        seq = self.order["sequence"]
        for i in range(len(seq)):
            tl = []
            q = queue.Queue()
            # task_list.append([0, i+1])
            for j in range(len(seq[i]) - 1):
                # print(graph[i][j], graph[i][j+1])
                tasks_arr = [seq[i][j], seq[i][j + 1]]
                tl.append(tasks_arr)
                q.put_nowait(tasks_arr)

            product_task.append(tl)
            task_queue.append(q)

        # for t in product_task:
        #     print(t)

        ########### Generate a global list of task objects ##############################
        total = []
        for i, p in enumerate(product_task):
            l = len(p) * self.order["PI"][i]
            total.append(l)
        # print(sum(total))

        for i, pt in enumerate(product_task):
            for pI in range(self.order["PI"][i]):
                for cmd in pt:
                    n = n + 1
                    # print(n,t1[0],t2[0], t2[1])
                    if cmd[0] == 11 or cmd[1] == 11:
                        type = 1
                    elif cmd[0] == 12 or cmd[1] == 12:
                        type = 4
                    else:
                        type = 2
                    # task_node = Task(n, type, cmd, i + 1, pI+1,  False, "Pending", 999)
                    task_node = n
                    global_task.append(task_node)
                    # print(task_node)

        return product_task, global_task, task_queue