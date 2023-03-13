from Greedy_implementation.SM10_Product_Task import Task

a = [10, 20 ,30, 40]
b = []

if b:
    print("list has elements")
else:
    print("list is empty")


task = Task(id=1, allocation=True, command=[1,2], robot=1, type=1, pV=1, pI=1,status="New")


print(task.command[1])