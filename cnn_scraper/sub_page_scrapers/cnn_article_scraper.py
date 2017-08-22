#!/usr/bin/env python3
import globals #import globals file
import re
import demjson

def scrape_article(path, uReq, soup, keyword_list):
    sub_page_html = uReq(path).read()
    sub_page_soup = soup(sub_page_html, "html.parser")

    tag_array = sub_page_soup.findAll("div", {"class" : "zn-body__paragraph"}) #find tags in the soup object
    
    relevant_story = None;
    
    if(len(tag_array) > 0): 
                
        for p in tag_array:
            #check if any text from page contains key words stored in list, if keyword found, print page text
            if(any(keyword in p.text for keyword in keyword_list)):
                relevant_story = True
                break
        
        if(relevant_story):
            return_string = ""           
            
            for p in tag_array:
                return_string += p.text
                
            print(return_string)
            #do something with string
    else:
        print(globals.err_prefix + "cnn sub page scraper cannot find tags")