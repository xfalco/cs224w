-- Python votes for answers
SELECT  a.OwnerUserId, --a.ParentId,
        SUM(CASE WHEN d.VoteTypeId = 2 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS UpVote,
        SUM(CASE WHEN d.VoteTypeId = 3 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS DownVote
FROM    Posts a,
        PostTags b,
        Tags c,
        Votes d
WHERE   a.ParentId = b.PostId AND b.TagId = c.Id
AND     a.Id = d.PostId
AND     a.OwnerUserId IN (25, 700820, 18515)
GROUP BY a.OwnerUserId--, a.ParentId
ORDER BY 1,2;


-- Python votes for questions
SELECT  a.OwnerUserId,
        SUM(CASE WHEN d.VoteTypeId = 2 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS UpVote,
        SUM(CASE WHEN d.VoteTypeId = 3 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS DownVote
FROM    Posts a,
        PostTags b,
        Tags c,
        Votes d
WHERE   a.Id = b.PostId AND b.TagId = c.Id
AND     a.Id = d.PostId
AND     a.OwnerUserId IN (25, 700820, 18515)
GROUP BY a.OwnerUserId
ORDER BY 1,2;


-- Total votes
SELECT  a.OwnerUserId,
        SUM(CASE WHEN b.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVote_All,
        SUM(CASE WHEN b.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVote_All
FROM    Posts a,
        Votes b
WHERE   a.Id = b.PostId
AND     a.OwnerUserId IN (25, 700820, 18515)
GROUP BY a.OwnerUserId
ORDER BY 1;

-------------------------------------------------------------

WITH
tblPythonAnswerVotes (OwnerUserId, UpVote, DownVote) AS
(
SELECT  a.OwnerUserId,
        SUM(CASE WHEN d.VoteTypeId = 2 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS UpVote,
        SUM(CASE WHEN d.VoteTypeId = 3 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS DownVote
FROM    Posts a,
        PostTags b,
        Tags c,
        Votes d
WHERE   a.ParentId = b.PostId AND b.TagId = c.Id
AND     a.Id = d.PostId
AND     a.OwnerUserId IN (25, 700820, 18515)
GROUP BY a.OwnerUserId
),
tblPythonQuestionVotes (OwnerUserId, UpVote, DownVote) AS
(
SELECT  a.OwnerUserId,
        SUM(CASE WHEN d.VoteTypeId = 2 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS UpVote,
        SUM(CASE WHEN d.VoteTypeId = 3 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS DownVote
FROM    Posts a,
        PostTags b,
        Tags c,
        Votes d
WHERE   a.Id = b.PostId AND b.TagId = c.Id
AND     a.Id = d.PostId
AND     a.OwnerUserId IN (25, 700820, 18515)
GROUP BY a.OwnerUserId
),
tblTotalVotes (OwnerUserId, UpVote, DownVote) AS
(
SELECT  a.OwnerUserId,
        SUM(CASE WHEN b.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVote,
        SUM(CASE WHEN b.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVote
FROM    Posts a,
        Votes b
WHERE   a.Id = b.PostId
AND     a.OwnerUserId IN (25, 700820, 18515)
GROUP BY a.OwnerUserId
)
SELECT  a.OwnerUserId,
        CAST((COALESCE(b.UpVote,0) + COALESCE(c.UpVote,0) - COALESCE(b.DownVote,0) - COALESCE(c.DownVote,0)) AS DOUBLE PRECISION) / (a.UpVote - a.DownVote)
FROM    tblTotalVotes a LEFT JOIN tblPythonAnswerVotes b ON a.OwnerUserId = b.OwnerUserId 
                        LEFT JOIN tblPythonQuestionVotes c ON a.OwnerUserId = c.OwnerUserId
ORDER BY 1;

-----------------------------------------------------------------------

DECLARE @MinUserId INT = 50000;
DECLARE @MaxUserId INT = 100000;

WITH
tblPythonAnswerVotes (OwnerUserId, UpVote, DownVote) AS
(
SELECT  a.OwnerUserId,
        SUM(CASE WHEN d.VoteTypeId = 2 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS UpVote,
        SUM(CASE WHEN d.VoteTypeId = 3 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS DownVote
FROM    Posts a,
        PostTags b,
        Tags c,
        Votes d
WHERE   a.ParentId = b.PostId AND b.TagId = c.Id
AND     a.Id = d.PostId
AND     a.OwnerUserId > @MinUserId AND a.OwnerUserId <= @MaxUserId
GROUP BY a.OwnerUserId
),
tblPythonQuestionVotes (OwnerUserId, UpVote, DownVote) AS
(
SELECT  a.OwnerUserId,
        SUM(CASE WHEN d.VoteTypeId = 2 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS UpVote,
        SUM(CASE WHEN d.VoteTypeId = 3 AND c.TagName = 'python' THEN 1 ELSE 0 END) AS DownVote
FROM    Posts a,
        PostTags b,
        Tags c,
        Votes d
WHERE   a.Id = b.PostId AND b.TagId = c.Id
AND     a.Id = d.PostId
AND     a.OwnerUserId > @MinUserId AND a.OwnerUserId <= @MaxUserId
GROUP BY a.OwnerUserId
),
tblTotalVotes (OwnerUserId, UpVote, DownVote) AS
(
SELECT  a.OwnerUserId,
        SUM(CASE WHEN b.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVote,
        SUM(CASE WHEN b.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVote
FROM    Posts a,
        Votes b
WHERE   a.Id = b.PostId
AND     a.OwnerUserId > @MinUserId AND a.OwnerUserId <= @MaxUserId
GROUP BY a.OwnerUserId
)
SELECT  a.OwnerUserId,
        CASE WHEN (a.UpVote = a.DownVote)
             THEN 0
             ELSE CAST((COALESCE(b.UpVote,0) + COALESCE(c.UpVote,0) - COALESCE(b.DownVote,0) - COALESCE(c.DownVote,0)) AS DOUBLE PRECISION) / (a.UpVote - a.DownVote)
        END AS VoteRatio_Python
FROM    tblTotalVotes a LEFT JOIN tblPythonAnswerVotes b ON a.OwnerUserId = b.OwnerUserId 
                        LEFT JOIN tblPythonQuestionVotes c ON a.OwnerUserId = c.OwnerUserId
ORDER BY 1;
