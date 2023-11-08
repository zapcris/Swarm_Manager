# Python3 program to check if the given graph
# represents a bus topology
import networkx as nx
import matplotlib.pyplot as plt

# A utility function to add an edge in an
# undirected graph.
def addEdge(adj, u, v):
	adj[u].append(v)
	adj[v].append(u)

# A utility function to print the adjacency list
# representation of graph
def printGraph(adj, V):

	for v in range(V):
		print("Adjacency list of vertex ",v,"\n head ")
		for x in adj[v]:
			print("-> ",x,end=" ")


# /* Function to return true if the graph represented
# by the adjacency list represents a bus topology
# else return false */
def checkBusTopologyUtil(adj, V, E):

	# Number of edges should be equal
	# to (Number of vertices - 1)
	if (E != (V - 1)):
		return False

	# a single node is termed as a bus topology
	if (V == 1):
		return True

	vertexDegree = [0]*(V + 1)

	# calculate the degree of each vertex
	for i in range(V + 1):
		for v in adj[i]:
			vertexDegree[v] += 1

	# countDegree2 - number of vertices with degree 2
	# countDegree1 - number of vertices with degree 1
	countDegree2,countDegree1 = 0,0
	for i in range(1, V + 1):
		if (vertexDegree[i] == 2):
			countDegree2 += 1

		elif (vertexDegree[i] == 1):
			countDegree1 += 1

		else:
			# if any node has degree other
			# than 1 or 2, it is
			# NOT a bus topology
			return False

	# if both necessary conditions as discussed,
	# satisfy return true
	if (countDegree1 == 2 and countDegree2 == (V - 2)):
		return True

	return False

# Function to check if the graph represents a bus topology
def checkBusTopology(adj, V, E):

	isBus = checkBusTopologyUtil(adj, V, E)
	if (isBus):
		print("The topology is a Bus")

	else:
		print("The topology is not a Bus" )


# Python3 program to check if the given graph
# represents a star topology

# A utility function to add an edge in an
# undirected graph.




# /* Function to return true if the graph represented
# by the adjacency list represents a ring topology
# else return false */
def checkRingTopologyUtil(adj, V, E):
	# Number of edges should be equal
	# to (Number of vertices - 1)
	if (E != (V)):
		return False

	# For a graph to represent a ring topology should have
	# greater than 2 nodes
	if (V <= 2):
		return False

	vertexDegree = [0] * (V + 1)

	# calculate the degree of each vertex
	for i in range(V + 1):
		for v in adj[i]:
			vertexDegree[v] += 1

	# countDegree2 stores the count of
	# the vertices having degree 2
	countDegree2 = 0

	for i in range(1, V + 1):
		if (vertexDegree[i] == 2):
			countDegree2 += 1

	# if all three necessary conditions as discussed,
	# satisfy return true
	if (countDegree2 == V):
		return True
	else:
		return False


# Function to check if the graph represents a ring topology
def checkRingTopology(adj, V, E):
	isRing = checkRingTopologyUtil(adj, V, E)
	if (isRing):
		print("The Topology is a Ring")

	else:
		print("The Topology is not a Ring")


# Driver code

# Graph 1
V, E = 6, 6
adj1 = [[] for i in range(V + 1)]
addEdge(adj1, 1, 2)
addEdge(adj1, 2, 3)
addEdge(adj1, 3, 4)
addEdge(adj1, 4, 5)
addEdge(adj1, 6, 1)
addEdge(adj1, 5, 6)
checkRingTopology(adj1, V, E)

# # Graph 2
# V, E = 5, 4
# adj2 = [[] for i in range(V + 1)]
# addEdge(adj2, 1, 2)
# addEdge(adj2, 1, 3)
# addEdge(adj2, 3, 4)
# addEdge(adj2, 4, 2)
# checkRingTopology(adj2, V, E)


G = nx.MultiDiGraph()
G.add_edge(0, 1)
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 0)

pos = nx.planar_layout(G)
nx.draw(G,pos=pos, with_labels=True, font_weight='bold', node_size=1000, node_color = 'black',font_color = 'white')
plt.show()

# This code is contributed by mohit kumar 29


# Driver code

# # Graph 1
# V, E = 5, 4
# adj1 = [[] for i in range(V + 1)]
# addEdge(adj1, 1, 2)
# addEdge(adj1, 1, 3)
# addEdge(adj1, 3, 4)
# addEdge(adj1, 4, 5)
# print(adj1)
# checkBusTopology(adj1, V, E)
#
# # Graph 2
# V, E = 4, 4
# adj2 = [[] for i in range(V + 1)]
# addEdge(adj2, 1, 2)
# addEdge(adj2, 1, 3)
# addEdge(adj2, 3, 4)
# addEdge(adj2, 4, 2)
# checkBusTopology(adj2, V, E)
#
# # This code is contributed by mohit kumar 29
