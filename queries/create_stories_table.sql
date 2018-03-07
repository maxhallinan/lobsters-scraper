CREATE TABLE stories (
    id serial PRIMARY KEY,
    comment_count int,
    submitted_on timestamp,
    tags varchar (200),
    title varchar (200),
    url varchar (2083),
    username varchar (200),
    upvote_count int
)
