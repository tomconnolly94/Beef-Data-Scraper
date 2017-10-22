#!/usr/bin/env python3
import globals #import globals file
import re
import demjson
from interfaces.url_access.url_access import access_url
from objects.beef_object import BeefObject
from text_extraction.extract_names import extract_names
from text_extraction.extract_quotes import extract_quotes

def scrape_article(path, uReq, soup, keyword_list):
    
    sub_page_html = access_url(path, uReq)
    
    if sub_page_html is not None:
            
        sub_page_soup = soup(sub_page_html, "html.parser")

        header_tag = sub_page_soup.find("div", {"class" : "article-header"}) #find tags in the soup object
        body_tag = sub_page_soup.find("div", {"class" : "article-body"}) #find tags in the soup object

        #print(body_tag)
        
        if header_tag and header_tag.div and header_tag.div.h1 and header_tag.div.text:
            title = header_tag.div.h1.text
        else:
            print(header_tag)
        
        content_string = ""

        for p in body_tag.findAll("p"):

            if p is not None:
                content_string += p.text
        
        header_divs = header_tag.findAll("div")

        img_link = ""
        
        if header_divs[3].img:
            img_link = header_divs[3].img["src"]
        
        #relevant_story = None;
        
        date_string = header_tag.find("div", {"class" : "date"}).text.replace("\n", "") #find tags in the soup object
        date_split = date_string.split(", ") #split to get month and day in slot [0] and year and rest of string in [1]
        secondary_date_split = date_split[0].split(" ") #split to seperate month and day
        tertiary_date_split = date_split[1].split(" ")
        
        final_date_string = str(secondary_date_split[1]) + "/" + str(globals.get_month_number(secondary_date_split[0])) + "/" + str(tertiary_date_split[0])
        
        actors_list = extract_names(content_string) #extract actors from content_string
        highlights = extract_quotes(content_string) #extract quotes from content_string
        categories = [1]

        link_raw = body_tag.findAll("iframe")
        link = ""
        link_type = ""
        
        if len(link_raw) > 0:
            link = link_raw[0]["src"]

            if "youtube" in link:
                link_type = "youtube"
            elif "spotify" in link:
                link_type = "spotify"
            elif "soundcloud" in link:
                link_type = "soundcloud"
            elif "twitter" in link:
                link_type = "twitter"

        media_link = {
            "link": link,
            "type": link_type 
        }

        #frame BeefObject( title, relevant_actors, content, date, highlights, data_source, categories, img_title)
        beef_obj = BeefObject(title, actors_list, content_string, final_date_string, highlights, path, categories, img_link, media_link) #create beefObject 
        
        #beef_obj.print_beef()

        return beef_obj
        
    else:
        return None