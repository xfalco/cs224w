### Intelligent Surfer PageRank
### ispr.py
import snap
import csv
import time
import os
import sys
import string
import math

gDebug = False

def LoadGraph(pFilename):

    ## Initialization
    vGraphTrain = snap.TNEANet.New()
    vGraphAll = snap.TNEANet.New()
    vNodeTags = {}          # [Node] = [List of tags]
    vTestQuesVotes = {}     # [QuestionId][AnswererId] = net votes
    vTestQuesTags = {}      # [QuestionId] = [List of tags]

    with open(pFilename,'r') as f:
        vReader = csv.reader(f, dialect='excel')
        for vLine in vReader:
            ## Load graph data
            ReadEdge(vGraphAll, vLine)
            if int(vLine[2]) % 10 == 0:  # Testing graph

                ## Index test questions: net votes
                vNetVotes = float(vLine[3]) - float(vLine[4])
                if int(vLine[2]) not in vTestQuesVotes:
                    vTestQuesVotes[int(vLine[2])] = {}
                vTestQuesVotes[int(vLine[2])][int(vLine[1])] = vNetVotes

                ## Index test questions: tags
                if int(vLine[2]) not in vTestQuesTags:
                    vTestQuesTags[int(vLine[2])] = []
                vTestQuesTags[int(vLine[2])].extend(vLine[7].split(","))

            else:   # Training graph
                ReadEdge(vGraphTrain, vLine)

            ## Index node tags
            if int(vLine[0]) not in vNodeTags:
                vNodeTags[int(vLine[0])] = []
            if int(vLine[1]) not in vNodeTags:
                vNodeTags[int(vLine[1])] = []
            vNodeTags[int(vLine[0])].extend(vLine[7].split(","))
            vNodeTags[int(vLine[1])].extend(vLine[7].split(","))

    ## Format indices
    for vNode in vNodeTags:
        vNodeTags[vNode] = list(set(vNodeTags[vNode]))
    for vQuestion in vTestQuesTags:
        vTestQuesTags[vQuestion] = list(set(vTestQuesTags[vQuestion]))
    
    return (vGraphTrain, vGraphAll, vNodeTags, vTestQuesVotes, vTestQuesTags)


def ReadEdge(pGraph, pLine):
    if pGraph.IsNode(int(pLine[0])) == False:
        pGraph.AddNode(int(pLine[0]))
    if pGraph.IsNode(int(pLine[1])) == False:
        pGraph.AddNode(int(pLine[1]))        
    pGraph.AddEdge(int(pLine[0]), int(pLine[1]))
    vEdgeId = pGraph.GetEId(int(pLine[0]), int(pLine[1]))
    pGraph.AddIntAttrDatE(vEdgeId, int(pLine[2]), "QuestionId")
    pGraph.AddFltAttrDatE(vEdgeId, float(pLine[3]), "UpVotes")
    pGraph.AddFltAttrDatE(vEdgeId, float(pLine[4]), "DownVotes")
    pGraph.AddFltAttrDatE(vEdgeId, float(pLine[5]), "SrcRep")
    pGraph.AddFltAttrDatE(vEdgeId, float(pLine[6]), "DstRep")    


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


def CalcIDF(pTagNodes, pNumQuestions):
    vTagIDF = {}    # [Tag] = Inverse document frequency
    for vTag in pTagNodes:
        vTagIDF[vTag] = math.log(float(pNumQuestions)/len(pTagNodes[vTag]))
    return vTagIDF


def CopyGraph(pGraph, pNodeTags, pTag):
    vSubgraphNodes = snap.TIntV()
    for vNode in pNodeTags[pTag]:
        vSubgraphNodes.Add(vNode)
    vGraph = snap.GetSubGraph(pGraph, vSubgraphNodes)
    return vGraph


def ReadISPR(pISPRDir):
    vTagPR = {}     # [Tag][User] = Tag-specific pagerank
    vFilelist = [ f for f in os.listdir(pISPRDir) ]
    for vFilename in vFilelist:
        if vFilename != 'ispr__tagstats.txt':
            vTag = string.replace(string.replace(vFilename,'ispr_',''),'.txt','')
            vTagPR[vTag] = {}
            with open(pISPRDir+vFilename,'r') as f:
                vReader = csv.reader(f, dialect='excel')
                for vLine in vReader:
                    vTagPR[vTag][int(vLine[0])] = float(vLine[1])
    return vTagPR


