import csv
import os
import psycopg2
import sys

def insert_story(cursor, row):
    query = """
    INSERT INTO stories (
        comment_count, 
        submitted_on,
        tags,
        title,
        url,
        username,
        upvote_count
    ) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    );
    """

    cursor.execute(query, row)

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
