#!/usr/bin/env python3
#imports
import sys
import urllib
from objects.actor_object import ActorObject

# function: validate a wikipedia URL, if valid, return the URL, if not valid, return the options provided by wikipedia
def pre_scrape_page_check(uReq, soup, actor_name):
    
    actor_name_us = prepare_name(actor_name)
    
    base_url = 'https://en.wikipedia.org/wiki/' #url to scrape
    op_url = base_url + actor_name_us
        
    try:
        #make initial request for page that may not exist
        page_soup = access_page(uReq, soup, op_url)
        
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

        
# function: take a valid wikipedia url and scrape data from it to form an actor db record
def scrape_actor_from_wiki(uReq, soup, op_url):

    print(op_url)

    try:
        page_soup = access_page(uReq, soup, op_url)
        
        raw_html = page_soup.findAll("table", {"class" : "infobox"}) #find tags in the soup object

        if raw_html is not None:
            bio_rows = raw_html[0].findAll("tr")

            for row in bio_rows:
                
                if row.th is not None and row.th.text is not None:
                    print(row.th.text)
                    
                if row.td is not None and row.td.text is not None:
                    print(row.td.text)

    except urllib.error.HTTPError as err:
        if err.code == 404:
           print("404 error")
        else:
           raise
        

# function: generate a BeautifulSoup page object from a URL
def access_page(uReq, soup, op_url):
    
    uClient = uReq(op_url)#make request for page
    page_html = uClient.read() #extract html data from request object
    return soup(page_html, "html.parser") #convert the html to a soup object

# function: format a name from spaced and any caps to type recognised by wikipedia
def prepare_name(name):
    
    actor_name_split = name.split(" ")
    
    actor_name_us = actor_name_split[0]
    
    for index, name in enumerate(actor_name_split):
        if index != 0:
            if name[0] == "(":
                print("hey")
                actor_name_us += "_" + name.lower()
            else:
                actor_name_us += "_" + name.title()

    return actor_name_us
    
