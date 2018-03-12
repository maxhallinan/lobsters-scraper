SELECT 
  users_.name,
  SUM(upvote_count),
  AVG(upvote_count),
  COUNT(stories_users_.user_id)
FROM 
  stories 
  INNER JOIN 
    stories_users_ ON stories.id=stories_users_.story_id
  INNER JOIN
    users_ ON stories_users_.user_id=users_.id
GROUP BY
  stories_users_.user_id,
  users_.name
ORDER BY
  SUM(upvote_count)
  /* AVG(upvote_count) */ 
DESC;
