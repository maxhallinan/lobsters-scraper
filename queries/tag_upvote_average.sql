SELECT 
  tags.name,
  AVG(upvote_count)
FROM 
  stories 
  INNER JOIN stories_tags ON stories.id=stories_tags.story_id
  INNER JOIN tags ON stories_tags.tag_id=tags.id
GROUP BY
  tags.id,
  tags.name
ORDER BY
  AVG(upvote_count)
DESC;
