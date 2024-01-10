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

#####################################
#  POTENTIALLY RELEVANT QUANTITIES  #
#####################################
#   post['created'] -- timestamp of initial post creation
#   post['change_log'] -- lists all changes (post created, instructor answer, followup, feedback)
#   post['history_size'] -- size of history list
#   post['history'] -- get last element of list?
#   post['type'] -- may help to differentiate between note and post
#   post['tags'] -- may help see if instructor note? probably unneeded
#   post['children'] -- followups yikes


# @840 is a decent question post to analyze
# @842 is private and has followup
# @1885 has multiple different followups
# @81 is an instructor note authored by multiple people?
    # probably not important to analyze
# would be good to start organizing output

# skips notes currently. 

printed_thingy = False

def connect_piazza(piazza):
    piazza = PiazzaRPC("lkj22ith9gvsl")
    piazza.user_login() #can pass in credentials as parameters
    return piazza

def get_ishaan_id(piazza, ishaan_id):
    for i in piazza.get_all_users():
        if i['name'] == 'Ishaan Lal':
            ishaan_id = i['id']
    return ishaan_id

def analyze_child(i, ishaan_id):
    if i['type'] == 'i_answer':
        print(i['history'][i['history_size']-1]['uid'])
        print(ishaan_id)
        if i['history'][i['history_size']-1]['uid'] == ishaan_id:
            instructor_answer = i['history'][i['history_size']-1]['content']
            print(instructor_answer)
    if i['type'] == 'followup':
        # print(json.dumps(i, indent=4))
        followup_content = i['subject']
        print(followup_content)
        followup_responses = i['children']
        for j in followup_responses:
            analyze_child(j)
        # potentially an annoying thing:
        # i['children'] is a feedback_children_dict
        # feedback_children_dict has a children field :O
    if i['type'] == 'feedback':
        # response to followup
        response = i['subject']
        print(response)


