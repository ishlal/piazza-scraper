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
import scrape2

# gets the counts of posts made per hour

if __name__ == "__main__":
    piazza = None
    piazza = scrape2.connect_piazza(piazza)
    allPosts = scrape2.get_all_posts(piazza)
    time_counts = {}
    for i in range(24):
        time_counts[i] = 0
    for i in allPosts:
        timePosted = i['created']
        trimmed = datetime.strptime(timePosted, "%Y-%m-%dT%H:%M:%SZ")
        time_counts[int(trimmed.hour)]+=1
    time_counts = {k:v for k, v in sorted(time_counts.items(), key=lambda item: -item[1])}
    print(time_counts)
    