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

import spacy
import re
import markovify
import nltk
import warnings
warnings.filterwarnings('ignore')

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ['::'.join((word.orth_, word.pos_)) for word in nlp(sentence)]
    def word_join(self, words):
        sentence = ' '.join(word.split('::')[0] for word in words)
        return sentence

if __name__ == "__main__":
    text = open("ishaan.txt", "r").read()
    nlp = spacy.load('en_core_web_sm')
    ishaan_doc = nlp(text)
    ishaan_sents = ' '.join([sent.text for sent in ishaan_doc.sents if len(sent.text) > 1])
    # print(ishaan_sents)
    generator = markovify.Text(ishaan_sents, state_size=3)
    # for i in range(3):
    #     print(generator.make_sentence())
    generator2 = POSifiedText(ishaan_sents, state_size=3)
    for i in range(5):
        print(generator2.make_sentence())
    