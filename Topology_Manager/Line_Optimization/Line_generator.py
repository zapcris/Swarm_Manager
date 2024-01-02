import math

import networkx as nx
import pymongo
from collections import Counter

from matplotlib import pyplot as plt


def unique_values_in_list_of_lists(lst):
    result = set(x for l in lst for x in l)
    return list(result)


def euclidean_dist(x1, y1, x2, y2):
    dist = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0)
    return round(dist)


def read_db():
    global Batch_sequence
    global G_pos
    global Qty_order
    global prod_name
    global prod_volume
    global prod_active
    global process_times
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Topology_Manager"]
    mycol = mydb["Spring_Topologies"]
    # read_doc = mycol.find_one({"Name": "Optimal_Spring"})
    cursor = mycol.find().sort("_id", -1).limit(1)
    read_doc = cursor[0]
    prod_name = read_doc["Product_name"]
    prod_volume = read_doc["Product_volume"]
    prod_active = read_doc["Product_active"]
    process_times = read_doc["Process_times"]
    Batch_sequence = read_doc["Process_Sequence"]
    Qty_order = read_doc["Product_volume"]
    spring_pos = read_doc["Optimized_Topology"]
    for index, value in enumerate(spring_pos):
        print(index, value)
        if value != None:
            G_pos.update({index + 1: (value[0], value[1])})


if __name__ == "__main__":
    G_pos = {}
    Batch_sequence = {}
    Qty_order = []
    prod_name = []
    prod_volume = []
    prod_active = []
    process_times = [[]]

    read_db()
    print(Batch_sequence)
    print(Qty_order)
    print(G_pos)

    PI_weight = []
    for i in range(len(Qty_order)):
        PI_weight.append(Qty_order[i] * len(Batch_sequence[i]))

    print("weighted list for Product Instances:", PI_weight)

    ## Start of the Spanning Tree solution to the problem#####
    node_list = unique_values_in_list_of_lists(Batch_sequence)
    print("Total nodes in batch:", node_list)
    edge_list = []
    raw_elist = []

    ### Generate a graph from the Genetic STage 1 Force directed output####
    G = nx.MultiGraph()
    G.add_nodes_from(node_list)
    G.add_edges_from(raw_elist)
    width_dict = Counter(G.edges())

    ### reliable edge list with distance and flow in dictionary####
    edge_dict = [(u, v, {'weight': euclidean_dist(G_pos[u][0], G_pos[u][1], G_pos[v][0], G_pos[v][1]), 'Flow': value})
                 for ((u, v), value) in width_dict.items()]
    G.remove_edges_from(raw_elist)
    G.add_edges_from(edge_dict)

    ##### Genetic algorithm for Optimizing the Spanning tree problem######
    print("Start of the Recurssion")
    ### Create population here####
    random_pop = []
    grid_size = 28
    pos = nx.spiral_layout(G)
    plt.figure()
    plt.title(f"The plot belongs to initial population")
    nx.draw(G, pos, with_labels=True)
    # plt.grid(True)
    plt.grid(which='major', axis='both', linestyle='-')
    # plt.pause(0.05)
    plt.show()
