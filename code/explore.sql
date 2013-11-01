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


-- UserIDs and names of people in Question 613183 
SELECT  CASE WHEN b.Name = 'Question'
             THEN a.Id
             ELSE a.ParentId
        END AS QuestionId,
        b.Name AS PostType,
        a.Score,
        a.Tags,
        a.OwnerUserId,
        c.DisplayName
FROM    Posts a,
        PostTypes b,
        Users c
WHERE   a.PostTypeId = b.Id
AND     a.OwnerUserId = c.Id
AND     (a.Id = 613183 OR a.ParentId = 613183)
ORDER BY b.Name DESC, a.Score DESC;


-- Network of people in Question 613183
-- Edge attributes = (TotalVote)
WITH tblQuestionUsers (QuestionId, PostType, Score, Tags, OwnerUserId, DisplayName) AS
(
SELECT  CASE WHEN b.Name = 'Question'
             THEN a.Id
             ELSE a.ParentId
        END AS QuestionId,
        b.Name AS PostType,
        a.Score,
        a.Tags,
        a.OwnerUserId,
        c.DisplayName
FROM    Posts a,
        PostTypes b,
        Users c
WHERE   a.PostTypeId = b.Id
AND     a.OwnerUserId = c.Id
AND     (a.Id = 613183 OR a.ParentId = 613183)
)
SELECT  a.QuestionId,
        a.OwnerUserId AS SrcNodeId,
        b.OwnerUserId AS DstNodeId,
        a.Score AS TotalVote
FROM    (
        SELECT  a.QuestionId,
                a.OwnerUserId,
                a.Score
        FROM    tblQuestionUsers a
        WHERE   a.PostType = 'Answer'
        ) AS a,
        (
        SELECT  a.QuestionId,
                a.OwnerUserId
        FROM    tblQuestionUsers a
        WHERE   a.PostType = 'Question'
        ) AS b
WHERE   a.QuestionId = b.QuestionId
ORDER BY TotalVote DESC;


-- Up/down votes for questions and answers in Question 613183 (not scalable)
WITH tblVotes (PostType, QuestionId, AnswerId, VoteType, NumVotes) AS 
(
SELECT  CAST('Answer' AS NVARCHAR(50)),
        c.ParentId AS QuestionId,
        c.Id AS AnswerId,
        b.Name AS VoteType,
        COUNT(*) AS NumVotes
FROM    Votes a,
        VoteTypes b,
        Posts c,
        PostTypes d
WHERE   a.VoteTypeId = b.Id
AND     a.PostId = c.Id
AND     c.PostTypeId = d.Id
AND     c.ParentId = 613183
AND     d.Name = 'Answer'
GROUP BY c.ParentId, c.Id, b.Name
UNION ALL
SELECT  'Question',
        a.PostId AS QuestionId,
        a.PostId,
        b.Name AS VoteType,
        COUNT(*) AS NumVotes
FROM    Votes a,
        VoteTypes b
WHERE   a.VoteTypeId = b.Id
AND     a.PostId = 613183
GROUP BY a.PostId, b.Name
)
SELECT  a.PostType,
        a.QuestionId,
        a.AnswerId,
        a.NumVotes AS UpVote,
        COALESCE(b.NumVotes,0) AS DownVote,
        a.NumVotes - COALESCE(b.NumVotes,0) AS Score
FROM    (
        SELECT  *
        FROM    tblVotes a
        WHERE   a.VoteType = 'UpMod'
        ) a LEFT JOIN
        (
        SELECT  *
        FROM    tblVotes a
        WHERE   a.VoteType = 'DownMod'
        ) b ON a.AnswerId = b.AnswerId
ORDER BY PostType DESC, Score DESC;


-- Multiple WITH is supported!!! YAY!!!
WITH 
tblOne (a) AS 
(
SELECT 1
),
tblTwo (b) AS 
(
SELECT 2
)
SELECT  a.a,
        b.b
FROM    tblOne a,
        tblTwo b;


--------------------------------------------------------------------------------
-- Build network with filter
--------------------------------------------------------------------------------

-- Monthly statistics to decide filter for programming language and date range
SELECT  a.TagName,
        a.CreationYear,
        a.CreationMonth,
        COUNT(*) AS NumQuestions,
        SUM(a.AnswerCount) AS SumAnswerCount,
        AVG(CAST(a.AnswerCount AS DOUBLE PRECISION)) AS AvgAnswerCount,
        STDEV(CAST(a.AnswerCount AS DOUBLE PRECISION)) AS StdevAnswerCount
FROM    (
        SELECT  b.TagName,
                YEAR(c.CreationDate) AS CreationYear,
                MONTH(c.CreationDate) AS CreationMonth,
                c.*
        FROM    PostTags a,
                Tags b,
                Posts c
        WHERE   a.TagId = b.Id
        AND     b.TagName IN ('python', 'c++', 'ios', 'sql', 'linux')
        AND     a.PostId = c.Id
        ) a
GROUP BY a.TagName, a.CreationYear, a.CreationMonth
ORDER BY 1,2,3;

