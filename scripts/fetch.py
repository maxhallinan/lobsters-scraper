from bs4 import BeautifulSoup
import requests
import sys
import time

root_url = "https://lobste.rs"

def get_next_page(root_url, path):
    url = "%s%s" % (root_url, path)

    response = requests.get(url, timeout=10)

    sanitized_path = path[1:]

    html_file_name = "data/html/%s.html" % (sanitized_path.replace("/", "-"))

    html_file = open(html_file_name, "w")

    html_file.write(response.text)

    html_file.close

    print(path)

    soup = BeautifulSoup(response.content, 'html.parser')

    pagination = soup.select('.morelink')
        
    if len(pagination) > 0:
        pagination_anchors = pagination[0].find_all('a')

        next_page_path = pagination_anchors[-1]['href']


        if next_page_path:
            time.sleep(1) 

            get_next_page(root_url, next_page_path)

start_page = "/page/%s" % (sys.argv[1])

get_next_page(root_url, start_page)
