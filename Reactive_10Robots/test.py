from datetime import datetime

import pandas as pd

excel_file_path = 'products.xlsx'
data = [[] for i in range(100)]
data2 = [[] for i in range(100)]
product_stats = [[200, 100, 400, 500], [200, 100, 400, 500], [200, 100, 400, 500], [200, 100, 400, 500]]
makespan = [1000, 2000, 3000, 5000]
prod_name = ["PV-3_PI-1", "PV-2_PI-1", "PV-2_PI-2", "PV-1_PI-1"]
column = ["Station", "Position", "Start time", "Stop time", "Total_Time"]
column2 = ["Product", "Makespan", "Transfer time", "Blockage time", "Process time", "Idle time"]
print(data)
excel_writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')

obj1 = {"sts": "Source",
        "tstamp": datetime.now()
        }

obj2 = {"sts": "Transfer",
        "dtime": 100.23,
        "tr_no": 2,
        "drop": 4,
        }

obj3 = {"sts": "Transfer",
        "dtime": 100.23,
        "tr_no": 3,
        "drop": 4,
        }

obj4 = {"sts": "Wait",
        "dtime": 20.23,
        "tr_no": 4,
        "drop": 6,
        }

obj5 = {"sts": "Process",
        "dtime": 45.23,
        "wk_no": 7
        }

obj6 = {"sts": "Sink",
        "tstamp": datetime.now()
        }

objects = [obj1, obj2, obj3, obj4, obj5, obj6]

print(object)

for i, obj in enumerate(objects):
    print(i, obj)
    if obj["sts"] == "Source":
        data[i].append(obj["sts"])
        data[i].append(None)
        data[i].append(obj["tstamp"].strftime("%m/%d/%Y, %H:%M:%S"))
        data[i].append(None)
        data[i].append(None)
    elif obj["sts"] == "Transfer":
        str = f"{obj["sts"]} "
        data[i].append(str)
        str2 = f" To workstation {obj["drop"]} by Robot {obj["tr_no"]} "
        data[i].append(str2)
        data[i].append(None)
        data[i].append(None)
        data[i].append(int(obj["dtime"]))
    elif obj["sts"] == "Wait":
        str = f"{obj["sts"]} "
        data[i].append(str)
        str2 = f"At workstation {obj["drop"]} by Robot {obj["tr_no"]} "
        data[i].append(str2)
        data[i].append(None)
        data[i].append(None)
        data[i].append(int(obj["dtime"]))
    elif obj["sts"] == "Process":
        str = f"{obj["sts"]} "
        data[i].append(str)
        str2 = f"At workstation {obj["wk_no"]}  "
        data[i].append(str2)
        data[i].append(None)
        data[i].append(None)
        data[i].append(int(obj["dtime"]))
    elif obj["sts"] == "Sink":
        data[i].append(obj["sts"])
        data[i].append(None)
        data[i].append(None)
        data[i].append(obj["tstamp"].strftime("%m/%d/%Y, %H:%M:%S"))
        data[i].append(None)

for i, (name, times, span) in enumerate(zip(prod_name, product_stats, makespan)):
    data2[i].append(name)
    data2[i].append(span)
    data2[i].append(times[0])
    data2[i].append(times[1])
    data2[i].append(times[2])
    data2[i].append(times[3])

prod_summary = [ele for ele in data2 if ele != []]
print(prod_summary)
sorted_list = sorted(prod_summary, key=lambda x: x[0])
print(sorted_list)

df = pd.DataFrame(data, columns=column)
df2 = pd.DataFrame(sorted_list, columns=column2)
df_transposed = df.transpose()
str_name = f"{1}_{1}"
sheet_name = str_name.replace(' ', '_')  # Use a modified name as the sheet name
df.to_excel(excel_writer, sheet_name=sheet_name, index=False, header=True)
df2.to_excel(excel_writer, sheet_name="summary", index=False, header=True)
# Save the Excel file
excel_writer._save()
