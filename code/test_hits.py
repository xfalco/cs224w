# tests efficiency from graph passed in as first parameter
# uses "../data/network_python.graph" if none passed in
# @author xfalco

import sys
import hits
import csv

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

questions = {}
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
  if not eAttrQId in questions:
    questions[eAttrQId] = {}
  questions[eAttrQId][dstNId] = func(eAttrUpVotes, eAttrDownVotes) 
file.close()

#
# SAVE RANKINGS
#

rankings = hits.calculateRankings(questions)

f = open("../data/hits_net.txt","w")
f.write("userId,hits ranking")
for n in rankings:
  buf = str(n) + "," + str(rankings[n])
  f.write (buf)
  f.write("\n")
