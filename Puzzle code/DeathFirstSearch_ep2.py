import sys
from math import *
from collections import *

# FUNCTIONS ***********************************************************************************************************************

def dijkstra_dist_list(graph, initial_node) : # return a dict of shortest dist from initial node to each others
    # ARGUMENTS FORMAT : 
    # graph : dict {'node 0' : [(node, dist), (node, dist)], 'node 1' : [(node, dist)], ...} 
    #         all keys and values are int()
    # initial_node : int() 


    current_node = initial_node
    # Mark the selected initial node with a current distance of 0 and the rest with infinity.
    current_dist = {}
    for k,v in graph.items() :
        if k == current_node :
            current_dist[k] = 0
        else :
            current_dist[k] = float('inf')

    visited = []
    while len(visited) != len(graph.keys()) :
        queue = deque()
        next_node, next_node_d = current_node, float('inf')

        # Visit the direct neighbours of the current node and add distances into current distances list 
        for v in graph[current_node] :
            queue.append(v)

        while queue :
            node = queue.popleft()
            n_index, n_dist = node[0], node[1]
            if current_dist[current_node] + n_dist < current_dist[n_index] :
                current_dist[n_index] = current_dist[current_node] + n_dist

        # Mark the current node as visited
        visited.append(current_node)

        # Chose the next node (the nearrest and non-visited from initial)    
        for k,v in current_dist.items() :
            if k not in visited and v < next_node_d : 
                next_node = k
                next_node_d = v

        current_node = next_node

    return(current_dist)

def dist_bet_2node(graph, a, b) :   # return integer distance bet. 2 nodes a, b
    # ARGUMENTS FORMAT : 
    # graph : dict {'node 0' : [(node, dist), (node, dist)], 'node 1' : [(node, dist)], ...} 
    #         all keys and values are int()
    # a, b  : int(id) of two nodes 
    return(dijkstra_dist_list(graph, a)[b])

def update_cuted_link(graph, a, b) : # set a dist = infiny bet. 2 nodes a, b 
    # ARGUMENTS FORMAT : 
    # graph : dict {'node 0' : [(node, dist), (node, dist)], 'node 1' : [(node, dist)], ...} 
    #         all keys and values are int()
    for v in graph[a] : 
        if v[0] == b : 
            v[1] = float('inf')
    for v in graph[b] : 
        if v[0] ==  a : 
            v[1] = float('inf') 
    return(graph)

def gateways_count(graph, gateways_list) :
    gateways_connected = {}
    for k in graph : 
        gateways_connected[k] = []
    for k,v in graph.items():
        for n in v :
            if n[0] in gateways_list :
                gateways_connected[k].append(n[0])

    filtre_empty = {k:v for k,v in gateways_connected.items() if len(v) > 0}
    gateways_connected = filtre_empty

    return(gateways_connected)


# GAME ****************************************************************************************************************************
# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways

n, l, e = [int(i) for i in input().split()]

graph = {}
for i in range(n) :
    graph[i] = []

for i in range(l):
    n1, n2 = [int(j) for j in input().split()]
    graph[n1].append([n2, 1])
    graph[n2].append([n1, 1])
#print(graph)

# Gateways list
gateways_list = []
for i in range(e):
    ei = int(input())  # the index of a gateway node
    gateways_list.append(ei)
#print(gateways_list)

gateways_dict = {}
for n in gateways_list : 
    gateways_dict[n] = len(graph[n])
#print(gateways_dict)

target_node_dict = gateways_count(graph, gateways_list)

# game loop
while True:
    si = int(input())  # The index of the node on which the Bobnet agent is positioned this turn

    target = []

    if si in target_node_dict.keys() :
        target = [si, target_node_dict[si][0] ]
    else :
        diff_mem = float('-inf')
        n_gat_mem = 0
        for n,v in target_node_dict.items() :
            diff = len(target_node_dict[n]) - dist_bet_2node(graph, si, n)
            n_gat = len(target_node_dict[n])
            if diff >= diff_mem : #and n_gat > n_gat_mem
                diff_mem = diff
                n_gat_mem = n_gat
                target = [n, v[0]]

    print(target[0], target[1])

    target_node_dict[target[0]].remove(target[1]) 
    filtre_empty = {k:v for k,v in target_node_dict.items() if len(v) > 0}
    target_node_dict = filtre_empty
    #print(target_node_dict)