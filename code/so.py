# core code for Stack Overflow data analysis
# mostly includes iterators ...
# @author xfalco

# CONSTANTS
class CONSTANTS:

  # POST HISTORY TYPES
  INITIAL_TITLE = 1
  INITIAL_BODY = 2
  INITIAL_TAGS = 3
  EDIT_TILE = 4
  EDIT_BODY = 5
  EDIT_TAGS = 6
  ROLLBACK_TITLE = 7
  ROLLBACK_BODY = 8
  ROLLBACK_TAGS = 9
  POST_CLOSED = 10
  POST_REOPENED = 11
  POST_DELETED = 12
  POST_UNDELETED = 13
  POST_LOCKED = 14
  POST_UNLOCKED = 15
  COMMUNITY_OWNED = 16
  POST_MIGRATED = 17
  QUESTION_MERGED = 18
  QUESTION_PROTECTED = 19
  QUESTION_UNPROTECTED = 20
  QUESTION_UNMERGED = 22
  SUGGESTED_EDIT_APPLIED = 24
  POST_TWEETED = 25
  DISCUSSION_MOVED_TO_CHAT = 31
  POST_NOTICE_ADDED = 33
  POST_NOTICE_REMOVED = 34
  POST_MIGRATED_AWAY = 35
  POST_MIGRATED_HERE = 36
  POST_MERGE_SROUCE = 37
  POST_MERGE_DESTINATION = 38

  # POST TYPES
  QUESTION = 1
  ANSWER = 2
  WIKI = 3
  TAG_WIKI_EXCERPT = 4
  TAG_WIKI = 5
  MODERATOR_NOMINATION = 6
  WIKI_PLACEHOLDER = 7
  PRIVILEGE_WIKI = 8

  # VOTE TYPES
  ACCEPTED_BY_ORIGINATOR = 1
  UP_MOD = 2
  DOWN_MOD = 3
  OFFENSIVE = 4
  FAVORITE = 5
  CLOSE = 6
  REOPEN = 7
  BOUNTY_START = 8
  BOUNTY_CLOSE = 9
  DELETION = 10
  UNDELETION = 11
  SPAM = 12
  MODERATOR_REVIEW = 15
  APPROVE_EDIT_SUGGESTION = 16

# file iteration
class FileIterator :
  def __init__(self, filename) :
    self.f = filename

  def iterate(self, fnToCreateObjectFromArr) :
    file = open(self.f)
    # read first line to ignore headers
    file.readline()
    for line in file :
      arr = line.split(',')
      yield fnToCreateObjectFromArr(arr)
    file.close()

# post iteration
class PostIterator(FileIterator) :
  def __init__(self) :
    FileIterator.__init__(self, "../data/posts.csv")
  
  def createPost(self, arr) :
    return Post(arr)

  def __iter__(self) :
    return iter(self.iterate(self.createPost))

# user iteration
class UserIterator(FileIterator) :
  def __init__(self) :
    FileIterator.__init__(self, "../data/users.csv")
  
  def createUser(self, arr) :
    return User(arr)

  def __iter__(self) :
    return iter(self.iterate(self.createUser))


class Post :
  def __init__(self, arr) :
    self.id = arr[0]
    self.postTypeId = arr[1]
    self.acceptedAnswerId = arr[2]
    self.parentId = arr[3]
    self.creationDate = arr[4]
    self.score = arr[5]
    self.viewCount = arr[6]
    self.body = arr[7]
    self.ownerUserId = arr[8]
    self.ownerDisplayName = arr[9]
    self.lastEditorUserId = arr[10]
    self.lastEditorDisplayName = arr[11]
    self.lastEditDate = arr[12]
    self.lastActivityDate = arr[13]
    self.title = arr[14]
    self.tags = arr[15]
    self.answerCount = arr[16]
    self.commentCount = arr[17]
    self.favoriteCount = arr[18]
    self.closedDate = arr[19]
    self.communityOwnedDate = arr[20]

class User :
  def __init__(self, arr) :
    self.id = arr[0]
    self.reputation = arr[1]
    self.creationDate = arr[2]
    self.displayName = arr[3]
    self.lastAccessDate = arr[4]
    self.websiteUrl = arr[5]
    self.location = arr[6]
    self.aboutMe = arr[7]
    self.views = arr[8]
    self.upVotes = arr[9]
    self.downVotes = arr[10]
    self.profileImageUrl = arr[11]
    self.emailHash = arr[12]
    self.age = arr[13]
