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
FROM    Posts a,
        PostTypes b,
        Comments c
WHERE   a.PostTypeId = b.Id
AND     a.Id = c.PostId
AND     (a.Id = 613183 OR a.ParentId = 613183)
ORDER BY b.Name DESC, a.Score DESC, c.Score DESC;
