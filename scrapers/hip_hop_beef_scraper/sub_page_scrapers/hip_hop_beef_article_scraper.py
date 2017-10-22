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

        content_tag_array = sub_page_soup.findAll("div", {"class" : "page-content"}) #find tags in the soup object
        title_tag_array = sub_page_soup.findAll("div", {"class" : "page_header"}) #find tags in the soup object
        media_tag_aray = sub_page_soup.findAll("iframe") #find tags in the soup object

        content_string = ""
        img_link = ""

        for p in content_tag_array[0].findAll("p"):

            if p.a is None:
                content_string += p.text
            elif p.a.img is not None and p.a.img["src"] is not None:
                img_link = p.a.img["src"]

        #relevant_story = None;

        date_string = sub_page_soup.find("span", {"class" : "date"}).text.replace("Posted ", "") #find tags in the soup object
        date_split = date_string.split("/")
        date_string = date_split[1] + "/" + date_split[0] + "/" + date_split[2]


        actors_list = extract_names(content_string) #extract actors from content_string
        highlights = extract_quotes(content_string) #extract quotes from content_string
        categories = [1]

        media_link = ""

        if len(media_tag_aray) > 0:
            link = media_tag_aray[0]["src"]
            link_type = ""
        
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
        beef_obj = BeefObject(title_tag_array[0].h2.text, actors_list, content_string, date_string, highlights, path, categories, img_link, media_link) #create beefObject 

        return beef_obj
    else:
        return None