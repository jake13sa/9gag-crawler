import requests
from datetime import datetime
import pandas as pd

# variables and inputs
number_of_content_to_scrape = int(input("How many content?: "))
tag = input("Tag: ")
page = 1

# for requests
base_url = f"https://9gag.com/v1/tag-posts/tag/{tag}?c={page}"
user_agent = {'user-agent': 'Mediapartners-Google'}

time_now = str(datetime.now().strftime('_%Y-%m-%d_%H-%M-%S'))
data = []       # dictionary to be stored in an excel file in the last lines

while page <= number_of_content_to_scrape:
    print(f"SCRAPING {number_of_content_to_scrape*(page/100)}%")
    gag_page = requests.get(base_url, headers=user_agent)       # Start giving parameters here for
    contents = gag_page.json()      # dict                      # the request to update every page
    contents = contents["data"]["posts"]
    for content in contents:                                    # LOOP THE DICT
        try: 
            content_details = {}
            content_details["id"] = content["id"]
            content_details["url"] = content["url"]
            content_details["title"] = content["title"]
            content_details["creator"] = content["creator"]["username"]
            if 'image460sv' in content["images"].keys():
                content_details["type"] = "video"
                content_details["url_download"] = content["images"]["image460sv"]["url"]
            else:
                content_details["type"] = "image"
                content_details["url_download"] = content["images"]["image700"]["url"]

            data.append(content_details)
        
        except Exception as e:
            print(e)

        page += 1       # increment value for the next 1 content
    
    base_url = f"https://9gag.com/v1/tag-posts/tag/{tag}?c={page}"

df = pd.DataFrame(data)
df.to_excel(f"{tag+time_now}.xlsx")         # add timestamp to the name to avoid duplication

print("Scraping Success")