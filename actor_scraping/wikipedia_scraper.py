#!/usr/bin/env python3
#imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
#from interfaces.insert_into_db import insert_if_not_exist # import db insert function
#import globals #import globals file

#globals.init()

actor_name = "Thomas Michael Andrew Connolly"

def scrape_actor_from_wiki(uReq, soup, actor_name):
    
    actor_name = actor_name.lower()
    actor_name_split = actor_name.split(" ")
    
    actor_name_us = actor_name_split[0]
    
    for index, name in enumerate(actor_name_split):
        if index != 0:
            actor_name_us += "_" + name
    
    base_url = 'https://en.wikipedia.org/wiki/' #url to scrape
    
    op_url = base_url + actor_name_us
    
    print(op_url)
    
    uClient = uReq(base_url)#make request for page
    page_html = uClient.read() #extract html data from request object

    page_soup = soup(page_html, "html.parser") #convert the html to a soup object
    print(page_html)
    #raw_html = page_soup.findAll("div", {"class" : "gs-c-promo"}) #find tags in the soup object






scrape_actor_from_wiki(uReq, soup, actor_name)