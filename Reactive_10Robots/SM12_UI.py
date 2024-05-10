import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pymongo
#from sklearn.preprocessing import MinMaxScaler
from itertools import cycle
from Reactive_10Robots.SM14_Topology_Scaling import scale_graph_uniformly

tree_stat_list = []
tree_top_list = []
Topology = []
Topology_str = "NONE"
prod_name = []
prod_volume = []
prod_active = []
prod_sequence = []
process_times = []
selection = ""
choosen_doc = {}
wk_type = []
wk_capabilities = [[]]





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


def vc_sequence(batch_sequence):
    new_batch = []
    for i, prod_sequence in enumerate(batch_sequence):
        prod_sequence.insert(0, 11 + i)
        prod_sequence.append(50)
        new_batch.append(prod_sequence)
    return new_batch


def read_mongoDB_docs(top_type):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Topology_Manager"]
    mycol = mydb[top_type]

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


def select_doc(top_type):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Topology_Manager"]
    mycol = mydb[top_type]
    print("Column read by select_doc", mycol)
    # id = datetime.strptime(topchoosen.get(), '%Y-%m-%d %H:%M:%S.%f')
    # id = datetime.strptime(topchoosen.get(), "%Y-%m-%d-%H-%M-%S")
    id = topchoosen.get()
    print(id)
    read_doc = mycol.find_one({'Timestamp': id})
    print(read_doc)
    global choosen_doc
    global tree_stat_list
    global tree_top_list
    global prod_volume
    global prod_active
    global prod_sequence
    global prod_name
    global process_times
    global wk_type
    global wk_capabilities
    tree_stat_list = read_doc["Statistical_Fitness"]
    tree_top_list = read_doc["Estimated_Topologies"]
    print("selected_document", tree_stat_list)
    toplist['values'] = tree_stat_list
    prod_name = read_doc["Product_name"]
    prod_volume = read_doc["Product_volume"]
    prod_active = read_doc["Product_active"]
    prod_sequence = read_doc["Process_Sequence"]
    process_times = read_doc["Process_times"]
    wk_type = read_doc["WK_type"]
    wk_capabilities = read_doc["WK_capabilities"]
    choosen_doc = read_doc
    print(choosen_doc["Timestamp"])


def topology_visualcomponents(selected_top):
    ## Scale Topology####

    original_coordinates = []
    ## Remove "None" elements from topology###
    for wk_pos in selected_top:
        if wk_pos != None:
            original_coordinates.append(wk_pos)
    print(original_coordinates)

    # scaler = MinMaxScaler(feature_range=(20000, 60000))  ## Maximum cordinate range in Visual Components
    # print(scaler.fit(original_coordinates))
    # # print(scaler.data_max_)
    # # print(scaler.transform(data))
    # scaled_top = scaler.transform(original_coordinates)
    # print("Preliminary scaled topology", scaled_top)
    # insert = np.array([999999, 999999])
    # insert_scaled = np.array([])
    # for i in range(len(selected_top)):
    #     if selected_top[i] == None:
    #         print("None inserted at position", i + 1)
    #         scaled_top = np.insert(scaled_top, i, insert, axis=0)

    # Create a sample set of coordinates
    coordinates = np.array(original_coordinates)

    # Desired x and y axis limits
    desired_x_min, desired_x_max = -16000, 14000
    desired_y_min, desired_y_max = 16000, 40000

    # Scale the coordinates
    Topology, scaled_coordinates = scale_graph_uniformly(coordinates, desired_x_min, desired_x_max, desired_y_min, desired_y_max)

    # Plot the original and scaled graphs
    plt.plot(coordinates[:, 0], coordinates[:, 1], 'o', label='Original Coordinates')
    plt.plot(scaled_coordinates[:, 0], scaled_coordinates[:, 1], 'o', label='Scaled Coordinates')
    plt.title('Original and Scaled Coordinates')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    plt.xlim(desired_x_min, desired_x_max)
    plt.ylim(desired_y_min, desired_y_max)
    plt.show()


    print("Final Scaled Topology", scaled_coordinates)
    print("Final Topology", Topology)
    reconfig = ""

    for i, wk_pos in enumerate(scaled_coordinates):
        if scaled_coordinates[i][0] != 999999.0:
            pos_str = str(int(wk_pos[0])) + "," + str(int(wk_pos[1])) + "d"
            reconfig = reconfig + pos_str
        elif scaled_coordinates[i][0] == 999999.0:
            pos_str = "NULL," + "NULLd"
            reconfig = reconfig + pos_str
    print(reconfig)
    # Topology = reconfig
    return Topology, reconfig


