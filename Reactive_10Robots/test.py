import os
import datetime as dt
import matplotlib.pyplot as plt

file_time = dt.datetime.fromtimestamp(os.path.getmtime(__file__))
# print(file_time.strftime("%d_%m_%Y_%H_%M"))

curr_time = file_time.strftime("%d_%m_%Y_%H_%M")

folder_name = "results/" + curr_time

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

target = f"results/{folder_name}.pdf"
print("The filename", target)

# x = [1, 2, 3]
# # corresponding y axis values
# y = [2, 4, 1]
#
# # plotting the points
# plt.plot(x, y)
#
# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')
#
# # giving a title to my graph
# plt.title('My first graph!')
#
# # function to show the plot
# plt.savefig(target)


