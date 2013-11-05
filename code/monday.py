from snap import *
import prw3
import pickle


def load_weighted_edgelist(filename):

	print "\nOpening ", filename
	f = open(filename, "rb")
	edge_list = pickle.load(f)
	f.close()
	print filename, " loaded, ", len(edge_list), "edges"

	return edge_list

def create_weighted_edge_graph(edge_list):

	print "\nCreating graph"
	g = TNEANet.New()
	l = range(len(edge_list))
	
	for i in l:
		edge1 = int(edge_list[i][0][0])
		edge2 = int(edge_list[i][0][1])
		if not g.IsNode(edge1):
			g.AddNode(edge1)
		if not g.IsNode(edge2):
			g.AddNode(edge2)
		g.AddEdge(edge1, edge2)
				
	g.AddFltAttrE("EValFlt", 1.0)
	g.AddFltAttrN("NValFlt", 0.0)
	
	for i in l:
		edge1 = int(edge_list[i][0][0])
		edge2 = int(edge_list[i][0][1])
		weight = float(edge_list[i][0][2])
# 		print edge1, edge2, weight
		prw3.AddWEdge(g, edge1, edge2, weight)
# 		print "added weight ", g.GetFltAttrDatE(g.GetEId(edge1, edge2,), "EValFlt")

		print "graph created" , g.GetNodes(), "nodes", g.GetEdges(),"edges"
	return g
	
print 
print
print "---------------------"
print

edge_list = load_weighted_edgelist("weighted_edge_list")
print
print "---------------------"
print
g = create_weighted_edge_graph(edge_list)
prw3.GetPageRankPy_w(g)

pr = [0] * g.GetNodes()

print "\n----saving-----------------\n"

# for n in g.Nodes():
# 	print g.GetFltAttrDatN(n.GetId(), "NValFlt")

SaveEdgeList(g, "weighted_graph_pr.txt", "Save as tab-separated list of edges")

f = open("pagerank.txt","w")

for n in g.Nodes():
	buf = str(n.GetId()) + "," + str(g.GetFltAttrDatN(n.GetId(), "NValFlt"))
	f.write (buf)
	f.write("\n")
	
print "\n... ok\n"

f.close()

