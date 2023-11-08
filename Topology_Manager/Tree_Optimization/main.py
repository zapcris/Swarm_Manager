import pymongo
import json
import random
import sys
import time
from random import randint
import matplotlib.pyplot as plt
from networkx.algorithms import SpanningTreeIterator
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
from Draw_heirachial_graph import draw_hierarchy_pos, hierarchy_pos2, hierarchy_pos3
from Fitness_Function import fitness_function
from Func_weighted_spanning_tree import *
from check_topology import checkBusTopology, addEdge, checkRingTopology
from grid_map import *
import EoN
from production_performance import prod_efficiency



def rand_index(gen):
    r1 = (random.randint(2, 6))
    r2 = (random.randint(6, 10))
    r3 = (random.randint(11, 15))
    index = [r1, r2, r3]
    print(index)

    if gen >= 10:
        print("stopped")
    else:
        rand_index(gen + 1)


G_pos = {1: (9, 4), 2: (18, 13), 3: (22, 8), 4: (18, 10), 5: (13, 0), 6: (15, 4), 7: (24, 22), 8: (12, 6), 9: (10, 11), 10: (14, 16), 11: (26, 15), 12: (30, 4), 13: (17, 17), 14: (0, 2), 15: (19, 24), 16: (22, 12), 17: (26, 20), 19: (23, 33), 20: (27, 28)}




Batch_sequence = [[1, 5, 9, 10, 2, 11, 13, 15, 7, 20],
                  [1, 2, 7, 3, 5, 6, 8, 9, 13, 15, 19, 20],
                  [1, 5, 8, 6, 3, 2, 4, 10, 15, 17, 20],
                  [1, 8, 9, 10, 2, 11, 13, 15, 7, 20],
                  [1, 4, 17, 3, 8, 9, 13, 15, 19, 20],
                  [1, 6, 8, 6, 3, 12, 4, 10, 15, 17, 20],
                  [1, 14, 8, 6, 13, 2, 4, 10, 15, 17, 20]]

def max_value(input_list):
    return max([sublist[-1] for sublist in input_list])

Qty_order = [10, 30, 50, 20, 60, 20, 40]
#Qty_order = [100,100,100,100,100,100,100]
#Qty_order = [1, 1, 1, 1, 1, 1, 1]

PI_weight = []
for i in range(len(Qty_order)):
    PI_weight.append(Qty_order[i] * len(Batch_sequence[i]))

print("weighted list for Product Instances:", PI_weight)

len_graph = [100, 100 ,100, 100,100, 100, 100]

#print(prod_efficiency(Batch_sequence, G_pos, PI_weight, len_graph))


## Start of the Spanning Tree solution to the problem#####


node_list = unique_values_in_list_of_lists(Batch_sequence)
print("Total nodes in batch:", node_list)
edge_list = []
raw_elist = []

for i in range(len(Batch_sequence)):
    for j in range(len(Batch_sequence[i]) - 1):
        # print(graph[i][j], graph[i][j+1])
        edge = [Batch_sequence[i][j], Batch_sequence[i][j + 1]]
        raw_elist.append(edge)
        if not edge in edge_list:
            edge_list.append(edge)  #### edge list of non repeating edges


#### Check the Bus and Ring topology###
V = max_value(Batch_sequence)
E = V-1
adj1 = [[] for i in range(V+1)]
for edge in edge_list:
    addEdge(adj1, edge[0], edge[1])


checkBusTopology(adj1, V, E)

checkRingTopology(adj1, V, E)


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

print("Start of the Genetic Algorithm")

### Create population here####
random_pop = []
grid_size = 28

# L = nx.MultiGraph()
# L.add_nodes_from(node_list)
# L.add_edges_from(raw_elist)

for i in range(1):
    iter_class1 = iter(SpanningTreeIterator(G, minimum=True, ignore_nan=True))
    random_pop.append(next(iter_class1))

for i in range(1):
    iter_class2 = iter(SpanningTreeIterator(G, minimum=False, ignore_nan=True))
    random_pop.append(next(iter_class2))

# for i in range(1):
#     iter_class3 = iter(SpanningTreeIterator(L, minimum=True, ignore_nan=True))
#     random_pop.append(next(iter_class3))

#     create_weightedPI_tree(G, G_pos, Batch_sequence[PI_weight.index(max(PI_weight))]))
for pseq in Batch_sequence:
    random_pop.append(create_weightedPI_tree(G, G_pos, pseq))
    # print("The new batch sequenc:", pseq)


