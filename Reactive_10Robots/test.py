
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

opcua_cmd = "q2"

if opcua_cmd == "pick" or opcua_cmd == "drop" or opcua_cmd == "sink":
    base = True
    q1 = False
    q2 = False
elif opcua_cmd == "q1":
    base = False
    q1 = True
    q2 = False
elif opcua_cmd == "q2":
    base = False
    q1 = False
    q2 = True

print(base, q1, q2)