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
tblQuestion (Id, OwnerUserId, CreationDate,
             UpVotes, DownVotes,
             AnswerCount, ViewCount, CommentCount, FavoriteCount,
             ClosedDate, Reputation) AS 
(
SELECT  a.Id,
        a.OwnerUserId,
        a.CreationDate,
        SUM(CASE WHEN b.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVotes,
        SUM(CASE WHEN b.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVotes,
        a.AnswerCount,
        a.ViewCount,
        a.CommentCount,
        a.FavoriteCount,
        a.ClosedDate,
        a.Reputation -- * (python votes / total votes)
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
        AND     a.CreationDate BETWEEN '2000-01-01' AND '2009-01-01'
        --AND     a.CreationDate BETWEEN '2009-01-01' AND '2010-01-01'
        --AND     a.CreationDate BETWEEN '2010-01-01' AND '2010-07-01'
        --AND     a.CreationDate BETWEEN '2010-07-01' AND '2011-01-01'
        --AND     a.CreationDate BETWEEN '2011-01-01' AND '2011-07-01'
        --AND     a.CreationDate BETWEEN '2011-07-01' AND '2012-01-01'
        --AND     a.CreationDate BETWEEN '2012-01-01' AND '2012-04-01'
        --AND     a.CreationDate BETWEEN '2012-04-01' AND '2012-07-01'
        --AND     a.CreationDate BETWEEN '2012-07-01' AND '2012-10-01'
        --AND     a.CreationDate BETWEEN '2012-10-01' AND '2013-01-01'
        --AND     a.CreationDate BETWEEN '2013-01-01' AND '2013-04-01'
        --AND     a.CreationDate BETWEEN '2013-04-01' AND '2013-07-01'
        --AND     a.CreationDate BETWEEN '2013-07-01' AND '2013-10-01'
        --AND     a.CreationDate BETWEEN '2013-10-01' AND '2013-12-31'
        ) a LEFT JOIN
        Votes b
        ON a.Id = b.PostId
GROUP BY a.Id, a.OwnerUserId, a.CreationDate, a.AnswerCount, a.ViewCount, a.CommentCount, a.FavoriteCount, a.ClosedDate, a.Reputation
),
tblAnswer   (Id, ParentId, OwnerUserId, CreationDate,
             UpVotes, DownVotes,
             AnswerCount, ViewCount, CommentCount, FavoriteCount,
             ClosedDate, Reputation) AS 
(
SELECT  a.Id,
        a.ParentId,
        a.OwnerUserId,
        a.CreationDate,
        SUM(CASE WHEN b.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVotes,
        SUM(CASE WHEN b.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVotes,
        a.AnswerCount,
        a.ViewCount,
        a.CommentCount,
        a.FavoriteCount,
        a.ClosedDate,
        a.Reputation --* (python votes / total votes)
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
        AND     e.CreationDate BETWEEN '2000-01-01' AND '2009-01-01'
        --AND     e.CreationDate BETWEEN '2009-01-01' AND '2010-01-01'
        --AND     e.CreationDate BETWEEN '2010-01-01' AND '2010-07-01'
        --AND     e.CreationDate BETWEEN '2010-07-01' AND '2011-01-01'
        --AND     e.CreationDate BETWEEN '2011-01-01' AND '2011-07-01'
        --AND     e.CreationDate BETWEEN '2011-07-01' AND '2012-01-01'
        --AND     e.CreationDate BETWEEN '2012-01-01' AND '2012-04-01'
        --AND     e.CreationDate BETWEEN '2012-04-01' AND '2012-07-01'
        --AND     e.CreationDate BETWEEN '2012-07-01' AND '2012-10-01'
        --AND     e.CreationDate BETWEEN '2012-10-01' AND '2013-01-01'
        --AND     e.CreationDate BETWEEN '2013-01-01' AND '2013-04-01'
        --AND     e.CreationDate BETWEEN '2013-04-01' AND '2013-07-01'
        --AND     e.CreationDate BETWEEN '2013-07-01' AND '2013-10-01'
        --AND     e.CreationDate BETWEEN '2013-10-01' AND '2013-12-31'
        ) a LEFT JOIN
        Votes b
        ON a.Id = b.PostId
GROUP BY a.Id, a.ParentId, a.OwnerUserId, a.CreationDate, a.AnswerCount, a.ViewCount, a.CommentCount, a.FavoriteCount, a.ClosedDate, a.Reputation
)
SELECT  a.*,
        b.Tags AS Q_Tags
FROM    (
        SELECT  a.OwnerUserId AS SrcNodeId,
                b.OwnerUserId AS DstNodeId,
                a.Id AS Q_Id,
                a.CreationDate AS Q_CreationDate,
                a.UpVotes AS Q_UpVotes,
                a.DownVotes AS Q_DownVotes,
                a.AnswerCount AS Q_AnswerCount, 
                a.ViewCount AS Q_ViewCount, 
                a.CommentCount AS Q_CommentCount, 
                a.FavoriteCount AS Q_FavoriteCount,
                a.ClosedDate AS Q_ClosedDate,
                a.Reputation AS Q_Reputation,
                b.Id AS A_Id,
                b.CreationDate AS A_CreationDate,
                b.UpVotes AS A_UpVotes,
                b.DownVotes AS A_DownVotes,
                --b.AnswerCount AS A_AnswerCount, 
                --b.ViewCount AS A_ViewCount,
                b.CommentCount AS A_CommentCount, 
                --b.FavoriteCount AS A_FavoriteCount,
                --b.ClosedDate AS A_ClosedDate,
                b.Reputation AS A_Reputation
        FROM    tblQuestion a,
                tblAnswer b
        WHERE   a.Id = b.ParentId
        ) a,
        Posts b
WHERE   a.Q_Id = b.Id 
ORDER BY a.Q_Id, a.DstNodeId;
