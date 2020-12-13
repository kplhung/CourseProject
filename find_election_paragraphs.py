#!/usr/bin/env python
# coding: utf-8

# # Filter May - Oct 2000 NYT corpus for election-related paragraphs

# In[1]:


import os
import xml.etree.ElementTree as ET

def find_election_paragraphs(directory):
    election_paragraphs = open("election_paragraphs.csv", "w+")
    election_paragraphs.write("Date///Paragraph\n")
    for root, dirs, files in os.walk(directory):
        for file in files:
            f = open(os.path.join(root, file), "r")
            try:
                parse_xml(f, election_paragraphs)
            except UnicodeDecodeError:
                continue
                

def parse_xml(xml, election_paragraphs):
    tree = ET.parse(xml)
    root = tree.getroot()
    for person in root.findall('.//person'):
        name = person.text
        if contains_election_words(name):
            for block in root.findall('.//block'):
                if block.attrib['class'] == 'full_text':
                    for paragraph in block.findall('.//p'):
                        if contains_election_words(paragraph.text):
                            date = format_date(xml)
                            election_paragraphs.write(date + "///" + paragraph.text + '\n')
            break

    
def contains_election_words(text):
    return "Bush" in text or "Gore" in text


def format_date(file_path):
    file_path = file_path.name.split('\\')
    date = file_path[1] + '-' + file_path[2] + '-' + file_path[4]
    return date
            


# In[2]:


find_election_paragraphs("data")


# In[3]:


import pandas as pd

paragraphs_df = pd.read_csv('election_paragraphs.csv', delimiter = '///', engine = 'python')
paragraphs_df

