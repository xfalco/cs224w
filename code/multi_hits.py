#! /usr/bin/env python

###########################
# HITS IMPLEMENTATION
# @author xfalco
###########################

import snap
import time
from math import fabs,sqrt

def init(graph, users, hubs, authorities, verbose):
  NUM_QUESTIONER = len(graph)
  initHub = 1.0 / sqrt(NUM_QUESTIONER)
  for userId in graph:
    hubs[userId] = initHub
    for user in graph[userId]:
      if not user in users:
        users[user] = {}
      users[user][userId] = graph[userId][user]
  NUM_ANSWERER = len(users)
  initAuthority = 1.0 / sqrt(NUM_ANSWERER)
  for userId in users:
    authorities[userId] = initAuthority
  if verbose:
    print "Done initializing: %d questioner, %d answerer" % (NUM_QUESTIONER, NUM_ANSWERER)

def diff(authorities, oldAuthorities, verbose):
  diffW = 0.0
  numOldAuthorities = len(oldAuthorities)
  for userId in authorities:
    if not numOldAuthorities == 0:
      diffW += fabs(authorities[userId] - oldAuthorities[userId])
    else:
      diffW += authorities[userId]
    oldAuthorities[userId] = authorities[userId]
  return diffW
 
def doIteration(authorities, hubs, graph, users, verbose):
  newAuthorities = {}
  newHubs = {}
  # do new authorities
  for answerer in users:
    weight = 0.0
    for questioner in users[answerer]:
      weight += users[answerer][questioner] * hubs[questioner]
    newAuthorities[answerer] = weight
  # do new hubs
  for questioner in graph:
    weight = 0.0
    for answerer in graph[questioner]:
      weight += graph[questioner][answerer] * authorities[answerer]
    newHubs[questioner] = weight
  # normalize
  sumAuthorities = sum(newAuthorities.values())
  sumHubs = sum(newHubs.values())
  if verbose:
    print "Pre-normalization sums: %f authorities, %f hubs" % (sumAuthorities, sumHubs)
  for userId in newAuthorities:
    authorities[userId] = newAuthorities[userId] / sumAuthorities
  for userId in newHubs:
    hubs[userId] = newHubs[userId] / sumHubs

#
# returns a python dictionary of nodeIds to rankings
# PARAMS:
#   graph: a dictionary object where keys are user Ids and
#          values are dictionaries of user ids to weights
#   verbose: adds logging
#   Eps: when to stop iterating
# RETURNS:
#   a dictionary object of userIds to rankings
#
def calculateRankings(graph, verbose=True, Eps = 1e-4):
  users = {}
  hubs = {}
  authorities = {}
  oldAuthorities = {}
  init(graph, users, hubs, authorities, verbose)
  numIteration = 0 
  diffW = diff(authorities, oldAuthorities, verbose)
  while(diffW > Eps):
    if verbose:
      print "(Iteration %d): %f diff" % (numIteration, diffW)
    doIteration(authorities, hubs, graph, users, verbose)
    diffW = diff(authorities, oldAuthorities, verbose)
  return authorities

