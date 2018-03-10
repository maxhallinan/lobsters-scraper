import csv
import datetime
import os
import psycopg2
import sys

def datetime_string_to_timestamp(datetime_string):
    datetime_string_format = "%Y-%m-%d %H:%M:%S %z"

    dt = datetime.datetime.strptime(datetime_string, datetime_string_format)

    ts = dt.timestamp()

    return ts

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

    # values = [row[0], datetime_string_to_timestamp(row[1]), row[2], row[3], row[4], row[5], row[6]]
    values = row

    cursor.execute(query, values)

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
