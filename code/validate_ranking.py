# tests efficiency from graph passed in as first parameter
# uses "../data/network_python.graph" if none passed in
# @author xfalco

import snap
import prw3
import csv
from math import log

FILE_NETWORK = "../data/network_python.graph"
FILE_PR = "../data/pagerank_net.txt"
FILE_HITS = "../data/hits_net.txt"

#
# LOAD FILES
#
def loadFile(CUT_OFF_RANK) : 
  global soHashMap
  global prHashMap
  global hitsHashMap
  global questions
  questions = {}
  weights = {}
  soReputations = {}
  prReputations = {}
  hitsReputations = {}
  graph = snap.TNEANet.New()

  file = open(FILE_NETWORK, 'rU')
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
    net = eAttrUpVotes - eAttrDownVotes
    if net < CUT_OFF_RANK:
      continue
    soReputations[srcNId] = eAttrSrcRep
    soReputations[dstNId] = eAttrDstRep
    net = eAttrUpVotes - eAttrDownVotes
    if not eAttrQId in questions :
      questions[eAttrQId] = {}
    questions[eAttrQId][dstNId] = net
  file.close()
  
  file = open(FILE_PR, 'rU') 
  reader = csv.reader(file, dialect='excel')
  next(reader, None)
  for list in reader :
    id = int(list[0])
    if not id in soReputations:
      continue
    rank = float(list[1])
    prReputations[id] = rank
  file.close()

  file = open(FILE_HITS, 'rU')
  reader = csv.reader(file, dialect='excel')
  next(reader, None)
  for list in reader :
    id = int(list[0])
    if not id in soReputations:
      continue
    rank = float(list[1])
    hitsReputations[id] = rank
  file.close()
  
  sortedSO = sorted(soReputations, key=lambda l: soReputations[l], reverse=True)
  sortedPR = sorted(prReputations, key=lambda l: prReputations[l], reverse=True)
  sortedHits = sorted(hitsReputations, key=lambda l: hitsReputations[l], reverse=True)

  soHashMap = {}
  for i in xrange(len(sortedSO)):
    soHashMap[sortedSO[i]] = i
  prHashMap = {}
  for i in xrange(len(sortedPR)):
    prHashMap[sortedPR[i]] = i
  hitsHashMap = {}
  for i in xrange(len(sortedHits)):
    hitsHashMap[sortedHits[i]] = i

##########################
## HOW RANKINGS FARED
##########################


def numRightTopAnswers (rankingHashMap) :
  numWrong = 0
  numRight = 0
  for question in questions.keys():
    questionSort = sorted(questions[question], key=lambda l : questions[question][l], reverse=True)
    good = True
    if len(questionSort) <= 1:
      continue
    for i in xrange(1,len(questionSort)):
      if not questionSort[i] in rankingHashMap:
          continue
      if not questionSort[0] in rankingHashMap:
          continue
      if rankingHashMap[questionSort[i]] < rankingHashMap[questionSort[0]]:
        good = False
        break
    if good:
      numRight += 1
    else :
      numWrong += 1
  return (numWrong, numRight)


def numRightRankings (rankingHashMap) :
  numWrong = 0
  numRight = 0
  for question in questions.keys():
    questionSort = sorted(questions[question], key=lambda l : questions[question][l], reverse=True)
    good = True
    if len(questionSort) <= 1:
      continue
    for i in xrange(len(questionSort)):
      for j in xrange(i):
        if not questionSort[j] in rankingHashMap:
          continue
        if not questionSort[i] in rankingHashMap:
          continue
        if rankingHashMap[questionSort[j]] <= rankingHashMap[questionSort[i]] :
          numRight += 1
        else :
          numWrong += 1
  return (numWrong, numRight)

RIGHT_TOP = 'right_top'
RIGHT_RANKS = 'right_ranks'

def loadAndTest(CUT_OFF_RANK):
  print "testing with cutoff", CUT_OFF_RANK
  loadFile(CUT_OFF_RANK)
  results[CUT_OFF_RANK] = {RIGHT_TOP: {}, RIGHT_RANKS: {}}
  rightTop = results[CUT_OFF_RANK][RIGHT_TOP]
  rightRanks = results[CUT_OFF_RANK][RIGHT_RANKS]
  (wrongSo, rightSo) = numRightTopAnswers(soHashMap)
  rightTop['percso'] = float(rightSo) * 100 / (rightSo + wrongSo)
  rightTop['numso'] = float(rightSo + wrongSo)
  (wrongSo, rightSo) = numRightTopAnswers(prHashMap)
  rightTop['percpr'] = float(rightSo) * 100 / (rightSo + wrongSo)
  rightTop['numpr'] = float(rightSo + wrongSo)
  (wrongSo, rightSo) = numRightTopAnswers(hitsHashMap)
  rightTop['perchits'] = float(rightSo) * 100 / (rightSo + wrongSo)
  rightTop['numhits'] = float(rightSo + wrongSo)
  
  (wrongSo, rightSo) = numRightRankings(soHashMap)
  rightRanks['percso'] = float(rightSo) * 100 / float(rightSo + wrongSo)
  rightRanks['numso'] = float(rightSo + wrongSo)
  (wrongSo, rightSo) = numRightRankings(prHashMap)
  rightRanks['percpr'] = float(rightSo) * 100 / float(rightSo + wrongSo)
  rightRanks['numpr'] = float(rightSo + wrongSo)
  (wrongSo, rightSo) = numRightRankings(hitsHashMap)
  rightRanks['perchits'] = float(rightSo) * 100 / float(rightSo + wrongSo)
  rightRanks['numhits'] = float(rightSo + wrongSo)

results = {}
for CUT_OFF in range(1, 92, 5):
  loadAndTest(CUT_OFF)
print "========================================================================================================="
print "\t| top answer % \t\t| top answer # \t\t| all answers %\t\t| all answers #\t\t|"
print "cut off\t| SO\t| PR\t| HITS\t| SO\t| PR\t| HITS\t| SO\t| PR\t| HITS\t| SO\t| PR\t| HITS\t|"
print "---------------------------------------------------------------------------------------------------------"
for rank in sorted(results):
  meth1 = results[rank][RIGHT_TOP]
  meth2 = results[rank][RIGHT_RANKS]
  print "%d\t| %.2f\t| %.2f\t| %.2f\t|%.0f\t|%.0f\t|%.0f\t| %.2f\t| %.2f\t| %.2f\t|%.0f\t|%.0f\t|%.0f\t|" % (rank, meth1['percso'], meth1['percpr'],meth1['perchits'], meth1['numso'], meth1['numpr'], meth1['numhits'], meth2['percso'], meth2['percpr'], meth2['perchits'], meth2['numso'], meth2['numpr'], meth2['numhits'])
