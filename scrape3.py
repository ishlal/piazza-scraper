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

def connect_piazza(piazza):
    piazza = PiazzaRPC("l6vqf2f5p8e6c1")
    piazza.user_login() #can pass in credentials as parameters
    return piazza

def get_ishaan_id(piazza, ishaan_id):
    for i in piazza.get_all_users():
        if i['name'] == 'Ishaan Lal':
            ishaan_id = i['id']
    return ishaan_id

def get_ishaan_q_and_a(piazza, ishaan_id):
    with open("ishaan_f22.txt", "a") as f:
        for j in range(10, 1925):
            try:
                post = piazza.content_get(j)
                change_log = post["change_log"]
                index_of_question = 0
                index_of_answer = 0
                is_ishaan_answer = False
                for i in range(len(change_log)):
                    if change_log[i]["type"] == "create":
                        index_of_question = i
                    elif change_log[i]["type"] == "i_answer":
                        index_of_answer = i
                        print(change_log[i]["uid"])
                        if change_log[i]["uid"] == ishaan_id:
                            is_ishaan_answer = True
                if is_ishaan_answer:
                    question = post["history"][0]["content"]
                    answer = post["children"][0]["history"][0]["content"]
                    # print("QUESTION: " + question + "\nANSWER: " + answer + "\n\n")
                    f.write("QUESTION: " + question + "\nANSWER: " + answer + "\n\n")

                # print(post)
                # print(json.dumps(post, indent=4))
            except:
                continue
            time.sleep(2.1)
    f.close()

piazza = None
ishaan_id = 0
piazza = connect_piazza(piazza)
ishaan_id = get_ishaan_id(piazza, ishaan_id)
print(ishaan_id)
get_ishaan_q_and_a(piazza, ishaan_id)