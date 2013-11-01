--------------------------------------------------------------------------------
-- Build network with filter
-- filter = (tag = python)

-- Example edge:
-- Dark fader --> (
--                questionId = 613183,
--                upvote = 720,
--                downvote = 3, 
--                devin_rep = 18720
--                darth_rep = 4297
--                tags=[python, list, dictionary, sorting, tuples]
--                ) 
-- Devin Jeanpierre

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
        --AND     a.CreationDate BETWEEN '2000-01-01' AND '2008-12-31'
        --AND     a.CreationDate BETWEEN '2009-01-01' AND '2009-12-31'
        --AND     a.CreationDate BETWEEN '2010-01-01' AND '2010-06-30'
        --AND     a.CreationDate BETWEEN '2010-07-01' AND '2010-12-31'
        --AND     a.CreationDate BETWEEN '2011-01-01' AND '2011-06-30'
        --AND     a.CreationDate BETWEEN '2011-07-01' AND '2011-12-31'
        --AND     a.CreationDate BETWEEN '2012-01-01' AND '2012-03-31'
        --AND     a.CreationDate BETWEEN '2012-04-01' AND '2012-06-30'
        --AND     a.CreationDate BETWEEN '2012-07-01' AND '2012-09-30'
        --AND     a.CreationDate BETWEEN '2012-10-01' AND '2012-12-31'
        --AND     a.CreationDate BETWEEN '2013-01-01' AND '2013-03-31'
        --AND     a.CreationDate BETWEEN '2013-04-01' AND '2013-06-30'
        --AND     a.CreationDate BETWEEN '2013-07-01' AND '2013-09-30'
        --AND     a.CreationDate BETWEEN '2013-10-01' AND '2013-12-31'
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
        --AND     e.CreationDate BETWEEN '2000-01-01' AND '2008-12-31'
        --AND     e.CreationDate BETWEEN '2009-01-01' AND '2009-12-31'
        --AND     e.CreationDate BETWEEN '2010-01-01' AND '2010-06-30'
        --AND     e.CreationDate BETWEEN '2010-07-01' AND '2010-12-31'
        --AND     e.CreationDate BETWEEN '2011-01-01' AND '2011-06-30'
        --AND     e.CreationDate BETWEEN '2011-07-01' AND '2011-12-31'
        --AND     e.CreationDate BETWEEN '2012-01-01' AND '2012-03-31'
        --AND     e.CreationDate BETWEEN '2012-04-01' AND '2012-06-30'
        --AND     e.CreationDate BETWEEN '2012-07-01' AND '2012-09-30'
        --AND     e.CreationDate BETWEEN '2012-10-01' AND '2012-12-31'
        --AND     e.CreationDate BETWEEN '2013-01-01' AND '2013-03-31'
        --AND     e.CreationDate BETWEEN '2013-04-01' AND '2013-06-30'
        --AND     e.CreationDate BETWEEN '2013-07-01' AND '2013-09-30'
        --AND     e.CreationDate BETWEEN '2013-10-01' AND '2013-12-31'
        ) a LEFT JOIN
        Votes b
        ON a.Id = b.PostId
GROUP BY a.Id, a.ParentId, a.OwnerUserId, a.Reputation
)
SELECT  a.SrcNodeId,
        a.DstNodeId,
        a.QuestionId AS EdgeAttrQuestionId,
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
ORDER BY a.QuestionId, a.DstNodeId;
