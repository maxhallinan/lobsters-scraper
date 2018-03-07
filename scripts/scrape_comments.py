from bs4 import BeautifulSoup
import csv
import os
import re
import sys

def scrape_story(story_soup):
    comment_label_text = story_soup.select(".comments_label a")[0].text 

    try:
        comment_count = re.search('[0-9]+', comment_label_text).group(0)
    except AttributeError:
        comment_count = 0

    submitted_on = story_soup.select(".byline span")[0]["title"]

    tags = [ tag_soup["href"] for tag_soup in story_soup.select(".tag")]

    title = story_soup.select(".link a")[0].text

    url = story_soup.select(".link a")[0]["href"]

    user = story_soup.select(".byline a")[0]["href"]

    vote_count = story_soup.select(".score")[0].text
    
    return [comment_count, submitted_on, tags, title, url, user, vote_count]

def scrape_page(file_path, target_path):
    with open(file_path, "r") as page:
        soup = BeautifulSoup(page, "html.parser")

        stories = soup.select(".story")

        data = [scrape_story(story) for story in stories]

    with open(target_path, "w") as target:
        writer = csv.writer(target)

        writer.writerows(data)

        print(target_path)

def scrape_pages(source_path, target_path):
    for filename in os.listdir(source_path):
        if filename.endswith(".html"):
            page_source_path = "%s%s" % (source_path, filename)

            page_target_path = "%s%s" % (target_path, filename.replace(".html", ".csv"))

            scrape_page(page_source_path, page_target_path)

source_path = sys.argv[1]

target_path = sys.argv[2]

scrape_pages(source_path, target_path)
