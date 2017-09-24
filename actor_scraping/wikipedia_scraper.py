#!/usr/bin/env python3
#imports
import sys
import urllib
import pprint
pp = pprint.PrettyPrinter(indent=4)
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

    try:
        page_soup = access_page(uReq, soup, op_url)
        
        raw_html = page_soup.findAll("table", {"class" : "infobox"}) #find tags in the soup object

        if raw_html is not None and len(raw_html) > 0:
            bio_rows = raw_html[0].findAll("tr")
            
            #init variables
            all_data = dict()
            stage_name = birth_name = nicknames = d_o_b = occupations = origin = achievements = bio = data_sources = associated_actors = links = img_title = ""

            for index, row in enumerate(bio_rows):
                
                if row.th is not None and row.th.text is not None:
                    
                    if row.td is not None and row.td.text is not None:
                        
                        all_data[row.th.text] = row.td.text
                        
                        if "birth name" in row.th.text.lower(): #get birth name
                            birth_name = row.td.text
                            
                        elif "name(s)" in row.th.text.lower(): # get nicknames
                            nicknames = row.td.text
                        
                        elif "born" in row.th.text.lower(): # get birth date and origin
                            
                            d_o_b_origin = row.td.text.split("\n")
                            
                            d_o_b = d_o_b_origin[0]
                            all_data["d_o_b"] = d_o_b
                            origin = d_o_b_origin[1]
                            all_data["Born"] = origin
                        
                        elif "occupation" in row.th.text.lower(): # get occupations
                            occupations = row.td.text

                        elif "work" in row.th.text.lower(): # get acheivements
                            achievements = row.td.text
                            
                        elif "website" in row.th.text.lower(): # get acheivements
                            links = row.td.text

            
            stage_name = page_soup.find("h1", {"id" : "firstHeading"}).text #find stage name from header
            
            bio = page_soup.findAll("div", {"class" : "mw-parser-output"})[0].p.text
            
            actor_object = ActorObject(stage_name, birth_name, nicknames, d_o_b, occupations, origin, achievements, bio, data_sources, associated_actors, links, img_title)
                   
            return { "actor_object": actor_object.toJSON(), "field_data_dump" : all_data}
                        
        return "nothing_found"
            
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
    to_be_removed = ["lady", "lord", "dame", "sir", "queen", "king", "mrs", "mr"]
    
    actor_name_us = actor_name_split[0]
    
    for index, name in enumerate(actor_name_split):
                        
        if name.lower() not in to_be_removed:
            
            if index != 0:
                if name[0] == "(":
                    actor_name_us += "_" + name.lower()
                else:
                    actor_name_us += "_" + name.title()

    print(actor_name_us)
    return actor_name_us
    
