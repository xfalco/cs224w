#! /usr/bin/env python

###########################
# PAGERANK IMPLEMENTATION
# V1 - Plain vanilla
###########################

import snap

def simple_graph():
    
    # Generates a simple graph for testing (cs246 book, chaoer 5...)
    
    graph = snap.PNGraph.New()
    
    for i in range(4):
        graph.AddNode(i+1)
    
    graph.AddEdge(1,2)
    graph.AddEdge(1,3)
    graph.AddEdge(1,4)
    
    graph.AddEdge(2,1)
    graph.AddEdge(2,3)
    
    graph.AddEdge(3,2)
    graph.AddEdge(3,4)
    
    graph.AddEdge(4,1)
    
    return graph

def total_difference(HashTable1, HashTable2):
    
    # Returns 'difference' between the values of two hash tables
    # Its calculated as the sum of absolute values of the difference between corresponding items
    # Use it to comapre the outputs of the SNAP PageRank and our python version
    
    difference = 0.00
    for i in HashTable1:
        difference += abs(i.GetDat() - HashTable2.GetDat(i.GetKey()))

    return difference

def initialize_PR_vector(graph, PRankH):
    
    # Sets the inital PR value of all nodes to 1/|N|
    
    initial_PR_score = float(1)/graph.GetNodes()
        
    for Node in graph.Nodes():
        PRankH.AddDat(Node.GetId(), initial_PR_score)

    return

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
    
def get_in_node_PR_weight(graph, node_id, PRankH):
    
    # Returns the PR weight that 'reaches' a given node based on inlinks
    # No 'leakage' is considered here
    
    Node = graph.GetNI(node_id)
    in_degree = Node.GetInDeg()

    pr_weight = 0.00
    
    for r in range(in_degree):
        in_node_id = Node.GetInNId(r)
        In_Node = graph.GetNI(in_node_id)
        in_node_out_degree = In_Node.GetOutDeg()
        # The PR wirght is sum of the contribution of each in-node
        # Each in-node contributes its own page rank divided by the number of outlinks it has
        pr_weight = pr_weight + PRankH(in_node_id)/in_node_out_degree

    return pr_weight

def RW_iteration(graph, PRankH, C=0.85):
 
    # Performs one Random Walk
    
    PRankH_temp = snap.TIntFltH()

    # Step 1: calculate new page ranks from in-nodes
    # This new page rank is 'dampened' by a factor C, usually about 0.85

    for i in PRankH:
        node_id = i.GetKey()
        PR = get_in_node_PR_weight(graph, node_id, PRankH)
        PRankH_temp.AddDat(node_id, PR * C)
        
    # Step 2: The total rank lost to leakage is calculated (sum)
    # The leaked value is then apportioned to all nodes by adding leakage/|N| to each node

    sum = diff = NewVal = 0.00
    
    for i in PRankH_temp:
        sum += i.GetDat()
    
    leaked = (1 - sum)/float(graph.GetNodes())

    for i in PRankH:
        NewVal = PRankH_temp(i.GetKey()) + leaked
        diff += abs(PRankH(i.GetKey()) - NewVal)
        PRankH.AddDat(i.GetKey(), NewVal)

    print diff

    # Return value is the 'difference' in value between the new PRs and the old ones.
    # After this value goes below some threshold, we will want to stop iterating random walks

    return diff

def GetPageRankPy(graph, PRankH, C=0.85, Eps = 1e-4, MaxIter = 100):
    
    # This is (our) the Python page rank function
    # Calling is analogous to the SNAP function - you pass the graph and a hash table
    # and the function changes the hash table to reflect the PageRank
    #
    # C is the damping factor
    # When difference between new ranks and old ones is less then Eps, we stop walking
    # Note that if you adjust Eps, C or Maxiter, your results will differ from SNAP's
    
    # Step 1: all nodes have a page rank of 1/|N|
    initialize_PR_vector(graph, PRankH)
    
    # We perform random walks till page ranks don't change or we iterate MaxIter times
    for r in range(MaxIter):
        difference = RW_iteration(graph, PRankH, C)
        if difference < Eps:
            break
    
    return

def h0():
    
    # Runs pagerank on the wiki vote dataset
    # Uses both the SNAP and our Python versions
    # And compares results...
    
    file = "wiki-vote.txt"
    graph = snap.LoadEdgeList(snap.PUNGraph, file, 0, 1)
    
    PR_Python = snap.TIntFltH()
    PR_SNAP = snap.TIntFltH()
    
    GetPageRankPy(graph, PR_Python)
    snap.GetPageRank(graph, PR_SNAP)
    
    print
    print "PR_Python len ", PR_Python.Len()
    print "PR_SNAP len ", PR_SNAP.Len()
    print
    print "Difference between SNAP and our Python implementations = ", total_difference(PR_Python, PR_SNAP)
    print
    print

if __name__ == '__main__':
    h0()
