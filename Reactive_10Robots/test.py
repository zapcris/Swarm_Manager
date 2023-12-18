import sys
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
batch = [[1, 4, 6, 7],
         [2, 3, 6, 6],
         [6, 7, 4, 3],
         [5, 8, 4, 3, 2, 5, ]]


def vc_sequence(batch_sequence):
    new_batch = []
    for i, prod_sequence in enumerate(batch_sequence):
        prod_sequence.insert(0, 11+i)
        prod_sequence.append(50)
        new_batch.append(prod_sequence)

    return new_batch


print(vc_sequence(batch))
