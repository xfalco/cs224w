### Net cumulative discount gain for SO python graph
### ncdg_python.py
import sys
import snap
import csv
import math
import random

def LoadGraph(pFilename):

    ### Initialization
    vGraph = snap.TNEANet.New()
    vQuestionTags = {}
    
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
            if int(vLine[2]) not in vQuestionTags:
                vQuestionTags[int(vLine[2])] = vLine[7].split(",")
            #break

    ### Test the first edge
    '''
    vEdgeId = vGraph.GetEId(111,59)
    print vGraph.GetIntAttrDatE(vEdgeId, "QuestionId")
    print vGraph.GetFltAttrDatE(vEdgeId, "UpVotes")
    print vGraph.GetFltAttrDatE(vEdgeId, "DownVotes")
    print vGraph.GetFltAttrDatE(vEdgeId, "SrcRep")
    print vGraph.GetFltAttrDatE(vEdgeId, "DstRep")
    vEdge = vGraph.GetEI(111,59)    
    print vGraph.GetIntAttrDatE(vEdge, "QuestionId")
    print vGraph.GetFltAttrDatE(vEdge, "UpVotes")
    print vGraph.GetFltAttrDatE(vEdge, "DownVotes")
    print vGraph.GetFltAttrDatE(vEdge, "SrcRep")
    print vGraph.GetFltAttrDatE(vEdge, "DstRep")
    print vQuestionTags[337]
    '''
    return (vGraph, vQuestionTags)


def LoadVoteRatio(pFilename):
    vVoteRatio = {}
    with open(pFilename,'r') as f:
        vReader = csv.reader(f, dialect='excel')
        for vLine in vReader:
            if vLine[0] == 'OwnerUserId':
                continue
            vVoteRatio[int(vLine[0])] = float(vLine[1])
    return vVoteRatio


def LoadPagerank(pFilename):
    vPagerank = {}
    with open(pFilename,'r') as f:
        vReader = csv.reader(f, dialect='excel')
        for vLine in vReader:
            if vLine[0] == 'id':
                continue
            vPagerank[int(vLine[0])] = float(vLine[1])
    return vPagerank


def DCG(pOrder, pRelevance):
    vRank = 0
    vDCG = 0.0
    vSortedAnsUserId = sorted(pOrder, key=lambda l: pOrder[l], reverse=True)
    for vAnsUserId in vSortedAnsUserId:
        vAnsEdge = []
        for (vSrcId, vDstId) in pRelevance.keys():
            if vDstId == vAnsUserId:
                vAnsEdge.append((vSrcId, vDstId))
        random.shuffle(vAnsEdge)
        for (vSrcId, vDstId) in vAnsEdge:
            vRank += 1
            if vRank == 1:
                vDCG += pRelevance[(vSrcId, vDstId)]
            else:
                vDCG += pRelevance[(vSrcId, vDstId)] / math.log(float(vRank),2)
    return vDCG


def DCGMax(pRelevance):
    vRank = 0
    vDCGmax = 0.0
    vSortedRel = sorted(pRelevance, key=lambda l: pRelevance[l], reverse=True)
    for (vSrcId, vDstId) in vSortedRel:
        vRank += 1
        if vRank == 1:
            vDCGmax += pRelevance[(vSrcId, vDstId)]
        else:
            vDCGmax += pRelevance[(vSrcId, vDstId)] / math.log(float(vRank),2)
    return vDCGmax


