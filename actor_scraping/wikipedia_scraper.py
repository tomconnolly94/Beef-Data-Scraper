#!/usr/bin/env python3
#imports
import sys
import urllib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
#from interfaces.insert_into_db import insert_if_not_exist # import db insert function
#import globals #import globals file

#globals.init()

actor_name = sys.argv[1] #"Jon Richardson"

def pre_scrape_page_check(uReq, soup, actor_name):
    
    actor_name = actor_name.title()
    actor_name_split = actor_name.split(" ")
    
    actor_name_us = actor_name_split[0]
    
    for index, name in enumerate(actor_name_split):
        if index != 0:
            actor_name_us += "_" + name
    
    base_url = 'https://en.wikipedia.org/wiki/' #url to scrape
    
    op_url = base_url + actor_name_us
        
    try:
        #make initial request for page that may not exist
        uClient = uReq(op_url)#make request for page
        page_html = uClient.read() #extract html data from request object
        page_soup = soup(page_html, "html.parser") #convert the html to a soup object
        
        #check if page exists, or further action is required
        raw_html = page_soup.find("div", {"id" : "mw-content-text"}) #find tags in the soup object
        if raw_html is not None:
            
            if "may refer to" in raw_html.div.p.text:
                
                list_items = raw_html.div.ul.findAll("li")

                link_differentiators = []

                for list_item in list_items:
                    link_differentiators.append(list_item.a.text.replace(actor_name, ""))

                return link_differentiators
            else:
                return op_url
        else:
            print(""""div", {"id" : "mw-content-text"}" - not found""")
        
        
    except urllib.error.HTTPError as err:
        if err.code == 404:
           print("404 error")
        else:
           raise
        
def scrape_actor_from_wiki(uReq, soup, actor_name):
    print("yo")
        
        
        
print(pre_scrape_page_check(uReq, soup, actor_name))