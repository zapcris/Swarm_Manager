from queue import Queue

# queue = Queue(maxsize=2)
#
# print(queue.qsize())
# queue.put('a')
# queue.put('b')
#
# print("\nFull: ", queue.full())
#
# print(queue.get())
# print(queue.get())
# print("\nEmpty: ", queue.empty())


# production_order = {}
#
# production_order["Name"] = "Test"
#
# print(production_order)
xyz = [True, True, True, False, True, True]

gen = [1 if i==True else 0 for i in xyz]

for x in gen:
    print(x)