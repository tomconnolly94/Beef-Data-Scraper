#!/usr/bin/env python3
#imports
import re

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
            '''
            if name[0] == "(":
                actor_name_us += "_" + name.lower()
            else:
                actor_name_us += "_" + name
            '''
            actor_name_us += "_" + name
            
    return actor_name_us
    
# function: take a date and attempt to format it in a way the beeftracker server will understand
def interpret_date(date):
    
    date_extract = re.findall('\((.*?)\)', date)
    
    if len(date_extract) > 0 and "-" in date_extract[0]:
        date_split = date_extract[0].split("-")

        if len(date_split) == 3:

            date_return = date_split[2] + "/" + date_split[1] + "/" + date_split[0]

            return date_return

        else:
            return date
    else:
        return date_extract