def PairwiseRank(pCutoff, pTagPR, pTestQuesVotes, pTestQuesTags, pTagIDF, pOption):
    vNumWrong = 0
    vNumRight = 0
    vCount = 0


    for vQuesId in pTestQuesVotes:
        #if vQuesId != 4504470:  # 8934740, 4504470
            #continue

        if gDebug:
            vCount += 1 
            print '\nvQuesId: %d\t(%2.2f pct done)' % (vQuesId, float(vCount) / len(pTestQuesVotes) * 100)

        if gDebug:
            print 'Before:', len(pTestQuesVotes[vQuesId])
        pTestQuesVotes[vQuesId] = {key: value for key, value in pTestQuesVotes[vQuesId].items() if value >= pCutoff}
        if gDebug:
            print 'After:', len(pTestQuesVotes[vQuesId])

        vQuestionSort = sorted(pTestQuesVotes[vQuesId], key=lambda l : pTestQuesVotes[vQuesId][l], reverse = True)

        if len(vQuestionSort) <= 1:
            continue
        
        if gDebug:
            print 'pTestQuesTags[%d]: %s' %(vQuesId, pTestQuesTags[vQuesId])
            print 'vQuestionSort:', vQuestionSort
            for vUserId in vQuestionSort:
                print 'pTestQuesVotes[%d][%d]: %d' % (vQuesId, vUserId, pTestQuesVotes[vQuesId][vUserId])
        
        vISPR = QuestionISPR(vQuestionSort, pTestQuesTags[vQuesId], pTagPR, pTagIDF)

        if gDebug:
            for vUserId in vQuestionSort:
                print 'vISPR[%d]: %f' % (vUserId, vISPR[vUserId])
        
        vQuesRight = 0
        vQuesWrong = 0
        if pOption == 'Top':
            vGood = True
            for vRank in range(1,len(vQuestionSort)):
                if vISPR[vQuestionSort[vRank]] > vISPR[vQuestionSort[0]]:
                    vGood = False
                    break
            if vGood:
                vNumRight += 1
                vQuesRight += 1
            else:
                vNumWrong += 1
                vQuesWrong += 1
            if gDebug:
                print 'vQuesWrong: %d, vQuesRight: %d' %(vQuesWrong, vQuesRight)
        elif pOption == 'All':
            for vRankLo in range(1,len(vQuestionSort)):
                for vRankHi in range(0,vRankLo):
                    if vISPR[vQuestionSort[vRankHi]] >= vISPR[vQuestionSort[vRankLo]]:
                        vNumRight += 1
                        vQuesRight += 1
                    else:
                        vNumWrong += 1
                        vQuesWrong += 1
            if gDebug:
                print 'vQuesWrong: %d, vQuesRight: %d' %(vQuesWrong, vQuesRight)

    return (vNumWrong, vNumRight)


def QuestionISPR(pUsers, pTags, pTagPR, pTagIDF):
    vISPR = {}    # [UserId] = Intelligent Surfer Pagerank
    vMissing = {} # [UserId] = # of tags that are not found in ../ispr_*.txt

    ## Initialize
    for vUser in pUsers:
        vISPR[vUser] = float(0)
        vMissing[vUser] = len(pTags)
    
    ## Method 1: P(q) is 1/|Q|
    for vTag in pTags:
        for vUser in pUsers:
            if vUser in pTagPR[vTag]:
                vISPR[vUser] += pTagPR[vTag][vUser]
                vMissing[vUser] -= 1
    
    for vUser in pUsers:
        vISPR[vUser] += vMissing[vUser] * float(pTagPR['_all'][vUser])
    '''
    
    ## Method 2: P(q) is TF-IDF  (TF is binary, so it's ignored)
    for vTag in pTags:
        if vTag != 'python':
            vIDF = pTagIDF[vTag]
        else:
            vIDF = 0
        for vUser in pUsers:
            if vUser in pTagPR[vTag]:
                vISPR[vUser] += pTagPR[vTag][vUser] * vIDF
    '''
    if gDebug:
        for vTag in pTags:
            print 'pTagIDF[%s]: %f' % (vTag, pTagIDF[vTag])
    
    return vISPR


