# tests efficiency from graph passed in as first parameter
# uses "../data/network_python.graph" if none passed in
# @author xfalco

import sys
import snap
import prw3
import csv
from math import log

if len(sys.argv) is 1 :
   filename = "network_python.graph"
else :
   filename = sys.argv[1]

#
# LOAD FILE
#

questions = {}
weights = {}
soReputations = {}
prReputations = {}
graph = snap.TNEANet.New()

CUT_OFF_RANK = 5

file = open(filename, 'rU')
reader = csv.reader(file, dialect='excel')
for list in reader :
  srcNId = int(list[0])
  dstNId = int(list[1])
  eAttrQId = int(list[2])
  eAttrUpVotes = float(list[3])
  eAttrDownVotes = float(list[4])
  eAttrSrcRep = float(list[5])
  eAttrDstRep = float(list[6])
  eAttrTags = list[7]
  key = (srcNId, dstNId)
  if not key in weights:
    weights[key] = 0
  weights[key] = weights[key] + eAttrUpVotes - eAttrDownVotes
  soReputations[srcNId] = eAttrSrcRep
  soReputations[dstNId] = eAttrDstRep
  net = eAttrUpVotes - eAttrDownVotes
  if net < CUT_OFF_RANK:
    continue
  if not eAttrQId in questions :
    questions[eAttrQId] = {}
  questions[eAttrQId][dstNId] = net
file.close()

for key in weights.keys() :
  if weights[key] <= 0:
    del weights[key]
  else:
  	# PK - many edges have weight 1, so you if you do log(1) you get 0
  	# and we dont want zero weight edges 
  	
    #weights[key] = log(weights[key])   
    pass

# PK - dont think normalization is required... results are the same either way (at least iteration errors are)

# sumWeights = sum(weights.values())
# for key in weights.keys():
#   weights[key] = weights[key] / sumWeights

# PK - first add all nodes and edges

for (src, dst) in weights.keys() :
  if not graph.IsNode(src):
    graph.AddNode(src)
  if not graph.IsNode(dst):
    graph.AddNode(dst)
  graph.AddEdge(src,dst)  # PK - You were not using AddEdge - so no edges were actually
  						  # being created		

# PK - then link the attributes to nodes and edges
  
graph.AddFltAttrE("EValFlt", 1.0)
graph.AddFltAttrN("NValFlt", 0.0)

# PK - then add weights to edges already created

for (src, dst) in weights.keys() :
  prw3.AddWEdge(graph, src, dst, weights[(src, dst)])
  
# PK - Here you had zero edges... that why PR just returned immediately
print " graph nodes and edges ", graph.GetNodes(), graph.GetEdges()

print "Getting page rank"
prw3.GetPageRankPy_w(graph)

# PK - I guess you no longer need to read this file...

file = open('pagerank_no_title.txt', 'rU') 
reader = csv.reader(file, dialect='excel')
for list in reader :
  id = int(list[0])
  rank = float(list[1])
  prReputations[id] = rank
file.close()

##############################
#### HOW MANY SWAPS & PERMS ##
##############################

print "Sorting Stack Overflow array (%d elems)" % len(soReputations)
sortedSO = sorted(soReputations, key=lambda l: soReputations[l], reverse=True)

print "Sorting Page Rank array (%d elems)" % len(prReputations)
sortedPR = sorted(prReputations, key=lambda l: prReputations[l], reverse=True)

soHashMap = {}
for i in xrange(len(sortedSO)):
  soHashMap[sortedSO[i]] = i
prHashMap = {}
for i in xrange(len(sortedPR)):
  prHashMap[sortedPR[i]] = i

outOfOrder = []

for i in range(len(sortedPR)):
  outOfOrder.append(soHashMap[sortedPR[i]])

print "Computing differences between the two rankings"
# decompose the permutation into disjoint cycles
nswaps = 0
seen = set()
numElems = len(outOfOrder)
for i in xrange(numElems):
  if i not in seen:           
    j = i # begin new cycle that starts with 'i'
    while outOfOrder[j] != i: # (i o(i) o(o(i)) ...)
      j = outOfOrder[j]
      seen.add(j)
      nswaps += 1

print "Number of swaps between two rankings : %d (%d elements)" % (nswaps, len(outOfOrder))

##########################
## HOW RANKINGS FARED
##########################


def numWrongRankings (rankingHashMap) :
  numWrong = 0
  numRight = 0
  for question in questions.keys():
    questionSort = sorted(questions[question], key=lambda l : questions[question][l], reverse=True)
    good = True
    for i in xrange(1,len(questionSort)):
      if rankingHashMap[questionSort[i]] < rankingHashMap[questionSort[0]]:
        good = False
        break
    if good:
      numRight += 1
    else :
      numWrong += 1
    #for i in xrange(len(questionSort)):
    #  for j in xrange(i):
    #    if rankingHashMap[questionSort[j]] <= rankingHashMap[questionSort[i]] :
    #      numRight += 1
    #    else :
    #      numWrong += 1
  return (numWrong, numRight)

(wrongSo, rightSo) = numWrongRankings(soHashMap)
print "SO's ranking had %d rights %d wrongs" % (rightSo, wrongSo)
(wrongPr, rightPr) = numWrongRankings(prHashMap)
print "PR's ranking had %d rights %d wrongs" % (rightPr, wrongPr)
