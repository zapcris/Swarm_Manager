## Spanning tree for most weighted product Instance in the batch###
import math
from collections import Counter

import networkx as nx


def unique_values_in_list_of_lists(lst):
    result = set(x for l in lst for x in l)
    return list(result)


def euclidean_dist(x1, y1, x2, y2):
    dist = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0)
    return round(dist)


def set_edge_weight(graph, pos):
    for e in graph.edges():
        dist = 0.0
        first_node_x = pos[e[0]][0]
        second_node_x = pos[e[1]][0]
        first_node_y = pos[e[0]][1]
        second_node_y = pos[e[1]][1]
        dist += round(
            math.sqrt(math.pow(second_node_x - first_node_x, 2) + math.pow(first_node_y - second_node_y, 2) * 1.0))
        graph[e[0]][e[1]][0]['weight'] = dist


def convert_logical_spatial(graph, pos):
    count_edges = Counter(graph.edges())
    ### reliable edge list with distance and flow in dictionary####
    edge_dict = [(u, v, {'weight': euclidean_dist(pos[u][0], pos[u][1], pos[v][0], pos[v][1]), 'Flow': value})
                 for ((u, v), value) in count_edges.items()]
    graph.remove_edges_from(graph.edges())
    graph.add_edges_from(edge_dict)
    return graph

def create_weightedPI_tree(G, pos, PI_sequence):
    edge_list = []
    remain_node = []
    span_edges = []
    reduced_span = []
    filtered_edges = []
    full_elist = list(G.edges())
    full_nlist = G.nodes()
    for i in range(len(PI_sequence) - 1):
        e = [PI_sequence[i], PI_sequence[i + 1]]
        edge_list.append(e)
    #print("Input product sequence:", PI_sequence)
    # print("Complete topology:", full_elist)
    # print("Complete topology:", full_elist[1][0], full_elist[1][1])
    ### enlist nodes to be added to complete the spanning tree####
    for node in full_nlist:
        if not node in PI_sequence:
            remain_node.append(node)
    # print("Remaining node:", remain_node)
    # print(full_elist)
    ### enlist pair of edges from global edge list for remaining nodes
    for node in remain_node:
        for i in range(len(full_elist)):
            for j in range(len(full_elist[i])):
                if full_elist[i][j] == node:
                    # print(node, full_elist[i])
                    n = node, full_elist[i], G[full_elist[i][0]][full_elist[i][1]][0]['weight']
                    span_edges.append(n)

    # print("FIrst step of spanned edges", span_edges)

    ### remove edges from prospective list which has both the nodes not present in the current graph
    for e in span_edges:
        # print(e[0], e[1][0], e[1][1], e[2])
        # if not (e[1][0] in remain_node and e[1][1] in remain_node):
        reduced_span.append(e)
    #     elif e[1][0] in remain_node and e[1][1] in remain_node:
    #         filtered_edges.append(e)
    #
    # print("Filtered edges:", filtered_edges)
    # print("second step reduction span edges:", reduced_span)

    ### pick edge pair from the reduced prospective list with minimum path to the current graph
    visited = []
    weight = []
    edge = []
    for e in reduced_span:
        a = []
        if e[0] in visited and e[1] == min(weight):
            weight.clear()
            edge.clear()
            weight.append(e[2])
            a = [e[1][0], e[1][1]]
            edge.append(a)
        if not e[0] in visited:
            visited.append(e[0])
            weight.append(e[2])
            a = [e[1][0], e[1][1]]
            edge.append(a)

    # print(weight)
    # print(edge)

    edge_list.extend(edge)

    # print("Spanning tree edge list:", edge_list)

    S = nx.MultiGraph()
    S.add_nodes_from(PI_sequence)
    S.add_edges_from(edge_list)
    width_dict = Counter(S.edges())
    ### reliable edge list with distance and flow in dictionary####
    edge_dict = [(u, v, {'weight': euclidean_dist(pos[u][0], pos[u][1], pos[v][0], pos[v][1]), 'Flow': value})
                 for ((u, v), value) in width_dict.items()]
    S.remove_edges_from(edge_list)
    S.add_edges_from(edge_dict)
    #print(S.edges())

    #print("The graph is a tree?", nx.is_tree(S))

    return S