def select_top():
    global tree_stat_list
    global tree_top_list
    global Topology
    global Topology_str
    sel_top = float(toplist.get())
    # print(tree_stat_list)
    # print(tree_top_list)
    selected_top = tree_top_list[tree_stat_list.index(sel_top)]
    print("Selected topology is", selected_top)
    # reconfig = "0,0d10000,6000d0,12000d0,18000d20000,24000d0,30000d30000,36000d0,42000d0,48000d0,54000d0,60000d"
    Topology, Topology_str = topology_visualcomponents(selected_top)


def select_specific(Topology, Topology_str, top_type):
    global prod_name
    global prod_volume
    global prod_active
    global prod_sequence
    global process_times
    global wk_type
    global wk_capabilities
    select_top = topology_visualcomponents(choosen_doc["Optimized_Topology"])
    "Connect to MongoDB"
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["Topology_Manager"]
    collection = db["Reconfigure_Topology"]

    coll_dict = {"Name": "Reconfiguration",
                 "Type": f"Manual_{top_type}",
                 "Topology": Topology,
                 "Topology_str": Topology_str,
                 "Product_name": prod_name,
                 "Production_volume": prod_volume,
                 "Product_active": prod_active,
                 "Production_Sequence": vc_sequence(prod_sequence),
                 "Process_times": process_times,
                 "WK_type": wk_type,
                 "WK_capabilities": wk_capabilities}
    # coll_dict = {"Topologies": topologies}

    total_doc = collection.count_documents({})
    if total_doc == 0:
        collection.insert_one(coll_dict)
    else:
        collection.replace_one({"Name": "Reconfiguration"}, coll_dict)
    if top_type == "Spring_Topologies":
        update_label(f"Selected Spring Topology Transferred")
    else:
        update_label(f"Selected Tree Topology Transferred")


def select_optimal(top_type):
    global choosen_doc
    optimal_top = topology_visualcomponents(choosen_doc["Optimized_Topology"])
    print("Optimal topology string generated", optimal_top)
    "Read write topology to MongoDB"
    client2 = pymongo.MongoClient("mongodb://localhost:27017")
    db2 = client2["Topology_Manager"]
    collection2 = db2["Reconfigure_Topology"]
    coll_dict2 = {"Name": "Reconfiguration",
                  "Type": f"Optimal_{top_type}",
                  "Topology": optimal_top[0],
                  "Topology_str": optimal_top[1],
                  "Product_name": choosen_doc["Product_name"],
                  "Production_volume": choosen_doc["Product_volume"],
                  "Product_active": choosen_doc["Product_active"],
                  "Production_Sequence": vc_sequence(choosen_doc["Process_Sequence"]),
                  "Process_times": choosen_doc["Process_times"],
                  "WK_type": choosen_doc["WK_type"],
                  "WK_capabilities": choosen_doc["WK_capabilities"]}

    total_doc = collection2.count_documents({})
    if total_doc == 0:
        collection2.insert_one(coll_dict2)
    else:
        collection2.replace_one({"Name": "Reconfiguration"}, coll_dict2)
    if top_type == "Spring_Topologies":
        update_label(f"Optimized Spring Topology Transferred")
    else:
        update_label(f"Optimized Tree Topology Transferred")


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


