#!/usr/bin/env python3
import globals #import globals file
import re
import demjson
from objects.beef_object import BeefObject
from text_extraction.extract_names import extract_names
from text_extraction.extract_quotes import extract_quotes

def scrape_article(path, uReq, soup, keyword_list):
    sub_page_html = uReq(path).read()
    sub_page_soup = soup(sub_page_html, "html.parser")
    
    content_tag_array = sub_page_soup.findAll("div", {"class" : "container"}) #find tags in the soup object
    
    print(content_tag_array)
    
    #relevant_story = None;
    
    
    
    
    #return beef_obj