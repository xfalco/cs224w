#! /usr/bin/env python

###########################
# PAGERANK IMPLEMENTATION
# v2 - With weighted edges
###########################


# In this version:
#   - The float attribute of nodes is their pageRank - hence the PageRank hashtable
#     has been eliminated
#   - The edge weights reside in the float attribute of edges


import snap
import time

def simple_graph():
    
    # Generates a simple graph for testing (cs246 book, chapter 5...)
    # Graoh in this verion has weighted edges...
    # Note that the weight attribute can only be initialized once the
    # edges are created
    
    g = snap.TNEANet.New()
    
    for i in range(4):
        g.AddNode(i+1)
    
    g.AddEdge(1,2)
    g.AddEdge(1,3)
    g.AddEdge(1,4)
    
    g.AddEdge(2,1)
    g.AddEdge(2,3)
    
    g.AddEdge(3,2)
    g.AddEdge(3,4)
    
    g.AddEdge(4,1)
    
    g.AddFltAttrE("EValFlt", 1.0)
    g.AddFltAttrN("NValFlt", 0.0)
 
#    AddWEdge(g,1,2,50)
#    AddWEdge(g,1,3,1)
#    AddWEdge(g,1,4,1)
#    AddWEdge(g,2,3,2)
#    AddWEdge(g,3,4,3)

    return g

def AddWEdge(graph, src_node_id, dst_node_id, weight = 1.0):
    
    # adds weight to an edge
    
    edge_id = graph.GetEId(src_node_id, dst_node_id)
    graph.AddFltAttrDatE(edge_id, weight, "EValFlt")
    
    return

def total_difference(HashTable1, HashTable2):
    
    # Returns 'difference' between the values of two hash tables
    # Its calculated as the sum of absolute values of the difference between corresponding items
    # Use it to comapre the outputs of the SNAP PageRank and our python version
    
    difference = 0.00
    for i in HashTable1:
        difference += abs(i.GetDat() - HashTable2.GetDat(i.GetKey()))

    return difference

def initialize_PR_vector_w(graph):
    
    # Sets the inital PR value of all nodes to 1/|N|
    
    initial_PR_score = 1.0/graph.GetNodes()
    
    for n in graph.Nodes():
        graph.AddFltAttrDatN(n.GetId(), initial_PR_score, "NValFlt")
    
    return

def pre_process(graph):
    
    # Build a dictionary with proportion of PR that goes out of every edge of every node
    # Example if a node has 2 out links, one with weight 1 and the other with weight 2
    # then 1/3 of the PR will be passed on through the first link and 2/3 through the other
    
    edge_PR_ratio = {}
    
    for e in graph.Edges():
        src = e.GetSrcNId()
        dst = e.GetDstNId()
        edge_PR_ratio[e.GetId()] = get_w_out_PR_ratio(graph, src, dst)
    
    return edge_PR_ratio

def test_in_node_PR_weight():

    graph = simple_graph()

    PRankH = initialize_PR_vector(graph)
    
    correct_results = [0.375, 0.20833333, 0.20833333, 0.20833333]
    
    error = 0

    for r in range(4):
        print get_in_node_PR_weight (graph, r + 1, PRankH, 1), correct_results[r]
        error = error + get_in_node_PR_weight(graph, r + 1, PRankH) - correct_results[r]

    if error < 0.00001:
        print "test ok - error < 0.00001 (%f)" %(error)
    else:
        print "test not ok - error > 0.00001 (%f)" %(error)
    
def get_in_node_PR_weight_w(graph,edge_PR_ratio, node_id):
    
    # Returns the PR weight that 'reaches' a given node based on inlinks
    # No 'leakage' is considered here
    
    Node = graph.GetNI(node_id)
    in_degree = Node.GetInDeg()

    pr_weight = 0.0
    
    for r in range(in_degree):
        in_node_id = Node.GetInNId(r)
        in_node_pr = graph.GetFltAttrDatN(in_node_id, "NValFlt")
        in_link_pr_contribution = edge_PR_ratio[graph.GetEId(in_node_id, node_id)] * in_node_pr
#        in_link_pr_contribution = get_w_out_PR_ratio(graph, in_node_id, node_id) * in_node_pr
        pr_weight = pr_weight + in_link_pr_contribution
    
    return pr_weight


def get_w_out_PR_ratio(graph, src_node_id, dst_node_id):

    # Returns the weighted PageRank to be transferred from the specified source node to the specified destination node
    
    source_node = graph.GetNI(src_node_id)

    total_weight = 0.0
    pr_weight = 0.0

    # Step 1: Calculate the sum of the weight of all outgoing edges

    for out_edge in source_node.GetOutEdges():
        edge_id = graph.GetEId(src_node_id, out_edge)
        total_weight += graph.GetFltAttrDatE(edge_id, "EValFlt")

    # Step 2: Get the weight of the edge linking the source to the destination nodes

    edge_id = graph.GetEId(src_node_id, dst_node_id)
    edge_weight = graph.GetFltAttrDatE(edge_id, "EValFlt")

    # Step 3: calculate the PR condsidering wieghts

    pr_weight = edge_weight / total_weight

    return pr_weight
    

def RW_iteration_w(graph, edge_PR_ratio, C = 0.85):
 
    # Performs one Random Walk
    
    PRankH_temp = snap.TIntFltH()

    # Step 1: calculate new page ranks from in-nodes
    # This new page rank is 'dampened' by a factor C, usually about 0.85

    for n in graph.Nodes():
        node_id = n.GetId()
        PR = get_in_node_PR_weight_w(graph, edge_PR_ratio, node_id)
        PRankH_temp.AddDat(node_id, PR * C)
        
    # Step 2: The total rank lost to leakage is calculated (sum)
    # The leaked value is then apportioned to all nodes by adding leakage/|N| to each node

    sum = diff = NewVal = 0.00
    
    for i in PRankH_temp:
        sum += i.GetDat()
    
    leaked = (1 - sum)/float(graph.GetNodes())

    for n in graph.Nodes():
        NewVal = PRankH_temp(n.GetId()) + leaked
        OldVal = graph.GetFltAttrDatN(n.GetId(), "NValFlt")
        diff += abs(OldVal - NewVal)
        graph.AddFltAttrDatN(n.GetId(), NewVal, "NValFlt")

    print diff

    # Return value is the 'difference' in value between the new PRs and the old ones.
    # After this value goes below some threshold, we will want to stop iterating random walks

    return diff


def GetPageRankPy_w(graph, C=0.85, Eps = 1e-4, MaxIter = 100):
    
    # This is (our) the Python page rank function
    # Calling is analogous to the SNAP function - you pass the graph and a hash table
    # and the function changes the hash table to reflect the PageRank
    #
    # C is the damping factor
    # When difference between new ranks and old ones is less then Eps, we stop walking
    # Note that if you adjust Eps, C or Maxiter, your results will differ from SNAP's
    
    # Step 0: Add attributes to nodes (to hold PageRank) and edges
    # (to hold edge weights)
    # Also, build a dictionary with proportion of PR that goes out of every edge of every node
    
    edge_PR_ratio = pre_process(graph)

    # Step 1: all nodes have a page rank of 1/|N|

    initialize_PR_vector_w(graph)

    # Step 2: We perform random walks till page ranks don't change or we iterate MaxIter times
    
    for r in range(MaxIter):
        print "iteration ", r 
        difference = RW_iteration_w(graph, edge_PR_ratio, C)
        if difference < Eps:
            break
    
    return  