-- filter = (tag = python, question date = 2009 Mar)

-- Questions: up/down votes, reputation
SELECT  a.Id,
        a.OwnerUserId,
        SUM(CASE WHEN b.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVotes,
        SUM(CASE WHEN b.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVotes,
        a.Reputation
FROM    (
        SELECT  a.*,
                e.Reputation
        FROM    Posts a,
                PostTypes b,
                PostTags c,
                Tags d,
                Users e
        WHERE   a.PostTypeId = b.Id
        AND     a.Id = c.PostId
        AND     c.TagId = d.Id
        AND     a.OwnerUserId = e.Id
        AND     b.Name = 'Question'
        AND     d.TagName IN ('python')
        AND     a.CreationDate BETWEEN '2009-03-01' AND '2009-03-31'
        ) a LEFT JOIN
        Votes b
        ON a.Id = b.PostId
GROUP BY a.Id, a.OwnerUserId, a.Reputation
ORDER BY 1;


-- Answers: up/down votes, reputation
SELECT  a.Id,
        a.ParentId,
        a.OwnerUserId,
        SUM(CASE WHEN b.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVotes,
        SUM(CASE WHEN b.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVotes,
        a.Reputation
FROM    (
        SELECT  a.*,
                f.Reputation
        FROM    Posts a,
                PostTypes b,
                PostTags c,
                Tags d,
                Posts e,
                Users f
        WHERE   a.PostTypeId = b.Id
        AND     a.ParentId = c.PostId
        AND     c.TagId = d.Id
        AND     e.Id = a.ParentId
        AND     a.OwnerUserId = f.Id
        AND     b.Name = 'Answer'
        AND     d.TagName IN ('python')
        AND     e.CreationDate BETWEEN '2009-03-01' AND '2013-03-31'
        ) a LEFT JOIN
        Votes b
        ON a.Id = b.PostId
GROUP BY a.Id, a.ParentId, a.OwnerUserId, a.Reputation
ORDER BY 1;


-- Network
WITH
tblQuestion (Id, OwnerUserId, UpVotes, DownVotes, Reputation) AS 
(
SELECT  a.Id,
        a.OwnerUserId,
        SUM(CASE WHEN b.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVotes,
        SUM(CASE WHEN b.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVotes,
        a.Reputation
FROM    (
        SELECT  a.*,
                e.Reputation
        FROM    Posts a,
                PostTypes b,
                PostTags c,
                Tags d,
                Users e
        WHERE   a.PostTypeId = b.Id
        AND     a.Id = c.PostId
        AND     c.TagId = d.Id
        AND     a.OwnerUserId = e.Id
        AND     b.Name = 'Question'
        AND     d.TagName IN ('python')
        AND     a.CreationDate BETWEEN '2009-03-01' AND '2009-03-31'
        ) a LEFT JOIN
        Votes b
        ON a.Id = b.PostId
GROUP BY a.Id, a.OwnerUserId, a.Reputation
),
tblAnswer (Id, ParentId, OwnerUserId, UpVotes, DownVotes, Reputation) AS 
(
SELECT  a.Id,
        a.ParentId,
        a.OwnerUserId,
        SUM(CASE WHEN b.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVotes,
        SUM(CASE WHEN b.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVotes,
        a.Reputation
FROM    (
        SELECT  a.*,
                f.Reputation
        FROM    Posts a,
                PostTypes b,
                PostTags c,
                Tags d,
                Posts e,
                Users f
        WHERE   a.PostTypeId = b.Id
        AND     a.ParentId = c.PostId
        AND     c.TagId = d.Id
        AND     e.Id = a.ParentId
        AND     a.OwnerUserId = f.Id
        AND     b.Name = 'Answer'
        AND     d.TagName IN ('python')
        AND     e.CreationDate BETWEEN '2009-03-01' AND '2009-03-31'
        ) a LEFT JOIN
        Votes b
        ON a.Id = b.PostId
GROUP BY a.Id, a.ParentId, a.OwnerUserId, a.Reputation
)
SELECT  a.QuestionId,
        a.SrcNodeId,
        a.DstNodeId,
        a.EdgeAttrUpVotes,
        a.EdgeAttrDownVotes,
        a.EdgeAttrSrcRep,
        a.EdgeAttrDstRep,
        b.Tags AS EdgeAttrTags
FROM    (
        SELECT  a.Id AS QuestionId,
                a.OwnerUserId AS SrcNodeId,
                b.OwnerUserId AS DstNodeId,
                b.UpVotes AS EdgeAttrUpVotes,
                b.DownVotes AS EdgeAttrDownVotes,
                a.Reputation AS EdgeAttrSrcRep,
                b.Reputation AS EdgeAttrDstRep
        FROM    tblQuestion a,
                tblAnswer b
        WHERE   a.Id = b.ParentId
        ) a,
        Posts b
WHERE   a.QuestionId = b.Id 
-- AND     a.QuestionId = 613183  -- DEBUG 1
-- AND     a.DstNodeId = 2786  -- DEBUG 2
ORDER BY a.SrcNodeId, a.DstNodeId;










