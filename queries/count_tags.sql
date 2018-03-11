SELECT 
    tags.name, COUNT(tags.name) 
FROM 
    tags INNER JOIN stories_tags 
ON 
    tags.id=stories_tags.tag_id 
GROUP BY 
    tags.name 
ORDER BY 
    COUNT(tags.name) 
DESC;
