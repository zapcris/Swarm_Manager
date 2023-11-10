import math
from collections import Counter
import random
import networkx as nx
from matplotlib import pyplot as plt
from networkx.algorithms import approximation, hierarchy, efficiency_measures, tree
from sklearn.preprocessing import MinMaxScaler

from variant_topology import workstation, config, topology


def unique_values_in_list_of_lists(lst):
    result = set(x for l in lst for x in l)
    return list(result)


def create_batch_topology(graph, num, k_val, iter):
    #k = 0
    print("The graph", graph)
    print("The batch topology number:", num)
    node_list = unique_values_in_list_of_lists(graph)
    print("node list", node_list)
    # print("no of node:", len(node_list))
    edge_list = []
    tw = 0
    for i in range(len(graph)):
        for j in range(len(graph[i]) - 1):
            # print(graph[i][j], graph[i][j+1])
            edge = [graph[i][j], graph[i][j + 1]]
            edge_list.append(edge)

    #print(edge_list)


    G = nx.MultiGraph()
    G.add_nodes_from(node_list)
    G.add_edges_from(edge_list)
    width_dict = Counter(G.edges())
    ### Calculate the frequency of connections between edges in the graph
    edge_width = [[u, v, {'frequency': value}]
                  for ((u, v), value) in width_dict.items()]
    #print(edge_width)




    H = nx.Graph()
    H.add_nodes_from(node_list)
    H.add_edges_from(edge_list)

    L = nx.MultiDiGraph()
    L.add_nodes_from(node_list)
    L.add_edges_from(edge_list)

    #cs = hierarchy.flow_hierarchy(L)
    eff = efficiency_measures.global_efficiency(G)


    #print("Flow hierarchy value:", eff)

    #print(approximation.treewidth_min_degree(H))
    #print(approximation.treewidth_min_fill_in(H))

    initialpos = {1: [0, 0], 20: [2, 2]}
    pos = nx.spring_layout(G, weight='myweight', pos=initialpos, k=k_val, dim=2, scale=1, seed=15, iterations=iter)
    nx.draw_networkx(G, pos)
    pos2 = nx.rescale_layout_dict(pos, 2)

    # for key, value in pos.items():
    #     print(value)

    min_x, min_y = 0, 0
    for key, value in pos.items():
        if value[0] < min_x:
            min_x = value[0]
        if value[1] < min_y:
            min_y = value[1]

    #print(f"min x {min_x} min y {min_y}")
    #print("position old data structure:", pos)
    scale = 20

    #new_pos = []
    r_pos = []
    data = [[0, 0] for i in range(max(node_list) + 1)]

    ##old scaling ####
    # for key, value in pos.items():
    #     print("The non-scaled topological positions:", key, value)
    #     new_pos.append((key, (scale * (value[0] + abs(min_x)), scale * (value[1] + abs(min_y)))))
    #
    #
    # print("The new position datastrcuture", new_pos)


    for i in range(len(data)):
        for key, value in pos.items():
            # print(key, value)
            if i == key:
                # print(i)
                data[i] = list(dict.fromkeys(value))

    #print(f"The new test topology of length {len(data)}", data)
    scaler = MinMaxScaler(feature_range=(2, 22))  ## Maximum cordinate range in Visual Components
    scaler.fit(data)
    scaled_top = scaler.transform(data)
    print("The new scaled topology", scaled_top)
    # pos = dict(new_pos)
    # print(dict(new_pos))
    #print(pos)

    ###insert new scaling into pos dict to generate graph###

    new_pos = {}
    for index, value in enumerate(scaled_top):
        if index in node_list:
            new_pos[index] = (round(value[0]), round(value[1]))

    print("New dictionoary for drawing graph", new_pos)
    #pos = dict(new_pos)
    pos = new_pos
    #print("position data structure:", pos)
    #print("old pos:", pos)
    #print("new pos:", pos2)

    for key, value in pos.items():
        r_pos.append((key,(round(value[0]), round(value[1]))))

    return_pos = dict(r_pos)



    val = []
    for key, value in pos.items():
        val.append(list(dict.fromkeys(value)))

    separated_num = math.modf(k_val)
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.title('Swarm topology')
    plt.grid(True)
    #plt.savefig(f'kval{round(separated_num[1])}_{round(separated_num[0] * 100)}_iter{iter}_batch_topology')

    pos_list = [[0, 0] for i in range(max(node_list) + 1)]
    #print("The zeroed position list", pos_list)

    config_list = []

    product_topologies = []
    all_workstations = []
    batch_topologies = []
    new_list = []
    total_cost = []
    fitness_value = []

    ## Deprecated pos_list -- old logic
    # for i in range(len(pos_list)):
    #     for key, value in pos.items():
    #         #print(key, value)
    #         if i == key:
    #             #print(i)
    #             pos_list[i] = list(dict.fromkeys(value))

    #print("The position list", pos_list)

    for i in range(len(graph)):
        ws = []
        for j in range(len(graph[i])):
            ws.append(workstation(num=graph[i][j], active=True))
        all_workstations.append(ws)

    sorted_configs = []
    for graph_taken in graph:
        # [1 5 4 2 3]
        this_graph_config = []
        for node in graph_taken:
            #print(f"Node {node}")
            #print(f"Value= {round(pos_list[node][0]),round(pos_list[node][1])}")
            print(f" TEST Pos Nodes: {node} and {scaled_top[node][0]} and {scaled_top[node][1]}")

            this_graph_config.append(config(round(scaled_top[node][0]), round(scaled_top[node][1])))
        sorted_configs.append(this_graph_config)

    for num in range(len(all_workstations)):
        product_topologies.append(topology(all_workstations[num], sorted_configs[num], num + 1))

    for top in product_topologies:
        #top.display()
        total_cost.append(top.calculate_distance())
        fitness_value.append(top.fitness_calc())

    return sum(fitness_value), pos, fitness_value
