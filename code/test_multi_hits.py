# tests efficiency from graph passed in as first parameter
# uses "../data/network_python.graph" if none passed in
# @author xfalco

import sys
import multi_hits
import csv
from sets import Set
import sys

if len(sys.argv) is 1 :
   filename = "../data/network_python.graph"
else :
   filename = sys.argv[1]


def func(eAttrUpVotes, eAttrDownVotes):
  if eAttrDownVotes >= eAttrUpVotes:
    return 0.0
  return eAttrUpVotes - eAttrDownVotes

#
# LOAD FILE
#

graph = {}
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
  if not srcNId in graph:
    graph[srcNId] = {}
  graph[srcNId][dstNId] = func(eAttrUpVotes, eAttrDownVotes) 
file.close()

#
# SAVE RANKINGS
#

rankings = multi_hits.calculateRankings(graph)

f = open("../data/hits_multi_net.txt","w")
f.write("userId,hits ranking")
for n in rankings:
  buf = str(n) + "," + str(rankings[n])
  f.write (buf)
  f.write("\n")
