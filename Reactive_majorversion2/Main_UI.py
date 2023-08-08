import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk

import numpy as np
import pymongo
from bson import ObjectId
from SM03_Manager import reconfigure_topology
from sklearn.preprocessing import MinMaxScaler

tree_stat_list = []
tree_top_list = []
def read_tree():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Topology_Manager"]
    mycol = mydb["Tree_Topologies"]

    #mydoc = mycol.distinct("Statistical_Fitness")
    mydoc = mycol.find()
    all_doc = list(mycol.find().sort("Timestamp", pymongo.DESCENDING))
    timestamp = []
    for x in all_doc:
        timestamp.append(x["Timestamp"])
        #print(x["Timestamp"])
    return timestamp

def select_doc():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Topology_Manager"]
    mycol = mydb["Tree_Topologies"]
    id = datetime.strptime(topchoosen.get(), '%Y-%m-%d %H:%M:%S.%f')
    read_doc = mycol.find_one({'Timestamp': id})
    global tree_stat_list
    global tree_top_list
    tree_stat_list = read_doc["Statistical_Fitness"]
    tree_top_list = read_doc["Topologies"]
    print("selected_document", tree_stat_list)
    toplist['values'] = tree_stat_list



def select_top():
    global tree_stat_list
    global tree_top_list
    selection = float(toplist.get())
    #print(tree_stat_list)
    #print(tree_top_list)
    selected_top = tree_top_list[tree_stat_list.index(selection)]
    print("Selected topology is", selected_top)
    # reconfig = "0,0d10000,6000d0,12000d0,18000d20000,24000d0,30000d30000,36000d0,42000d0,48000d0,54000d0,60000d"
    ## Scale Topology####
    data = []
    ## Remove "None" elements from topology###
    for wk_pos in selected_top:
        if wk_pos != None:
            data.append(wk_pos)

    scaler = MinMaxScaler(feature_range=(0, 40000)) ## Maximum cordinate range in Visual Components
    print(scaler.fit(data))
    # print(scaler.data_max_)
    #print(scaler.transform(data))
    scaled_top = scaler.transform(data)
    print("Preliminary scaled topology", scaled_top)
    insert = np.array([999999, 999999])
    insert_scaled = np.array([])
    for i in range(len(selected_top)):
        if selected_top[i] == None:
            print("None inserted at position", i+1)
            scaled_top = np.insert(scaled_top, i, insert, axis=0)
    print("Final Scaled Topology", scaled_top)
    reconfig = ""

    for i, wk_pos  in enumerate(scaled_top):
        if scaled_top[i][0] != 999999.0:
            pos_str = str(int(wk_pos[0])) + "," + str(int(wk_pos[1])) + "d"
            reconfig = reconfig + pos_str
        elif scaled_top[i][0] == 999999.0:
            pos_str = "NULL," + "NULLd"
            reconfig = reconfig + pos_str
    print(reconfig)






# Creating tkinter window
window = tk.Tk()
window.title('Swarm Manager')
window.geometry('800x850')

# label text for title
ttk.Label(window, text="Swarm Manager",
          background='green', foreground="white",
          font=("Times New Roman", 15)).grid(row=0, column=1)

# label
ttk.Label(window, text="Select the Document :",
          font=("Times New Roman", 10)).grid(column=0,
                                             row=5, padx=10, pady=25)

ttk.Label(window, text="Select the Topology :",
          font=("Times New Roman", 10)).grid(column=30,
                                             row=20, padx=10, pady=25)


# Combobox creation
n = tk.StringVar()
n2 = tk.StringVar()
topchoosen = ttk.Combobox(window, width=27, textvariable=n)
toplist = ttk.Combobox(window, width=27, textvariable=n2)

# Adding combobox drop down list
topchoosen['values'] = read_tree()

topchoosen.grid(column=1, row=5)
toplist.grid(column=60, row=50)
topchoosen.current()
toplist.current()



reconfig = "0,0d20000,6000d0,15000d0,14000d20000,24000d0,31000d30000,36000d0,42000d0,48000d0,54000d0,60000d"


b1 = tk.Button(window, text='Read Estimated Topologies', command=select_doc).grid(column=30,
                                             row=5, padx=10, pady=25)
b2 = tk.Button(window, text='Retrieve Topology', command=select_top).grid(column=60,
                                             row=5, padx=10, pady=25)
b3 = tk.Button(window, text='Reconfigure Topology', command=lambda: reconfigure_topology(reconfig)).grid(column=90,
                                             row=5, padx=10, pady=25)

window.mainloop()
