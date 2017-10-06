#!/usr/bin/env python3
import globals #import globals file
import re
import demjson
from interfaces.url_access.url_access import access_url
from objects.beef_object import BeefObject
from text_extraction.extract_names import extract_names
from text_extraction.extract_quotes import extract_quotes

def scrape_video(path, uReq, soup, keyword_list):
    
    
    sub_page_html = access_url(path, uReq)
        
        
    if sub_page_html is not None:
    
        sub_page_soup = soup(sub_page_html, "html.parser")
        
        title_tag_array = sub_page_soup.findAll("div", {"class" : "page_header"}) #find tags in the soup object
        media_tag_array = sub_page_soup.findAll("iframe") #find tags in the soup object

        content_string = ""
        img_link = ""

        if len(title_tag_array) > 0 and title_tag_array[0] and title_tag_array[0].div and title_tag_array[0].div.img:
            img_link = title_tag_array[0].div.img["src"]

        #relevant_story = None;

        date_string = sub_page_soup.find("span", {"class" : "date"}).text.replace("Posted on: ", "") #find tags in the soup object

        actors_list = extract_names(title_tag_array[0].h1.text) #extract actors from content_string
        highlights = extract_quotes(title_tag_array[0].h1.text) #extract quotes from content_string
        categories = [1]

        media_link = ""

        if len(media_tag_array) > 0:
            media_link = media_tag_array[0]["src"]

        #frame BeefObject( title, relevant_actors, content, date, highlights, data_source, categories, img_title)
        beef_obj = BeefObject(title_tag_array[0].h1.text, actors_list, content_string, date_string, highlights, path, categories, img_link, media_link) #create beefObject 

        return beef_obj
    else:
        return None