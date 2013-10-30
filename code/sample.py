from so import *
import matplotlib.pyplot as plt
from math import log
import snap

graph = snap.TNEANet.New()

userIterator = UserIterator()
for user in userIterator :
  graph.AddNode(user.id)

### SUPER_USER
SUPER_USER_ID=-999
graph.AddNode(SUPER_USER_ID)

for user in userIterator :
  # -1 doesn't register as a node...
  if not user.id is -1 :
    graph.AddEdge(user.id, SUPER_USER_ID)

postIterator = PostIterator()
for post in postIterator :
  owner = post.ownerUserId
  # data is unsanitized - some post owner ids
  # don't actually map back to users
  if not graph.IsNode(owner):
    continue
  if post.score > 0 :
    for i in range(0,post.score) :
      graph.AddEdge(SUPER_USER_ID, owner)


print "%d edges, %d nodes" % (graph.GetEdges(), graph.GetNodes())

rankings = []
numbers = []
PRankH = snap.TIntFltH()
snap.GetPageRank(graph, PRankH)
num = 1
for item in PRankH:
  numbers.append(log(num))
  rankings.append(log(item.GetDat()))
  num += 1

# sort
rankings.sort()

NUMS_TO_SHOW = 1000

plt.plot(numbers[-NUMS_TO_SHOW:],rankings[-NUMS_TO_SHOW:],'r--')
plt.show()
