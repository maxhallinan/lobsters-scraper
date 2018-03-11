CREATE TABLE stories (
    id serial PRIMARY KEY,
    comment_count int,
    submitted_on timestamp,
    title varchar (200),
    url varchar (2083),
    upvote_count int
)