def main():
    
    vFilename = "../data/network_python.graph"
    print 'Loading graph data from', vFilename
    (vGraph, vQuestionTags) = LoadGraph(vFilename)
    print '#nodes = %d, #edges = %d' % (vGraph.GetNodes(), vGraph.GetEdges())
    print '#questions = %d' % len(vQuestionTags)
    
    vFilename = "../data/voteratio_python.csv"
    print 'Loading python vote ratio data from', vFilename
    vVoteRatio = LoadVoteRatio(vFilename)
    print '#voteratio = %d' % len(vVoteRatio)    

    vFilename = "../data/pagerank_net.txt"
    print 'Loading pagerank data from', vFilename
    vPagerank = LoadPagerank(vFilename)
    print '#pagerank = %d' % len(vPagerank)
    
    vNDCG_Rep = {}
    vNDCG_RepPython = {}
    vNDCG_Pagerank = {}
    vCount = 0
    #for vQuestionId in vQuestionTags:
    vQuestionId = 613183
    if 1==1:
        vCount += 1
        print 'Calculating NDCG for %d\t(%6.4f percent complete)' % \
                (vQuestionId, float(vCount)/len(vQuestionTags)*100)

        ## Populate Reputation and Relevance for the QuestionId
        vReputation = {}
        vReputationPython = {}
        vRelevance = {}
        for vEdge in vGraph.Edges():
            if vGraph.GetIntAttrDatE(vEdge.GetId(), "QuestionId") == vQuestionId:
                #print vEdge.GetSrcNId(), vEdge.GetDstNId(), vEdge.GetId()
                vReputation[vEdge.GetDstNId()] = \
                        vGraph.GetFltAttrDatE(vEdge.GetId(), "DstRep")
                vReputationPython[vEdge.GetDstNId()] = \
                        vGraph.GetFltAttrDatE(vEdge.GetId(), "DstRep") * \
                        vVoteRatio[vEdge.GetDstNId()]
                vRelevance[(vEdge.GetSrcNId(), vEdge.GetDstNId())] = \
                        vGraph.GetFltAttrDatE(vEdge.GetId(), "UpVotes") - \
                        vGraph.GetFltAttrDatE(vEdge.GetId(), "DownVotes")
                # Should be vRelevance[vAnswerId] but AnswerId is not in graph data

        ## Calculate NDCGs
        vDCGmax = DCGMax(vRelevance)
        if vDCGmax == 0:
            vNDCG_Rep[vQuestionId] = 0.0
            vNDCG_RepPython[vQuestionId] = 0.0
            vNDCG_Pagerank[vQuestionId] = 0.0
        else:
            vNDCG_Rep[vQuestionId] = DCG(vReputation, vRelevance) / vDCGmax
            vNDCG_RepPython[vQuestionId] = DCG(vReputationPython, vRelevance) / vDCGmax
            vNDCG_Pagerank[vQuestionId] = DCG(vPagerank, vRelevance) / vDCGmax

        ## Cleanup memory
        del vReputation
        del vReputationPython
        del vRelevance

    ## Write NDCGs to file
    vFilename = "../data/ndcg.txt"
    print 'Writing NDCGs to', vFilename
    with open(vFilename,'w') as f:
        f.write('QuestionId,NDCG_Rep,NDCG_RepPython,NDCG_Pagerank\n')
        #for vQuestionId in vQuestionTags:
        vQuestionId = 613183
        if 1==1:
            f.write(str(vQuestionId) + ',' + \
                    str(vNDCG_Rep[vQuestionId]) + ',' + \
                    str(vNDCG_RepPython[vQuestionId]) + ',' + \
                    str(vNDCG_Pagerank[vQuestionId])+'\n')


### ---------- 2nd version ----------
def LoadGraph2(pFilename):

    ### Initialization
    vQuestionTags = {}     # [qId] = [Tags]
    vUserReputation = {}   # [dstId] = DstRep
    vAnswerRelevance = {}  # [vAnswerId] = Upvote - Downvote
    vHashQuesIdAnsId = {}  # [qId] = [vAnswerId1, vAnswerId2, ...]
    vHashAnsIdEdge = {}    # [vAnswerId] = (SrcId, DstId)

    ### Load graph data
    vAnswerId = 0
    with open(pFilename,'r') as f:
        vReader = csv.reader(f, dialect='excel')
        for vLine in vReader:
            vAnswerId += 1
            if int(vLine[2]) not in vQuestionTags:
                vQuestionTags[int(vLine[2])] = vLine[7].split(",")
            if int(vLine[1]) not in vUserReputation:
                vUserReputation[int(vLine[1])] = float(vLine[6])
            if vAnswerId not in vAnswerRelevance:
                vAnswerRelevance[vAnswerId] = float(vLine[3]) - float(vLine[4])
            if int(vLine[2]) not in vHashQuesIdAnsId:
                vHashQuesIdAnsId[int(vLine[2])] = [vAnswerId]
            else:
                vHashQuesIdAnsId[int(vLine[2])].append(vAnswerId)
            vHashAnsIdEdge[vAnswerId] = (int(vLine[0]), int(vLine[1]))
            #break

    return (vQuestionTags, vUserReputation, vAnswerRelevance, \
            vHashQuesIdAnsId, vHashAnsIdEdge)