def main():
    vStartTime = time.clock()
    vTrain = False
    if len(sys.argv) == 2:
        if string.upper(sys.argv[1]) == 'TRAIN':
            vTrain = True

    ## Read edgelist into training and test graphs
    vFilename = '../data/network_python.graph'
    print 'Loading graph:', vFilename
    [vGraphTrain, vGraphAll, vNodeTags, vTestQuesVotes, vTestQuesTags] = LoadGraph(vFilename)
    print 'Training graph: %d nodes, %d edges' % (vGraphTrain.GetNodes(), vGraphTrain.GetEdges())
    print 'Entire   graph: %d nodes, %d edges' % (vGraphAll.GetNodes(), vGraphAll.GetEdges())
    print '# of test questions: %d' % (len(vTestQuesVotes))
    print '**Runtime:', time.clock() - vStartTime,'seconds'
    
    if vTrain:
        print 'Train the intelligent surfer!'

        ## Initialize output folder
        vFilename = '../data/ispr/'
        print 'Remove all files in', vFilename
        filelist = [ f for f in os.listdir(vFilename) ]
        for f in filelist:
            os.remove(vFilename+f)
        print '**Runtime:', time.clock() - vStartTime,'seconds'

        ## Calculate statistics
        vFilename = '../data/ispr/ispr__tagstats.txt'
        print 'Tag statistics:', vFilename
        vTagNodes = TagNode(vNodeTags)
        vTagIDF = CalcIDF(vTagNodes,vGraphAll.GetNodes())
        with open(vFilename,'w') as f:
            for vTag in vTagNodes:
                f.write(str(vTag)+','+str(len(vTagNodes[vTag]))+','+str(vTagNodes[vTag])+'\n')
        print '**Runtime:', time.clock() - vStartTime,'seconds'

        ## Pagerank for entire training graph
        vFilename = '../data/ispr/ispr__all.txt'
        print 'Pagerank for all tags:', vFilename
        vPR = snap.TIntFltH()
        snap.GetPageRank(vGraphAll, vPR)
        WritePagerank(vPR, vFilename)
        print '**Runtime:', time.clock() - vStartTime,'seconds'
        
        ## Pagerank for each tag in training graph
        print 'Calculating Pagerank for each tag'
        for vTag in vTagNodes:
            vGraphTag = CopyGraph(vGraphTrain, vTagNodes, vTag)
            if vGraphTag.GetNodes() > 0:
                vFilename = '../data/ispr/ispr_'+vTag+'.txt'
                #print '  Pagerank:', vFilename
                vPR = snap.TIntFltH()
                snap.GetPageRank(vGraphTag, vPR)
                WritePagerank(vPR, vFilename)
        print '**Runtime:', time.clock() - vStartTime,'seconds'    
    
    ## Pagerank for each node in testing graph
    print 'Calculating ISPR for each test question'

    # Initialization
    if not vTrain:
        print '  Read data'
        vTagNodes = TagNode(vNodeTags)
        vTagIDF = CalcIDF(vTagNodes,vGraphAll.GetNodes())
    vISPRDir = '../data/ispr/'
    vTagPR = ReadISPR(vISPRDir)
    vNumWrongTop = {}   # [Cutoff] = number of wrong rankings for top answer
    vNumRightTop = {}   # [Cutoff] = number of right rankings for top answer
    vNumWrongAll = {}   # [Cutoff] = number of wrong rankings for all answers
    vNumRightAll = {}   # [Cutoff] = number of right rankings for all answers

    # Computation
    for vCutoff in range(-5,100):
        print '=' * 80
        print ' Cutoff:', vCutoff
        [vNumWrongTop[vCutoff], vNumRightTop[vCutoff]] = PairwiseRank(vCutoff, vTagPR, vTestQuesVotes, vTestQuesTags, vTagIDF, 'Top')
        [vNumWrongAll[vCutoff], vNumRightAll[vCutoff]] = PairwiseRank(vCutoff, vTagPR, vTestQuesVotes, vTestQuesTags, vTagIDF, 'All')

    # Output results
    print '=' * 80
    print 'Final output'
    print '{0:>8}{1:>16}{2:>16}{3:>16}{4:>16}'.format('Cutoff', 'vNumWrongTop', 'vNumRightTop', 'vNumWrongAll', 'vNumRightAll')
    for vCutoff in range(-5,100):
        print '{0:8d}{1:16d}{2:16d}{3:16d}{4:16d}'.format(vCutoff, vNumWrongTop[vCutoff], vNumRightTop[vCutoff], vNumWrongAll[vCutoff], vNumRightAll[vCutoff])
    print '**Runtime:', time.clock() - vStartTime,'seconds'
    

if __name__ == "__main__":
    main()

