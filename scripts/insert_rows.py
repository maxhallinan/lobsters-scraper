import csv
import datetime
import json
import os
import psycopg2
import sys

def datetime_string_to_timestamp(datetime_string):
    datetime_string_format = "%Y-%m-%d %H:%M:%S %z"

    dt = datetime.datetime.strptime(datetime_string, datetime_string_format)

    ts = dt.timestamp()

    return ts

# insert a row for each story to `stories` table
def insert_story_row(cursor, comment_count, submitted_on, title, url, upvote_count):
    query = """
    INSERT INTO stories (
        comment_count, 
        submitted_on,
        title,
        url,
        upvote_count
    ) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s
    )
    RETURNING id;
    """
    values = [comment_count, submitted_on, title, url, upvote_count]

    cursor.execute(query, values)

    id = cursor.fetchone()[0]

    return id


# insert a row for each tag in the `stories_tags` table
def insert_stories_tags_row(cursor, story_id, tag_id):
    query = """
    INSERT INTO stories_tags (
        story_id,
        tag_id
    ) VALUES (
        %s,
        %s
    )
    RETURNING id;
    """

    values = [story_id, tag_id]

    cursor.execute(query, values)

    id = cursor.fetchone()[0]

    return id

# insert a row for each tag in the `stories_users` table
def insert_stories_users_row(cursor, story_id, user_id):
    query = """
    INSERT INTO stories_users_ (
        story_id,
        user_id
    ) VALUES (
        %s,
        %s
    )
    RETURNING id;
    """

    values = [story_id, user_id]

    cursor.execute(query, values)

    id = cursor.fetchone()[0]

    return id

# select a tag by name 
def select_tag_by_name(cursor, tag_name):
    query = """
    SELECT 
        id 
    FROM 
        tags 
    WHERE 
        name = %s;
    """

    values = [tag_name]
    
    cursor.execute(query, values)

    tag = cursor.fetchone()

    if tag == None:
        id = None
    else:
        id = tag[0]

    return id
    
# insert a row for each tag if tag does not exist in `tags` table
def insert_tags_row(cursor, tag_name):
    query = """
    INSERT INTO tags (
        name
    ) VALUES (
        %s
    )
    RETURNING id;
    """

    values = [tag_name]

    cursor.execute(query, values)

    id = cursor.fetchone()[0]

    return id

# select a user by user_name 
def select_user_by_name(cursor, user_name):
    query = """
    SELECT 
        id 
    FROM 
        users_ 
    WHERE 
        name = %s;
    """

    values = [user_name]
    
    cursor.execute(query, values)

    user = cursor.fetchone()

    if user == None:
        id = None
    else:
        id = user[0]

    return id
    
# insert a row for each user in story to `users` table
def insert_users_row(cursor, user_name):
    query = """
    INSERT INTO users_ (
        name
    ) VALUES (
        %s
    )
    RETURNING id;
    """

    values = [user_name]

    cursor.execute(query, values)

    id = cursor.fetchone()[0]

    return id

def insert_story(cursor, row):
    comment_count = row[0]
    submitted_on = row[1]
    tag_names = row[2].split(',')
    title = row[3]
    url = row[4]
    user_name = row[5]
    upvote_count = row[6]

    # insert story row
    story_id = insert_story_row(cursor, comment_count, submitted_on, title, url, upvote_count)

    # check if user is already in users_ table
    user_id = select_user_by_name(cursor, user_name)
    # if user is not in database, create row for user
    if user_id == None:
        user_id = insert_users_row(cursor, user_name)

    # create row in stories_users table
    insert_stories_users_row(cursor, story_id, user_id)

    tag_ids = []

    # for each tag:
    for tag_name in tag_names:
        # check if tag name is already in tags table
        tag_id = select_tag_by_name(cursor, tag_name)
        # if user is not in database, create row for user
        if tag_id == None:
            tag_id = insert_tags_row(cursor, tag_name)
        # add to tag ids
        tag_ids.append(tag_id)

    for tag_id in tag_ids:
        insert_stories_tags_row(cursor, story_id, tag_id)

def insert_stories(data_dir_path):
    connection = psycopg2.connect("dbname=lobsters")
    cursor = connection.cursor()

    for filename in os.listdir(data_dir_path):
        with open(os.path.join(data_dir_path, filename), "r") as csv_file:
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                insert_story(cursor, row)

    connection.commit()
    cursor.close()
    connection.close()

insert_stories(sys.argv[1])
