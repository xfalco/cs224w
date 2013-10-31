/*
-- Number of posts per day
WITH tblPosts (Id, CreationDate) AS
(
SELECT  a.Id,
        CAST(a.CreationDate AS DATE)
FROM    Posts a
--WHERE   a.CreationDate BETWEEN '2008-08-01' AND '2008-08-10'
)
SELECT  a.CreationDate,
        COUNT(a.Id)
FROM    tblPosts a
GROUP BY a.CreationDate
ORDER BY 1;
*/


/*
-- Number of each PostType per day
WITH tblPosts (Id, CreationDate, PostType) AS
(
SELECT  a.Id,
        CAST(a.CreationDate AS DATE),
        b.Name
FROM    Posts a,
        PostTypes b
WHERE   a.PostTypeId = b.Id
)
SELECT  a.CreationDate,
        a.PostType,
        COUNT(a.Id)
FROM    tblPosts a
GROUP BY a.CreationDate, a.PostType
ORDER BY 1,2;
*/


-- Mimic the following post:
-- http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
SELECT  b.Name AS PostType,
        a.Score AS PostScore,
        a.Tags AS PostTags,
        a.Body AS PostBody,
        c.Score AS CommentScore,
        c.Text AS CommentText
        --,c.*
FROM    Posts a,
        PostTypes b,
        Comments c
WHERE   a.PostTypeId = b.Id
AND     a.Id = c.PostId
AND     (a.Id = 613183 OR a.ParentId = 613183)
ORDER BY b.Name DESC, a.Score DESC, c.Score DESC;


-- Votes on Question
SELECT  b.Name,
        COUNT(*)
FROM    Votes a,
        VoteTypes b
WHERE   a.VoteTypeId = b.Id
AND     a.PostId = 613183
GROUP BY b.Name;


-- Votes on Answers
WITH tblVoteAnswer (PostId, PostScore, VoteType, NumVotes) AS
(
SELECT  c.Id,
        c.Score,
        b.Name,
        COUNT(*)
FROM    Votes a,
        VoteTypes b,
        Posts c,
        PostTypes d
WHERE   a.VoteTypeId = b.Id
AND     a.PostId = c.Id
AND     c.PostTypeId = d.Id
AND     c.ParentId = 613183
AND     d.Name = 'Answer'
GROUP BY b.Name, c.Id, c.Score
)
SELECT  a.PostId,
        a.NumVotes - COALESCE(b.NumVotes,0) AS Score
FROM    (
        SELECT  PostId, NumVotes
        FROM    tblVoteAnswer
        WHERE   VoteType = 'UpMod'
        ) a LEFT JOIN
        (
        SELECT  PostId, NumVotes
        FROM    tblVoteAnswer
        WHERE   VoteType = 'DownMod'
        ) b
        ON   a.PostId = b.PostId
ORDER BY 2 DESC;


-- Stack Overflow does not provide the userid of up/down votes
SELECT  *
FROM    Votes
WHERE   PostId = 613218;   -- answer

/*
WITH tblVoteAnswer (PostId, PostScore, OwnerUserId, VoteType, NumVotes) AS
(
SELECT  c.Id,
        c.Score,
        c.OwnerUserId,
        b.Name,
        COUNT(*)
FROM    Votes a,
        VoteTypes b,
        Posts c,
        PostTypes d
WHERE   a.VoteTypeId = b.Id
AND     a.PostId = c.Id
AND     c.PostTypeId = d.Id
AND     c.ParentId = 613183
AND     d.Name = 'Answer'
GROUP BY b.Name, c.Id, c.Score, c.OwnerUserId
)
SELECT  a.PostId,
        a.OwnerUserId,
        a.NumVotes - COALESCE(b.NumVotes,0) AS Score,
        CASE WHEN (a.NumVotes + COALESCE(b.NumVotes,0)) > 0
             THEN CAST(a.NumVotes AS DOUBLE PRECISION) / (a.NumVotes + COALESCE(b.NumVotes,0))
             ELSE 0
        END AS PosEval

FROM    (
        SELECT  PostId, OwnerUserId, NumVotes
        FROM    tblVoteAnswer
        WHERE   VoteType = 'UpMod'
        ) a LEFT JOIN
        (
        SELECT  PostId, OwnerUserId, NumVotes
        FROM    tblVoteAnswer
        WHERE   VoteType = 'DownMod'
        ) b
        ON   a.PostId = b.PostId
ORDER BY Score DESC;
*/