##Draw hierarchy tree psoitions all population###
tree_pos = []
for i, chr_Tree in enumerate(random_pop):
    # pos= G_pos
    pos = draw_hierarchy_pos(chr_Tree, root=1, width=grid_size, height=grid_size)
    #pos = EoN.hierarchy_pos(chr_Tree, root=1, width=grid_size)
    #pos = hierarchy_pos3(chr_Tree,root=1,width=grid_size,xcenter=14)
    #pos = graphviz_layout(G, prog='dot')
    tree_pos.append(pos)
    plt.figure()
    plt.title(f"The plot belongs to initial population {i + 1} ")
    nx.draw(chr_Tree, pos, with_labels=True)

    #plt.grid(True)
    plt.grid(which='major', axis='both', linestyle='-')
    #plt.pause(0.05)
    plt.show()


##### calculate fitness function for random population
cross_gen_fitness = []
random_fitness = []
perf_fitness= []
print("Taking a pause")
time.sleep(1)  # Pause 1 seconds
print("pause ended")

topology_htable = dict()
for i, (chr_Tree, pos) in enumerate(zip(random_pop, tree_pos)):
    fit_val = fitness_function(chr_Tree, Batch_sequence, PI_weight,pos)
    random_fitness.append(fit_val[0])
    topology_htable.update({fit_val[0]: (fit_val[1], fit_val[2])})


    time.sleep(0.05)
    # print(i, random_fitness[i])

cross_gen_fitness.append(random_fitness)

# print(random_pop[20].edges())
## Choose the fittest spanning tree####

print("TREE Fitness values for population", random_fitness)
print("Euclidean Fitness values for population", random_fitness)
print("Performance fitness of population", perf_fitness)


sorted_fitness = sorted(random_fitness)
pIndex_1 = random_fitness.index(sorted_fitness[0])
pIndex_2 = random_fitness.index(sorted_fitness[1])

parent1 = random_pop[pIndex_1]
parent2 = random_pop[pIndex_2]

##### crossover function#######
### convert the global map G to prufer suitable
prufer_map = {}
for i, j in enumerate(set(G)):
    prufer_map[j] = i

print("Prufer global map:", prufer_map)

### convert back to original map
origin_map = dict([(value, key) for key, value in prufer_map.items()])
print("original map:", origin_map)


def get_prufer_sequence(parent, map):
    # map = {}
    # for i, j in enumerate(set(parent)):
    #     map[j] = i
    # print("map of offsrping1 :", map)
    parent = nx.relabel_nodes(parent, map)
    # print(set(parent))
    # print(set(range(len(parent))))
    pruf_seq = nx.to_prufer_sequence(parent)
    return pruf_seq, parent


def prufer_to_tree(pruf_seq, map):
    graph = nx.from_prufer_sequence(pruf_seq)

    graph = nx.relabel_nodes(graph, map)
    print("The graph is a tree?", nx.is_tree(graph))
    return graph


def uniform_crossover(A, B):
    for i in range(len(A)):
        # if P[i] < 0.01:
        temp = A[i]
        A[i] = B[i]
        B[i] = temp
    a1 = A
    b1 = B
    return A, B


def crossover(a, b, index):
    return b[:index] + a[index:], a[:index] + b[index:]


def multi_point_crossver(parent1, parent2, index_arr):
    # create segments first
    child_A = []
    child_B = []
    A_seg = [0] * (len(index_arr) + 1)
    B_seg = [0] * (len(index_arr) + 1)
    tmp_a = []
    tmp_b = []
    for i in range(len(index_arr) + 1):
        if i == 0:
            tmp_a.append(parent1[:index_arr[i]])
            tmp_b.append(parent2[:index_arr[i]])
        elif i != 0 and i != len(index_arr):
            tmp_a.append(parent1[index_arr[i - 1]:index_arr[i]])
            tmp_b.append(parent2[index_arr[i - 1]:index_arr[i]])
        elif i == len(index_arr):
            tmp_a.append(parent1[index_arr[i - 1]:])
            tmp_b.append(parent2[index_arr[i - 1]:])
    # print(tmp_a)
    # print(tmp_b)
    ### exchange odd segments to other parent ######
    for i, (Aseg, Bseg) in enumerate(zip(tmp_a, tmp_b)):

        if (i % 2) == 0:
            A_seg[i] = Aseg
            B_seg[i] = Bseg
        else:
            tmp = Aseg
            A_seg[i] = Bseg
            B_seg[i] = tmp
    # print(A_seg)
    # print(B_seg)
    for a, b in zip(A_seg, B_seg):
        child_A.extend(a)
        child_B.extend(b)
    # print(child_A)
    # print(child_B)

    return child_A, child_B


