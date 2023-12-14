import os
import subprocess
import tkinter as tk
from tkinter import ttk
import numpy as np
import pymongo
from sklearn.preprocessing import MinMaxScaler
from itertools import cycle

tree_stat_list = []
tree_top_list = []
Topology = "NONE"
prod_name = []
prod_volume = []
prod_active = []
prod_sequence = []


def dummy():
    print("Nothing")


def update_label(new_text):
    blinking_label.config(text=new_text)


def blink():
    if next(blink_iter):
        blinking_label.config(fg='red')
    else:
        blinking_label.config(fg='white')
    window.after(500, blink)


def read_tree():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Topology_Manager"]
    mycol = mydb["Spring_Topologies"]

    # mydoc = mycol.distinct("Statistical_Fitness")
    mydoc = mycol.find()
    all_doc = list(mycol.find().sort("Timestamp", pymongo.DESCENDING))
    timestamp = []
    for x in all_doc:
        # _time = x["_id"].generation_time
        _time = x["Timestamp"]
        # stamp = _time.strftime("%Y-%m-%d-%H-%M-%S")
        timestamp.append(_time)
        # print(x["Timestamp"])
    return timestamp


def select_doc():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Topology_Manager"]
    mycol = mydb["Spring_Topologies"]
    # id = datetime.strptime(topchoosen.get(), '%Y-%m-%d %H:%M:%S.%f')
    # id = datetime.strptime(topchoosen.get(), "%Y-%m-%d-%H-%M-%S")
    id = topchoosen.get()
    print(id)
    read_doc = mycol.find_one({'Timestamp': id})
    print(read_doc)
    global tree_stat_list
    global tree_top_list
    global prod_volume
    global prod_active
    global prod_sequence
    global prod_name
    tree_stat_list = read_doc["Statistical_Fitness"]
    tree_top_list = read_doc["Estimated_Topologies"]
    print("selected_document", tree_stat_list)
    toplist['values'] = tree_stat_list
    prod_name = read_doc["Product_name"]
    prod_volume = read_doc["Product_volume"]
    prod_active = read_doc["Product_active"]
    prod_sequence = read_doc["Process_Sequence"]


def topology_visualcomponents(selected_top):
    ## Scale Topology####

    data = []
    ## Remove "None" elements from topology###
    for wk_pos in selected_top:
        if wk_pos != None:
            data.append(wk_pos)

    scaler = MinMaxScaler(feature_range=(0, 40000))  ## Maximum cordinate range in Visual Components
    print(scaler.fit(data))
    # print(scaler.data_max_)
    # print(scaler.transform(data))
    scaled_top = scaler.transform(data)
    print("Preliminary scaled topology", scaled_top)
    insert = np.array([999999, 999999])
    insert_scaled = np.array([])
    for i in range(len(selected_top)):
        if selected_top[i] == None:
            print("None inserted at position", i + 1)
            scaled_top = np.insert(scaled_top, i, insert, axis=0)
    print("Final Scaled Topology", scaled_top)
    reconfig = ""

    for i, wk_pos in enumerate(scaled_top):
        if scaled_top[i][0] != 999999.0:
            pos_str = str(int(wk_pos[0])) + "," + str(int(wk_pos[1])) + "d"
            reconfig = reconfig + pos_str
        elif scaled_top[i][0] == 999999.0:
            pos_str = "NULL," + "NULLd"
            reconfig = reconfig + pos_str
    print(reconfig)
    # Topology = reconfig
    return reconfig


def select_top():
    global tree_stat_list
    global tree_top_list
    global Topology
    selection = float(toplist.get())
    # print(tree_stat_list)
    # print(tree_top_list)
    selected_top = tree_top_list[tree_stat_list.index(selection)]
    print("Selected topology is", selected_top)
    # reconfig = "0,0d10000,6000d0,12000d0,18000d20000,24000d0,30000d30000,36000d0,42000d0,48000d0,54000d0,60000d"
    Topology = topology_visualcomponents(selected_top)
    ## Scale Topology####
    # data = []
    # ## Remove "None" elements from topology###
    # for wk_pos in selected_top:
    #     if wk_pos != None:
    #         data.append(wk_pos)
    #
    # scaler = MinMaxScaler(feature_range=(0, 40000)) ## Maximum cordinate range in Visual Components
    # print(scaler.fit(data))
    # # print(scaler.data_max_)
    # #print(scaler.transform(data))
    # scaled_top = scaler.transform(data)
    # print("Preliminary scaled topology", scaled_top)
    # insert = np.array([999999, 999999])
    # insert_scaled = np.array([])
    # for i in range(len(selected_top)):
    #     if selected_top[i] == None:
    #         print("None inserted at position", i+1)
    #         scaled_top = np.insert(scaled_top, i, insert, axis=0)
    # print("Final Scaled Topology", scaled_top)
    # reconfig = ""
    #
    # for i, wk_pos  in enumerate(scaled_top):
    #     if scaled_top[i][0] != 999999.0:
    #         pos_str = str(int(wk_pos[0])) + "," + str(int(wk_pos[1])) + "d"
    #         reconfig = reconfig + pos_str
    #     elif scaled_top[i][0] == 999999.0:
    #         pos_str = "NULL," + "NULLd"
    #         reconfig = reconfig + pos_str
    # print(reconfig)
    # Topology = reconfig