def selection_changed(event):
    global selection
    global topchoosen
    global toplist
    selection = combo.get()
    messagebox.showinfo(
        title="New Selection",
        message=f"Selected option: {selection}"
    )
    topchoosen['values'] = read_mongoDB_docs(top_type=selection)
    topchoosen.current()
    topchoosen.set('')
    toplist.current()
    toplist.set('')
    update_label(f"Select a Topology")


if __name__ == "__main__":
    # Creating tkinter window
    window = tk.Tk()
    window.title('Swarm Manager')
    window.geometry('1400x500')
    cmd_str = ""

    # label text for title
    ttk.Label(window, text="Swarm Manager Database Interface",
              background='green', foreground="white",
              font=("Times New Roman", 15)).grid(row=0, column=1)

    ttk.Label(window, text="Select Topology Type :",
              font=("Times New Roman", 10)).grid(column=0,
                                                 row=5, padx=10, pady=25)

    # label
    ttk.Label(window, text="Select the Document :",
              font=("Times New Roman", 10)).grid(column=0,
                                                 row=20, padx=10, pady=25)

    ttk.Label(window, text="Select the Topology :",
              font=("Times New Roman", 10)).grid(column=30,
                                                 row=5, padx=10, pady=25)
    ttk.Label(window, text="Or",
              font=("Arial", 25)).grid(column=40,
                                       row=20, padx=10, pady=25)

    blinking_label = tk.Label(window, text="Select a Topology", font=('Helvetica', 16))
    blinking_label.grid(column=30, row=60, padx=10, pady=25)

    # Combobox creation
    n = tk.StringVar()
    n2 = tk.StringVar()
    topchoosen = ttk.Combobox(window, width=27, textvariable=n)
    topchoosen.grid(column=1, row=20)
    toplist = ttk.Combobox(window, width=27, textvariable=n2)
    toplist.grid(column=40, row=5)

    # Adding combobox drop down list
    # topchoosen['values'] = read_mongoDB_docs(top_type=selection)
    # topchoosen.current()
    # toplist.current()

    # reconfig = "0,0d20000,6000d0,15000d0,14000d20000,24000d0,31000d30000,36000d0,42000d0,48000d0,54000d0,60000d"

    combo = ttk.Combobox(values=["Spring_Topologies", "Tree_Topologies", "Ring_Topologies"])
    combo.bind("<<ComboboxSelected>>", selection_changed)
    combo.grid(column=1, row=5, padx=10, pady=25)

    b1 = tk.Button(window, text='Load Selected MongoDB Document', command=lambda: select_doc(top_type=selection))
    b1.grid(column=1, row=30, padx=10, pady=25)

    b2 = tk.Button(window, text='Load Specific Topology', command=select_top)
    b2.grid(column=40, row=10, padx=10, pady=25)
    # b3 = tk.Button(window, text='Reconfigure Topology', command=lambda: reconfigure_topology()).grid(column=90,
    #                                              row=5, padx=10, pady=25)
    b3 = tk.Button(window, text='Transfer Topology to VisualComponents',
                   command=lambda: select_specific(Topology=Topology, top_type=selection, Topology_str=Topology_str))
    b3.grid(column=60, row=5, padx=10, pady=25)
    b3.config()

    b4 = tk.Button(window, text='Transfer optimized topology for VisualComponents',
                   command=lambda: select_optimal(top_type=selection))
    b4.grid(column=40, row=30, padx=10, pady=25)

    # b5 = tk.Button(window, text='Run Visual Components Simulation', command=lambda:dummy()).grid(column=1,
    #                                                                      row=20, padx=10, pady=25)
    # b6 = tk.Button(window, text='Run OPCUA Server', command=main).grid(column=25,
    #                                                                  row=15, padx=10, pady=25)

    blink_iter = cycle([True, False])
    blink()
    window.mainloop()
