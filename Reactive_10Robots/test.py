
import datetime as dt
import os

file_time = dt.datetime.fromtimestamp(os.path.getmtime(__file__))

now = dt.datetime.now()
curr_time = now.strftime("%d_%m_%Y_%H_%M")
folder_name = "results/" + curr_time
print("geneated folder name", folder_name)
#os.makedirs(folder_name)

cmd = ['', 'a,18', '', '', '', '', '', '', '', '', '']
new_arr = cmd[:10]
print(new_arr)