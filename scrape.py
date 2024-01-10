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


#if __name__ == "__main__":

def csvstuff():
    p = PiazzaRPC("lkj22ith9gvsl")
    p.user_login()
    
    # put in for loop
    try:
        post = p.content_get(10)
        cols = post.keys()
        csv_file = "piazzas23.csv"
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cols)
                writer.writeheader()
                writer.writerow(post)
        except IOError:
            print("IOError")
        # f = pd.json_normalize(post, record_path=['change_log', 'history', 'children', 'config'])
        # f = pd.json_normalize(post)
        # json_obj = json.dumps(post)
        # print(json_obj)
        # # f2 = pd.json_normalize(post, "history")
        
        # f.to_csv("piazza.csv")
        # #f2.to_csv("piazza.csv")
        # try:
        #     with open(csv_file, 'w') as csvfile:
        #         writer = csv.writer(csvfile, fieldnames = f.columns)
        #         writer.writeheader()
        #         writer.writerow(json_obj)
        # except IOError:
        #     print("IOError")
        # print(f)
            
        

    except:
        pass

def dostuff():
    p = PiazzaRPC("lkj22ith9gvsl")
    p.user_login() # can pass in credentials as parameters
    ishaan_id = 0
    for i in p.get_all_users():
        if i['name'] == 'Ishaan Lal':
            ishaan_id = i['id']

    for j in range(1, 1678):
        try:
            post = p.content_get(j)
            # print(json.dumps(post, indent = 4))
            ishaan_msg = False
            # print(dir(p))
            change_log = []
            followup = []
            timeposted = ''
            timeanswered = ''
            print("time posted: " + post['created'])
            print("-------------------QUESTION--------------------")
            change = post['history'][0]
            print("subject: " + change['subject'])
            print("timestamp: " + change['created'])
            timeposted = change['created']
            print("content: " + change['content'])
            change_log.append(post)


            ishaan = False
            
            count = 0
            for child in post['children']:
                # check if response or followup
                if child['type'] == 'i_answer':
                    print("-----------------RESPONSE-----------------")
                    # response
                    for change in child['history']:
                        # should check if responder is me by verifying uid
                        print("User: " + change['uid'])
                        if (change['uid'] == ishaan_id):
                            change_log.append(change)
                            ishaan = True
                            print("Ishaan Answered this!")
                        timeanswered = change['created']
                        print("timestamp: " + change['created'])
                        print("content: " + change['content'])
                elif child['type'] == 'followup':
                    print("----------------FOLLOWUP-----------------")
                    # followup
                    print("follwup question: " + child['subject'])
                    for change in child['children']:
                        count = count + 1
                        #print("User: " + change['uid'])
                        if count >= 2:
                            if 'uid' not in change.keys() or change['uid'] == ishaan_id:
                                followup.append(child)
                                followup.append(change)
                        elif ('uid' in change.keys() and change['uid'] == ishaan_id):
                            followup.append(child)
                            followup.append(change)
                            print("Ishaan Answered this!")
                        print("timestamp: " + change['created'])
                        print("content: " + change['subject'])
            print("------------------------------------------------------------")
            f = open("piazza.txt", "a")
            if (ishaan):
                change_log = [post] + change_log
            # change_log = [*set(change_log)]
            for i in range(len(change_log)):
                if i > 0:
                    if 'content' in change_log[i]:
                        f.write(change_log[i]['content'])
                        f.write("\n")
                        print(change_log[i]['content'])
                    elif 'history' in change_log[i]:
                        f.write(change_log[i]['history'][0]['content'])
                        f.write("\n")
                        print(change_log[i]['history'][0]['content'])
                else:
                    f.write(change_log[i]['history'][0]['content'])
                    f.write("\n")
                    print(change_log[i]['history'][0]['content'])
            # followup = [*set(followup)]
            for i in followup:
                f.write(i['subject'])
                f.write("\n")
                print(i['subject'])

            if (timeanswered != '' and timeanswered != '' and ishaan):
                time_to_ans = datetime.strptime(timeanswered, "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(timeposted, "%Y-%m-%dT%H:%M:%SZ")
                f.write("response time: " + str(time_to_ans))
                f.write("\n\n\n\n")
                print("response time: " + str(time_to_ans))
            time.sleep(2)
        except:
            continue
    f.close()

def getstats():
    #p = PiazzaRPC("l6vqf2f5p8e6c1")
    p = Piazza("lkj22ith9gvsl")
    p.user_login() #can pass in credentials as parameters
    network = p.network("lkj22ith9gvsl")
    stats = network.get_statistics()
    print(stats)
        

if __name__ == "__main__":
    dostuff()
    # getstats()