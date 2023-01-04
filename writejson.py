import requests
from bs4 import BeautifulSoup
import ssl
import sys
from piazza_api.rpc import PiazzaRPC
from piazza_api import Piazza
import json
import time
import csv
import pandas as pd
from datetime import datetime 

if __name__ == "__main__":
    piazza = PiazzaRPC("l6vqf2f5p8e6c1")
    piazza.user_login() # can pass in credentials as parameters
    for j in range(1, 1925):
        try:
            post = piazza.content_get(j)
            with open("posts.json", "a") as out:
                json.dump(post, out)
                out.write("\n")
                time.sleep(2)
                
        except:
            continue
    
    allPosts = []
    with open("posts.json") as f:
        for jsonObj in f:
            currPost = json.loads(jsonObj)
            allPosts.append(currPost)
    #print(json.dumps(allPosts[0], indent=4))
    #print(allPosts[0] == post)
    # print(allPosts)
    # print(len(allPosts))
    