def main2():
    
    vFilename = "../data/network_python.graph"
    print 'Loading graph data from', vFilename
    (vQuestionTags, vUserReputation, vAnswerRelevance, \
     vHashQuesIdAnsId, vHashAnsIdEdge) = LoadGraph2(vFilename)
    print '#vQuestionTags    = %d' % len(vQuestionTags)
    print '#vUserReputation  = %d' % len(vUserReputation)
    print '#vAnswerRelevance = %d' % len(vAnswerRelevance)
    print '#vHashQuesIdAnsId = %d' % len(vHashQuesIdAnsId)
    print '#vHashAnsIdEdge   = %d' % len(vHashAnsIdEdge)
    
    vFilename = "../data/voteratio_python.csv"
    print 'Loading python vote ratio data from', vFilename
    vVoteRatio = LoadVoteRatio(vFilename)
    print '#voteratio = %d' % len(vVoteRatio)    

    vFilename = "../data/pagerank_net.txt"
    print 'Loading pagerank data from', vFilename
    vPagerank = LoadPagerank(vFilename)
    print '#pagerank = %d' % len(vPagerank)
    

    ## Calculate NDCGs and write to file
    vFilename = "../data/ndcg.txt"
    print 'Calculating and writing NDCGs to', vFilename
    with open(vFilename,'w') as f:
        f.write('QuestionId,NDCG_Rep,NDCG_RepPython,NDCG_Pagerank,numAnswers\n')
        vNDCG_Rep = {}
        vNDCG_RepPython = {}
        vNDCG_Pagerank = {}
        vCount = 0
        for vQuestionId in vQuestionTags:
        #vQuestionId = 613183
        #if 1==1:
            vCount += 1
            print 'Calculating NDCG for %d\t(%6.4f percent complete)' % \
                    (vQuestionId, float(vCount)/len(vQuestionTags)*100)

            ## Populate Reputation and Relevance for the QuestionId
            vReputation = {}
            vReputationPython = {}
            vRelevance = {}
            for vAnsIdx in range(0,len(vHashQuesIdAnsId[vQuestionId])):
                vAnswerId = vHashQuesIdAnsId[vQuestionId][vAnsIdx]
                vDstId = vHashAnsIdEdge[vAnswerId][1]
                vRelevance[vHashAnsIdEdge[vAnswerId]] = vAnswerRelevance[vAnswerId]
                vReputation[vDstId] = vUserReputation[vDstId]
                if vDstId in vVoteRatio:
                    vReputationPython[vDstId] = vUserReputation[vDstId] * vVoteRatio[vDstId]
                else:
                    vReputationPython[vDstId] = 0.0
            
            ## Calculate NDCGs
            vDCGmax = DCGMax(vRelevance)
            if vDCGmax == 0:
                vNDCG_Rep[vQuestionId] = 0.0
                vNDCG_RepPython[vQuestionId] = 0.0
                vNDCG_Pagerank[vQuestionId] = 0.0
            else:
                vNDCG_Rep[vQuestionId] = DCG(vReputation, vRelevance) / vDCGmax
                vNDCG_RepPython[vQuestionId] = DCG(vReputationPython, vRelevance) / vDCGmax
                vNDCG_Pagerank[vQuestionId] = DCG(vPagerank, vRelevance) / vDCGmax

            ## Write NDCGs to file
            f.write(str(vQuestionId) + ',' + \
                    str(vNDCG_Rep[vQuestionId]) + ',' + \
                    str(vNDCG_RepPython[vQuestionId]) + ',' + \
                    str(vNDCG_Pagerank[vQuestionId]) + ',' + \
                    str(len(vHashQuesIdAnsId[vQuestionId]))+'\n')


if __name__ == "__main__":
    #main()
    main2()