def breed_crossover(parent1, parent2):
    index = int(np.random.uniform(low=1, high=len(parent1) - 1))  # random point between 1 and 1 is always 1
    return np.hstack([parent1[:index], parent2[index:]])


A = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
B = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12, 13, 14, 15, 16]
index = [2, 6, 12, 14]
multi_point_crossver(A, B, index)

children = []
# print("multipoint corssover test:", breed_crossover(A, B))
children.append(breed_crossover(A, B))
children.append(breed_crossover(B, A))

print("multipoint corssover test:", children)
test = [1, 2, 3, 4, 5, 6, 7, 8, 9, ]
random.shuffle(test)


# print("A shuffled list", test)


def genetic_stage2(parent1, parent2, gen):
    print("Started recurrsion with generation number", gen)
    parent_fitness = []
    offspring_fitness = []
    offspring_fitness = []
    pruf_parent1 = get_prufer_sequence(parent1, prufer_map)
    pruf_parent2 = get_prufer_sequence(parent2, prufer_map)
    # print("parent1 prufer", pruf_parent1[0])
    # print("parent2 prufer", pruf_parent2[0])
    middle_idx1 = round((len(pruf_parent1[0]) - 1) / 2)
    middle_idx2 = round((len(pruf_parent2[0]) - 1) / 2)

    # off_pruf1 = pruf_parent1[0][:middle_idx1] + pruf_parent2[0][middle_idx2:]
    # off_pruf2 = pruf_parent2[0][:middle_idx2] + pruf_parent1[0][middle_idx1:]
    # off_pruf3 = pruf_parent1[0][:middle_idx1] + pruf_parent2[0][:middle_idx2]
    # off_pruf4 = pruf_parent2[0][:middle_idx2] + pruf_parent1[0][:middle_idx1]

    index2 = [randint(1, len(pruf_parent1[0]) - 1), randint(1, len(pruf_parent1[0]) - 1)]

    cut_points = [(random.randint(2, 5)), (random.randint(6, 10)), (random.randint(11, 15))]
    Off = multi_point_crossver(pruf_parent1[0], pruf_parent2[0], cut_points)

    # random.shuffle(Off[0])
    # random.shuffle(Off[1])
    # # Off = crossover(pruf_parent1[0], pruf_parent2[0], index)
    # # Off = multi_point_crossover(pruf_parent1[0], pruf_parent2[0], index2)
    #
    # print("offsprinf prufer sequences:", Off)
    # Off_2 = uniform_crossover(pruf_parent1[0], pruf_parent2[0])

    off1_tree = prufer_to_tree(Off[0], origin_map)
    off2_tree = prufer_to_tree(Off[1], origin_map)

    logical_off = [off1_tree, off2_tree]  # off3_tree, off4_tree]
    offspring_trees = []
    off_pos =[]
    # print("pause started")
    # time.sleep(5)
    # print("resumed")
    ### Draw and calculate fitness function ####
    for i, off_tree in enumerate(logical_off):
        pos_off = draw_hierarchy_pos(off_tree, root=1, width=grid_size, height=grid_size)

        #pos_off = EoN.hierarchy_pos(off_tree, root=1, width=grid_size)
        off_pos.append(pos_off)
        # pos_off = EoN.hierarchy_pos(off_tree, root=1, width=40)
        plt.figure()
        plt.title(f"The plot belongs to offsrping {i + 1} in generation {gen} ")
        nx.draw(off_tree, pos_off, with_labels=True)
        plt.grid(True)
        plt.pause(0.05)
        plt.show()
        offspring_trees.append(convert_logical_spatial(off_tree, pos_off))

    for i, (off_top,pos) in enumerate(zip(offspring_trees,off_pos)):
        fit_off = fitness_function(off_top, Batch_sequence, PI_weight,pos)
        offspring_fitness.append(fit_off[0])
        topology_htable.update({fit_off[0]: (fit_off[1], fit_off[2])})

    cross_gen_fitness.append(offspring_fitness)
    print(f'The fitness list of generation {gen} is {offspring_fitness}')

    #if min(offspring_fitness) <= 2000 or gen >= 3:
    if gen >= 2:
        print("fitness of this generation", offspring_fitness)
        print("Recurssion Ended ")


    else:
        # time.sleep(1)
        gen = gen + 1

        sorted_fitness = sorted(offspring_fitness)
        pIndex_1 = offspring_fitness.index(sorted_fitness[0])
        pIndex_2 = offspring_fitness.index(sorted_fitness[1])
        new_parent1 = offspring_trees[pIndex_1]
        new_parent2 = offspring_trees[pIndex_2]
        genetic_stage2(new_parent1, new_parent2, gen)


