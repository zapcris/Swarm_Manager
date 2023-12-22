import math
import os
import queue
import datetime as dt
from scipy.spatial import distance

produts = [1, 2, 3, 4, 5, 6, 7, 8]
priority = [1, 1, 1, 1, 4, 7, 6, 1]
test = [(1, 4), (1, 5), (1, 6)]

waiting_list = queue.PriorityQueue()
pqueue = queue.PriorityQueue(maxsize=3)

for test in test:
    q_data = test
    if not pqueue.full():
        pqueue.put_nowait(q_data)
        print(pqueue.qsize())
    else:
        waiting_list.put(q_data)
print("The waiting priority queue", waiting_list.queue)

print("The queue", pqueue.queue)

for i, data in enumerate(pqueue.queue):
    print(f"")

if pqueue.queue[0][1] == 4:
    print(f"Robot3 queued for base position")

for data in pqueue.queue:
    print(data[1])

queue_pos = 0
for i, robot in enumerate(pqueue.queue):
    if robot[1] == 6:
        queue_pos = i + 1

print("queue position", queue_pos)

item = pqueue.get()

a = [10, 20, 40]

a.pop(0)

print(a)

a.append(99)

print(a)


def maintain_max_3_elements(arr, new_element):
    if len(arr) < 3:
        arr.append(new_element)
        arr.sort(reverse=True)
    elif new_element > arr[-1]:
        arr.pop()
        arr.append(new_element)
        arr.sort(reverse=True)


# Example usage:
my_array = [10, 5, 8]

print("Original array:", my_array)

maintain_max_3_elements(my_array, 12)
print("After adding 12:", my_array)

maintain_max_3_elements(my_array, 6)
print("After adding 6:", my_array)

maintain_max_3_elements(my_array, 15)
print("After adding 15:", my_array)

task = 30
robot = [10, 20, 40, 50, 70]

if any(task for x in robot):
    print("Found")

# id = 1
# str = f"Robot {id}"
# process_queue = ["" for _ in range(3)]
#
# process_queue.append(str)
#
# print(process_queue)
#
# process_queue.pop


while not pqueue.empty():
    item = pqueue.get()
    # print("order", item)
p1 = [9806.01443856, 14251.0105294]
p2 = [8001.0, 38301.0]
p3 = [8001, 10001]
a = math.dist(p1, p2)
print("Distance:", a)

a = [20]

if 40 in a and a:
    print("element popped from array", a.pop(0))
else:
    print("Error")
