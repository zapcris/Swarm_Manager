


import threading




class Reactive_scheduling:

    def __init__(self, global_task, data_opcua):
        self.global_task = global_task
        self.data_opcua = data_opcua

    def greedy_allocator(self):
        tasks_for_allocation = []


        return tasks_for_allocation

    def scheduling_queue(self):
        queue_list = []


        return queue_list


    def release_task(self):
        task_for_execution = []

        return task_for_execution

def worker(q):
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()

# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True).start()

# Send thirty task requests to the worker.
for item in range(30):
    q.put(item)

# Block until all tasks are done.
q.join()
print('All work completed')
