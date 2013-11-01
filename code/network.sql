--------------------------------------------------------------------------------
-- Build network with filter
-- filter = (tag = python, question date = 2013 Oct)

-- Example edge:
-- Dark fader --> (
--                upvote = 720,
--                downvote = 3, 
--                devin_rep = 18720
--                darth_rep = 4297
--                tags=[python, list, dictionary, sorting, tuples], 
--                ) 
-- Devin Jeanpierre

-- There are several DEBUG filters. Uncomment them to test results.
-- Debug 1:
-- Mimic this question
-- http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value

-- Debug 2:
-- In the same month (March 2009), dark fader also answered to a question
-- http://stackoverflow.com/questions/644170/how-does-python-sort-a-list-of-tuples

--------------------------------------------------------------------------------

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
SELECT  a.QuestionId,  -- Exclude this from network
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

