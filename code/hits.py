#! /usr/bin/env python

###########################
# HITS IMPLEMENTATION
# @author xfalco
###########################

import snap
import time
from math import fabs,sqrt

def init(graph, users, hubs, authorities, verbose):
  NUM_QUESTIONS = len(graph)
  initHub = 1.0 / sqrt(NUM_QUESTIONS)
  for questionId in graph:
    hubs[questionId] = initHub
    for userId in graph[questionId]:
      if not userId in users:
        users[userId] = {}
      users[userId][questionId] = graph[questionId][userId]
  NUM_USERS = len(users)
  initAuthority = 1.0 / sqrt(NUM_USERS)
  for userId in users:
    authorities[userId] = initAuthority
  if verbose:
    print "Done initializing: %d users, %d questions" % (NUM_USERS, NUM_QUESTIONS)

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
  for userId in users:
    weight = 0.0
    for questionId in users[userId]:
      weight += users[userId][questionId] * hubs[questionId]
    newAuthorities[userId] = weight
  # do new hubs
  for questionId in graph:
    weight = 0.0
    for userId in graph[questionId]:
      weight += graph[questionId][userId] * authorities[userId]
    newHubs[questionId] = weight
  # normalize
  sumAuthorities = sum(newAuthorities.values())
  sumHubs = sum(newHubs.values())
  if verbose:
    print "Pre-normalization sums: %f authorities, %f hubs" % (sumAuthorities, sumHubs)
  for userId in newAuthorities:
    authorities[userId] = newAuthorities[userId] / sumAuthorities
  for questionId in newHubs:
    hubs[questionId] = newHubs[questionId] / sumHubs

#
# returns a python dictionary of nodeIds to rankings
# PARAMS:
#   graph: a dictionary object where keys are question Ids and
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