def save(Topology):
    global prod_name
    global prod_volume
    global prod_active
    global prod_sequence
    "Connect to MongoDB"
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["Topology_Manager"]
    collection = db["Reconfigure_Topology"]

    coll_dict = {"Name": "Reconfiguration",
                 "Type": "Manual",
                 "Topology": Topology,
                 "Product_name": prod_name,
                 "Production_volume": prod_volume,
                 "Production_Active": prod_active,
                 "Production_Sequence": prod_sequence}
    # coll_dict = {"Topologies": topologies}

    total_doc = collection.count_documents({})
    if total_doc == 0:
        collection.insert_one(coll_dict)
    else:
        collection.replace_one({"Name": "Reconfiguration"}, coll_dict)

    update_label("Specific Topology Transferred")


def optimize():
    global Topology
    "Read optimal topology to MongoDB"
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["Topology_Manager"]
    collection = db["Optimal_Topology"]
    optimal_doc = collection.find_one({'Name': "Optimal_Spring"})
    optimal_top = optimal_doc["Topology"]
    Topology = topology_visualcomponents(optimal_top)
    print("Optimal topology string generated", Topology)

    "Read write topology to MongoDB"
    client2 = pymongo.MongoClient("mongodb://localhost:27017")
    db2 = client2["Topology_Manager"]
    collection2 = db2["Reconfigure_Topology"]
    coll_dict2 = {"Name": "Reconfiguration",
                  "Type": "Optimal",
                  "Topology": Topology,
                  "Product_name": prod_name,
                  "Production_volume": prod_volume,
                  "Production_Active": prod_active,
                  "Production_Sequence": prod_sequence}
    total_doc = collection.count_documents({})
    if total_doc == 0:
        collection2.insert_one(coll_dict2)
    else:
        collection2.replace_one({"Name": "Reconfiguration"}, coll_dict2)
    update_label("Optimum Topology Transferred")


if __name__ == "__main__":
    # Creating tkinter window
    window = tk.Tk()
    window.title('Swarm Manager')
    window.geometry('1200x600')
    cmd_str = ""

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
                                                 row=5, padx=10, pady=25)
    ttk.Label(window, text="Or",
              font=("Arial", 25)).grid(column=40,
                                       row=20, padx=10, pady=25)

    blinking_label = tk.Label(window, text="Select a Topology", font=('Helvetica', 16))
    blinking_label.grid(column=60, row=20, padx=10, pady=25)

    # Combobox creation
    n = tk.StringVar()
    n2 = tk.StringVar()
    topchoosen = ttk.Combobox(window, width=27, textvariable=n)
    toplist = ttk.Combobox(window, width=27, textvariable=n2)

    # Adding combobox drop down list
    topchoosen['values'] = read_tree()

    topchoosen.grid(column=1, row=5)
    toplist.grid(column=40, row=5)
    topchoosen.current()
    toplist.current()

    # reconfig = "0,0d20000,6000d0,15000d0,14000d20000,24000d0,31000d30000,36000d0,42000d0,48000d0,54000d0,60000d"

    b1 = tk.Button(window, text='Load Selected MongoDB Document', command=select_doc)
    b1.grid(column=1,row=10, padx=10, pady=25)

    b2 = tk.Button(window, text='Load Specific Topology', command=select_top)
    b2.grid(column=40, row=10, padx=10, pady=25)
    # b3 = tk.Button(window, text='Reconfigure Topology', command=lambda: reconfigure_topology()).grid(column=90,
    #                                              row=5, padx=10, pady=25)
    b3 = tk.Button(window, text='Transfer Topology to VisualComponents', command=lambda: save(Topology))
    b3.grid(column=60, row=5, padx=10, pady=25)
    b3.config()

    b4 = tk.Button(window, text='Transfer optimum topology for VisualComponents', command=lambda: optimize())
    b4.grid(column=40, row=30, padx=10, pady=25)

    # b5 = tk.Button(window, text='Run Visual Components Simulation', command=lambda:dummy()).grid(column=1,
    #                                                                      row=20, padx=10, pady=25)
    # b6 = tk.Button(window, text='Run OPCUA Server', command=main).grid(column=25,
    #                                                                  row=15, padx=10, pady=25)

    blink_iter = cycle([True, False])
    blink()
    window.mainloop()