genetic_stage2(parent1, parent2, 1)


min_fit = 0
gen_fit = 0
for i, fit in enumerate(cross_gen_fitness):
    print(fit)
    if i == 0:
        min_fit = min(fit)
        gen_fit = 1
    elif min(fit) < min_fit:
        min_fit = min(fit)
        gen_fit = i + 1

if gen_fit <= 1:
    print(
        f" Fittest value found is : {min_fit} in initial population chromosome no: {(random_fitness.index(min_fit)) + 1}")
else:
    print(f" Fittest value found is : {min_fit} in generation {gen_fit}")

"Find the perfromance of the fittest topology"
#perf_fitness.append(prod_efficiency(Batch_sequence, pos, Qty_order, fit_val[1]))
print("Fittest topology is", topology_htable[min_fit][1])
print(prod_efficiency(Batch_sequence, topology_htable[min_fit][1], Qty_order, topology_htable[min_fit][0]))

#print("Topology hash table" ,topology_htable)
top_keys = []
for fit in topology_htable:
    k = fit
    top_keys.append(k)


topologies = []


for fit_val in top_keys:
    #topologies.append(topology_htable[fit_val][1])
    top_dict = topology_htable[fit_val][1]
    top = [None] * max_value(Batch_sequence)
    for key, value in top_dict.items():
        top[key-1] = value
    topologies.append(top)

optimized_top = [None] * max_value(Batch_sequence)
for key, value in topology_htable[min_fit][1].items():
    optimized_top[key-1] = value
#print(topologies)

"Connect to MongoDB"
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Topology_Manager"]
collection = db["Tree_Topologies"]

coll_dict = { "Batch_Sequence": Batch_sequence, "Production_order": Qty_order, "Statistical_Fitness": top_keys,
              "Topologies": topologies, "Optimized_Topology": optimized_top}
#coll_dict = {"Topologies": topologies}

x = collection.insert_one(coll_dict)
sys.exit()




Grid_graph = nx.grid_2d_graph(50,50)

plt.figure(figsize=(100,100))
pos = {(x,y):(y,-x) for x,y in Grid_graph.nodes()}
nx.draw(Grid_graph, pos=pos,
        node_color='lightgreen',
        with_labels=True,
        node_size=600)
plt.savefig(f'charts/throughput/gridmap')

#### GRAPH TO GRID MAPP#####

matrix = np.array(
    [[-2, 5, 3, 2],
     [9, -6, 5, 1],
     [3, 2, 7, 3],
     [-1, 8, -4, 8]])

diags = [matrix[::-1, :].diagonal(i) for i in range(-3, 4)]
diags.extend(matrix.diagonal(i) for i in range(3, -4, -1))

# for n in diags:
#     print(n.tolist())


Grid = np.zeros((35, 35))
# print(Grid)

max_index = PI_weight.index(max(PI_weight))
# print(max_index)

nList_diag = Batch_sequence[max_index]
# print("Diagnoally prefered sequence", nList_diag)

np.fill_diagonal(Grid, 99)

di = np.diag_indices_from(Grid)
# print(di)

# create list to be filled in diagonal of grid matrix

interval = len(Grid.diagonal()) // len(nList_diag)

# print(interval)


diag_seq = [0 for n in Grid.diagonal()]

for i in range(0, len(Grid.diagonal()), 3):
    # print(i)
    diag_seq[i] = 6

# print(diag_seq)

# Initiliaze the grid map
grid_map = GridMap(35, 35, 1, 17.5, 17.5)

# grid_map.plot_grid_map()

# Place diagonals workstations on the grid MAP
for i in range(len(nList_diag)):
    x = i * interval
    y = i * interval
    grid_map.set_value_from_xy_pos(x, y, 1)

    label = f"WK({nList_diag[i]})"
    # plt.annotate(label,  # this is the text
    #              (x, y),  # these are the coordinates to position the label
    #              textcoords="offset points",  # how to position the text
    #              xytext=(0, 0),  # distance from text to points (x,y)
    #              ha='left')  # horizontal alignment can be left, right or cente