def clean_html(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
# i - json object of stuff
# main_q - main question?
# print - boolean representing whether or not to print the thingy
# returns true/false
def analyze_child_enh(i, ishaan_id, main_post, printer, f, post_num, folder, ish):
    global printed_thingy
    if i['type'] == 'i_answer':
        # check if response is from ishaan?
        # returns TRUE if ishaan responded, FALSE if not

        # can improve to get exact ishaan response
        # loop through i['history'] and try to find matching uid
        # the return the appropriate content.
        # for j in i['history']:
        #     if j['uid'] == ishaan_id:

        if i['history'][i['history_size']-1]['uid'] == ishaan_id:
            instructor_answer = i['history'][i['history_size']-1]['content']
            print(main_post)
            timeposted = main_post['created']
            timeanswered = i['history'][i['history_size']-1]['created']
            time_to_ans = datetime.strptime(timeanswered, "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(timeposted, "%Y-%m-%dT%H:%M:%SZ")
            printed_thingy = True
            ish.write(clean_html(instructor_answer))
            ish.write('\n')
            f.write("<article class=\"general-box\">")
            f.write("\n")
            f.write("<p>Post: " + str(post_num) + "</p>")
            f.write("\n")
            f.write("<p>Folder: " + folder + "</p>")
            f.write("\n")
            f.write("<p>Title: " + main_post['subject'] + "</p>")
            f.write('\n')
            f.write("<article class=\"question\">\n")
            f.write(main_post['content'])
            f.write('\n')
            f.write("</article>\n")
            print(main_post['content'])
            print(instructor_answer)
            f.write("<article class=\"answer\">\n")
            f.write(instructor_answer)
            f.write('\n')
            f.write("</article>\n")
            f.write("<p>Response Time: "+ str(time_to_ans) +"</p>")
            f.write('\n')
            return True
        else:
            return False
    if i['type'] == 'followup':
        followup_content = i['subject']
        followup_responses = i['children']

        ####### THIS WORKS ###########
        if printer:
            f.write("<article class=\"question\">\n")
            f.write(followup_content)
            f.write('\n')
            f.write("</article>\n")
            for j in followup_responses:
                printer = analyze_child_enh(j, ishaan_id, followup_content, printer, f, post_num, folder, ish)
        #############################


        # if 'uid' in i.keys():
        #     # can change to if printer and i['uid'] == ishaan_id
        #     if printer:
        #         f.write("<article class=\"answer\"\n")
        #         f.write(followup_content)
        #         f.write('\n')
        #         f.write("</article>\n")
        #         for j in followup_responses:
        #             analyze_child_enh(j, ishaan_id, followup_content, printer, f, post_num, folder)
        # elif printer:
        #     f.write("<article class=\"question\">\n")
        #     f.write(followup_content)
        #     f.write('\n')
        #     f.write("</article>\n")
        #     for j in followup_responses:
        #         analyze_child_enh(j, ishaan_id, followup_content, printer, f, post_num, folder)


        # if printer and i['uid'] != ishaan_id:
        #     f.write("<article class=\"question\">\n")
        #     f.write(followup_content)
        #     f.write('\n')
        #     f.write("</article>\n")
        #     print(followup_content)
        #     if len(followup_responses > 0):
        #         for j in followup_responses:
        #             analyze_child_enh(j, ishaan_id, followup_content, printer, f, post_num, folder)
        #     else:
        #         f.write("</article>\n")
        #     # f.write("</article>\n")
        # elif printer:
        #     f.write("<article class=\"answer\">\n")
        #     f.write(followup_content)
        #     f.write('\n')
        #     f.write("</article>")
        #     print(followup_responses)
        #     for j in followup_responses:
        #         printer = analyze_child_enh(j, ishaan_id, followup_content, printer, f, post_num, folder)
        return printer
    if i['type'] == 'feedback':
        response = i['subject']
        print(i)
        ################ THIS WORKS ####################
        if printer:
            f.write("<article class=\"answer\">\n")
            f.write(response)
            f.write('\n')
            f.write("</article>\n")
        ################################################


        # if 'uid' in i.keys():
        #     if printer:
        #         f.write("<article class=\"answer\">\n")
        #         f.write(response)
        #         f.write('\n')
        #         f.write("</article>\n")
        # elif printer:
        #     f.write("<article class=\"question\">\n")
        #     f.write(response)
        #     f.write('\n')
        #     f.write("</article>\n")

        # if printer and i['uid'] == ishaan_id:
        #     f.write("<article class=\"answer\">\n")
        #     f.write(response)
        #     f.write('\n')
        #     f.write("</article>\n")
        #     print(response)
        # elif printer:
        #     f.write("<article class=\"question\">\n")
        #     f.write(response)
        #     f.write('\n')
        #     f.write("</article>\n")
        return printer
    return False # may not be needed?


def analyze_post(piazza, ishaan_id, f, ish):
    # allPosts = []
    # with open("posts.json") as f2:
    #     for jsonObj in f2:
    #         currPost = json.loads(jsonObj)
    #         allPosts.append(currPost)
    allPosts = get_all_posts(piazza)
    global printed_thingy
    # NEED TO ANALYZE POST @81
    for j in range(0, 1168):
        printed_thingy = False
        try:
            # post = piazza.content_get(j) #1919 also good to test
            post = allPosts[j]
            folder = post['folders'][len(post['folders'])-1]
            main_post = post['history'][post['history_size']-1]
            main_question = main_post['content']

            children = post['children']
            

            if post['type'] == 'note':
                printer = False
            else:
                printer = True
            for i in children:
                printer = analyze_child_enh(i, ishaan_id, main_post, printer, f, j, folder, ish)
            if printed_thingy:
                f.write("</article>\n")
            f.write('\n')
            print('\n')
            # time.sleep(2)
        except:
            continue

def get_ishaan_q_and_a(piazza, ishaan_id):
    allPosts = get_all_posts(piazza)
    for j in range(12, 13):
        try:
            post = allPosts[j]
            print(json.dumps(post, indent=4))
        except:
            continue

def get_counts(piazza):
    # allPosts = []
    # with open("posts.json") as f2:
    #     for jsonObj in f2:
    #         currPost = json.loads(jsonObj)
    #         allPosts.append(currPost)
    allPosts = get_all_posts(piazza)
    counts = {}
    for i in piazza.get_all_users():
        counts[i['id']] = 0
    for j in range(0, 1168):
        try:
            post = piazza.content_get(j)
            post = allPosts[j]
            for i in post['change_log']:
                if 'uid' in i:
                    counts[i['uid']]+=1
            time.sleep(2)
        except:
            continue
    translate(piazza, counts)
    # print(counts)

def translate(piazza, old_counts):
    ids_to_name = {}
    for i in piazza.get_all_users():
        ids_to_name[i['id']] = i['name']
    # print(ids_to_name)
    translation = {}
    for i in old_counts:
        translation[ids_to_name[i]] = old_counts[i]
    translation = {k:v for k, v in sorted(translation.items(), key=lambda item: -item[1])}
    tas = ['Rajiv Gandhi', 'Ishaan Lal', 'Andrew Jiang', 'Rashmi Iyer', 'Elisa Luo',
           'Harish Balasubramanian', 'Darren Chen', 'Luna Chen', 'Nathan Chen',
           'Aaron Jiang', 'Alexandra Oh', 'Cindy Yang', 'Claire Lu', 'Dilini Ranaweera',
           'Eric Zhao', 'Ethan Soloway', 'Ethan Weisberg', 'Gabrielle Tran', 'Hasit Nanda',
           'Helen Rudoler', 'Jason Liu', 'Karen Li', 'Megan Yang', 'Michael Tesfaye', 
           'Ria Subramanian', 'Richard Zhang', 'Sam Ngiam', 'Sana Manesh', 'Sara Xin',
           'Saurabh Mallela', 'Selina Qiu', 'Shaurya Singhi', 'Sidhant Srivastava',
           'Suzanna Wang', 'Thomas Li', 'Thomas Zeuthen', 'Victor Zhu', 'Winnie Dong',
           'Winston Chen', 'Yijia Li'
           ]
    ta_counts = {}
    print(translation)
    for ta in tas:
        ta_counts[ta] = translation[ta]
    ta_counts = {k:v for k, v in sorted(ta_counts.items(), key=lambda item: -item[1])}
    print(json.dumps(translation, indent=4))
    json_obj = json.dumps(translation, indent=4)
    # f2 = open("counts.txt", "w")

    with open("counts.txt", "w") as outfile:
        outfile.write(json_obj)

    tas_obj = json.dumps(ta_counts, indent=4)
    with open("TAs_counts.txt", "w") as out:
        out.write(tas_obj)

def get_all_posts(piazza):
    allPosts = []
    with open("posts23.json") as f:
        for jsonObj in f:
            currPost = json.loads(jsonObj)
            allPosts.append(currPost)
    return allPosts

def my_analysis(piazza):
    allPosts = get_all_posts(piazza)
    print(json.dumps(allPosts[618], indent=4))

# def get_ishaan_id(piazza, ishaan_id):
#     for i in piazza.get_all_users():
#         if i['name'] == 'Ishaan Lal':
#             ishaan_id = i['id']
#     return ishaan_id


if __name__ == "__main__":
    f = open("piazzas23.txt", "w")
    ish = open("ishaa23.txt", "w")
    piazza = None
    ishaan_id = 0
    piazza = connect_piazza(piazza)
    ishaan_id = get_ishaan_id(piazza, ishaan_id)
    # analyze_post(piazza, ishaan_id, f, ish)
    print('getting counts')
    # get_counts(piazza)
    # my_analysis(piazza)
    get_ishaan_q_and_a(piazza, ishaan_id)