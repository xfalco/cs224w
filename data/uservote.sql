-- Validation using user = 'Devin Jeanpierre'
-- UpVotes = 552, DownVotes = 180
SELECT  a.*
FROM    Users a
WHERE   a.Id IN (18515);


-- List of people who posted in python
-- For each user, separate votes earned inside/outside python
-- Reputation in python = Reputation in python * (net votes in python / net votes) 
-- Put these ratios in revised network graph for each post!!!

-- http://stackoverflow.com/users/18515/devin-jeanpierre?tab=answers (147)
-- http://stackoverflow.com/users/18515/devin-jeanpierre?tab=questions (13)


-- Number of posts by Devin Jeanpierre (160)
SELECT  COUNT(*)
FROM    Posts a
WHERE   a.OwnerUserId = 18515;

-- Number of python posts by Devin Jeanpierre (8)
SELECT  a.*
FROM    Posts a,
        PostTags b,
        Tags c
WHERE   a.Id = b.PostId AND b.TagId = c.Id
AND     c.TagName = 'python'
AND     a.OwnerUserId = 18515;


-- Up/down votes related to python for Devin Jeanpierre
SELECT  SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVote,
        SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVote
FROM    Posts a,
        PostTags b,
        Tags c,
        Votes d
WHERE   a.Id = b.PostId AND b.TagId = c.Id
AND     a.Id = d.PostId
AND     c.TagName = 'python'
AND     a.OwnerUserId = 18515;


