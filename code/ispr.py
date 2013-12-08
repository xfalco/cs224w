### Intelligent Surfer PageRank
### ispr.py
import snap
import csv
import time


def LoadGraph(pFilename):

    ### Initialization
    vGraph = snap.TNEANet.New()
    vNodeTags = {}  # [Node] = [List of tags]
    
    ### Load graph data
    with open(pFilename,'r') as f:
        vReader = csv.reader(f, dialect='excel')
        for vLine in vReader:
            if vGraph.IsNode(int(vLine[0])) == False:
                vGraph.AddNode(int(vLine[0]))
            if vGraph.IsNode(int(vLine[1])) == False:
                vGraph.AddNode(int(vLine[1]))        
            vGraph.AddEdge(int(vLine[0]), int(vLine[1]))
            vEdgeId = vGraph.GetEId(int(vLine[0]), int(vLine[1]))
            vGraph.AddIntAttrDatE(vEdgeId, int(vLine[2]), "QuestionId")
            vGraph.AddFltAttrDatE(vEdgeId, float(vLine[3]), "UpVotes")
            vGraph.AddFltAttrDatE(vEdgeId, float(vLine[4]), "DownVotes")
            vGraph.AddFltAttrDatE(vEdgeId, float(vLine[5]), "SrcRep")
            vGraph.AddFltAttrDatE(vEdgeId, float(vLine[6]), "DstRep")

            if int(vLine[0]) not in vNodeTags:
                vNodeTags[int(vLine[0])] = []
            if int(vLine[1]) not in vNodeTags:
                vNodeTags[int(vLine[1])] = []
            vNodeTags[int(vLine[0])].extend(vLine[7].split(","))
            vNodeTags[int(vLine[1])].extend(vLine[7].split(","))

    '''
    print '*** here'
    print vNodeTags[111]
    print '*** set'
    print set(vNodeTags[111])
    print '*** list'
    print list(set(vNodeTags[111]))
    '''
    for vNode in vNodeTags:
        vNodeTags[vNode] = list(set(vNodeTags[vNode]))
    
    return (vGraph, vNodeTags)


def WritePagerank(pPR, pFilename):
    with open(pFilename,'w') as f:
        for item in pPR:
            vNode = item.GetKey()
            vPageRank = item.GetDat()
            f.write(str(vNode)+','+str(vPageRank)+'\n')


def TagNode(pNodeTags):
    vTagNode = {}   # [Tag] = [List of nodes]
    for vNode in pNodeTags:
        for vTag in pNodeTags[vNode]:
            if vTag not in vTagNode:
                vTagNode[vTag] = []
            vTagNode[vTag].append(vNode)
    return vTagNode


def CopyGraph(pGraph, pNodeTags, pTag):
    vSubgraphNodes = snap.TIntV()
    for vNode in pNodeTags[pTag]:
        vSubgraphNodes.Add(vNode)
    vGraph = snap.GetSubGraph(pGraph, vSubgraphNodes)
    return vGraph


def main():
    vStartTime = time.clock()

    vFilename = '../data/network_python.graph'
    print 'Loading graph:', vFilename
    [vGraph, vNodeTags] = LoadGraph(vFilename)
    
    vFilename = '../data/ispr/ispr__all.txt'
    print 'Pagerank for all tags:', vFilename
    vPR = snap.TIntFltH()
    snap.GetPageRank(vGraph, vPR)
    WritePagerank(vPR, vFilename)
    
    vFilename = '../data/ispr/ispr__tagstats.txt'
    print 'Tag statistics:', vFilename
    vTagNodes = TagNode(vNodeTags)
    with open(vFilename,'w') as f:
        for vTag in vTagNodes:
            f.write(str(vTag)+','+str(len(vTagNodes[vTag]))+','+str(vTagNodes[vTag])+'\n')
    
    print 'Calculating Pagerank for each tag'
    for vTag in vTagNodes:
        vFilename = '../data/ispr/ispr_'+vTag+'.txt'
        print '  Pagerank:', vFilename
        vGraphTag = CopyGraph(vGraph, vTagNodes, vTag)
        vPR = snap.TIntFltH()
        snap.GetPageRank(vGraphTag, vPR)
        WritePagerank(vPR, vFilename)

    vEndTime = time.clock()
    print 'Runtime:', vEndTime - vStartTime,'seconds'

if __name__ == "__main__":
    main()