-- Running sum of votes of (all, tag = python)
SELECT  d.CreationDate AS VoteCreationDate,
        SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS UpVote_All,
        SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS DownVote_All,
        SUM(CASE WHEN (d.VoteTypeId = 2 AND c.TagName IN ('python')) THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS UpVote_Python,
        SUM(CASE WHEN (d.VoteTypeId = 3 AND c.TagName IN ('python')) THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS DownVote_Python
FROM    Posts a,
        PostTags b,
        Tags c,
        Votes d
WHERE   a.Id = b.PostId AND b.TagId = c.Id
AND     a.Id = d.PostId
AND     a.OwnerUserId = 18515
ORDER BY d.CreationDate;


-- Running ratio of python votes per user
SELECT  a.OwnerUserId,
        a.CreationDate,
        (CAST (a.UpVote_Python AS DOUBLE PRECISION) - CAST (a.DownVote_Python AS DOUBLE PRECISION)) / (a.UpVote_All - a.DownVote_All) AS Ratio_Python
FROM    (
        SELECT  a.OwnerUserId,
                d.CreationDate,
                SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS UpVote_All,
                SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS DownVote_All,
                SUM(CASE WHEN (d.VoteTypeId = 2 AND c.TagName IN ('python')) THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS UpVote_Python,
                SUM(CASE WHEN (d.VoteTypeId = 3 AND c.TagName IN ('python')) THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS DownVote_Python
        FROM    Posts a,
                PostTags b,
                Tags c,
                Votes d
        WHERE   a.Id = b.PostId AND b.TagId = c.Id
        AND     a.Id = d.PostId
        AND     a.OwnerUserId = 18515
        ) a
ORDER BY a.OwnerUserId, a.CreationDate;


-- Number of distinct python users (79677)
SELECT  COUNT (DISTINCT a.OwnerUserId),  -- 79677
        AVG(CAST(a.OwnerUserId AS DOUBLE PRECISION)),  -- 1014521.4835842226
        MIN(a.OwnerUserId), -- 25
        MAX(a.OwnerUserId) -- 2949246
FROM    Posts a,
        PostTags b,
        Tags c
WHERE   a.Id = b.PostId AND b.TagId = c.Id
AND     c.TagName = 'python';


SELECT  DISTINCT a.OwnerUserId, 
FROM    Posts a,
        PostTags b,
        Tags c
WHERE   a.Id = b.PostId AND b.TagId = c.Id
AND     c.TagName = 'python'
AND     a.OwnerUserId <= 1014521;  -- count = 37574 
--AND     a.OwnerUserId > 1014521; -- count = 42103 


-- Create batches of users cumulative votes over time
SELECT  a.OwnerUserId,
        SUM(a.NumVotes) OVER (ORDER BY a.OwnerUserId ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS CumulativeVotes
FROM    (
        SELECT  a.OwnerUserId,
                --SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVote,
                --SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVote
                SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) + SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) AS NumVotes
        FROM    Posts a,
                PostTags b,
                Tags c,
                Votes d
        WHERE   a.Id = b.PostId AND b.TagId = c.Id
        AND     a.Id = d.PostId
        AND     c.TagName = 'python'
        --AND     a.OwnerUserId BETWEEN 25 AND 7891 -- 40004 votes
        AND     a.OwnerUserId > 0
        GROUP BY a.OwnerUserId
        ) a
ORDER BY 1;


-- Running ratio of python votes for user = 18515
SELECT  a.OwnerUserId,
        a.CreationDate,
        (CAST (a.UpVote_Python AS DOUBLE PRECISION) - CAST (a.DownVote_Python AS DOUBLE PRECISION)) / (a.UpVote_All - a.DownVote_All) AS Ratio_Python
FROM    (
        SELECT  a.OwnerUserId,
                d.CreationDate,
                SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS UpVote_All,
                SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS DownVote_All,
                SUM(CASE WHEN (d.VoteTypeId = 2 AND c.TagName IN ('python')) THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS UpVote_Python,
                SUM(CASE WHEN (d.VoteTypeId = 3 AND c.TagName IN ('python')) THEN 1 ELSE 0 END) OVER (ORDER BY d.CreationDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS DownVote_Python
        FROM    Posts a,
                PostTags b,
                Tags c,
                Votes d
        WHERE   a.Id = b.PostId AND b.TagId = c.Id
        AND     a.Id = d.PostId
        AND     a.OwnerUserId = 18515
        ) a
ORDER BY a.OwnerUserId, a.CreationDate;


-- Ratio of python votes for user = 18515
SELECT  a.OwnerUserId,
        (CAST (a.UpVote_Python AS DOUBLE PRECISION) - CAST (a.DownVote_Python AS DOUBLE PRECISION)) / (a.UpVote_All - a.DownVote_All) AS Ratio_Python
FROM    (
        SELECT  a.OwnerUserId,
                SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVote_All,
                SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVote_All,
                SUM(CASE WHEN (d.VoteTypeId = 2 AND c.TagName IN ('python')) THEN 1 ELSE 0 END) AS UpVote_Python,
                SUM(CASE WHEN (d.VoteTypeId = 3 AND c.TagName IN ('python')) THEN 1 ELSE 0 END) AS DownVote_Python
        FROM    Posts a,
                PostTags b,
                Tags c,
                Votes d
        WHERE   a.Id = b.PostId AND b.TagId = c.Id
        AND     a.Id = d.PostId
        AND     a.OwnerUserId = 18515
        GROUP BY a.OwnerUserId
        ) a
ORDER BY a.OwnerUserId;


-- Create batches of users
SELECT  a.OwnerUserId,
        --SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVote,
        --SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVote
        SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) + SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) AS NumVotes
FROM    Posts a,
        PostTags b,
        Tags c,
        Votes d
WHERE   a.Id = b.PostId AND b.TagId = c.Id
AND     a.Id = d.PostId
AND     c.TagName = 'python'
--AND     a.OwnerUserId BETWEEN 0 AND 1800000  -- 49357 users
AND     a.OwnerUserId > 1800000  -- 16164 users
GROUP BY a.OwnerUserId
ORDER BY 1;


-- Ratio of python votes for batches of users
WITH tblPythonUsers (OwnerUserId, NumVotes) AS 
(
SELECT  a.OwnerUserId,
        --SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVote,
        --SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVote
        SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) + SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) AS NumVotes
FROM    Posts a,
        PostTags b,
        Tags c,
        Votes d
WHERE   a.Id = b.PostId AND b.TagId = c.Id
AND     a.Id = d.PostId
AND     c.TagName = 'python'
--AND     a.OwnerUserId BETWEEN 0 AND 1800000  -- 49357 users
AND     a.OwnerUserId > 1800000  -- 16164 users
GROUP BY a.OwnerUserId
)
SELECT  a.OwnerUserId,
        CASE WHEN a.UpVote_All = a.DownVote_All
             THEN 0
             ELSE (CAST (a.UpVote_Python AS DOUBLE PRECISION) - CAST (a.DownVote_Python AS DOUBLE PRECISION)) / (a.UpVote_All - a.DownVote_All)
             END AS VoteRatio_Python
FROM    (
        SELECT  a.OwnerUserId,
                SUM(CASE WHEN d.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVote_All,
                SUM(CASE WHEN d.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVote_All,
                SUM(CASE WHEN (d.VoteTypeId = 2 AND c.TagName IN ('python')) THEN 1 ELSE 0 END) AS UpVote_Python,
                SUM(CASE WHEN (d.VoteTypeId = 3 AND c.TagName IN ('python')) THEN 1 ELSE 0 END) AS DownVote_Python
        FROM    Posts a,
                PostTags b,
                Tags c,
                Votes d
        WHERE   a.Id = b.PostId AND b.TagId = c.Id
        AND     a.Id = d.PostId
        AND     a.OwnerUserId IN (SELECT OwnerUserId FROM tblPythonUsers)
        GROUP BY a.OwnerUserId
        ) a
ORDER BY a.OwnerUserId;
