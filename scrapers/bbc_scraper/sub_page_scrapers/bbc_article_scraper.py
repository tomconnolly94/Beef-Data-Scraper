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

    content_tag_array = sub_page_soup.findAll("div", {"class" : "story-body__inner"}) #find tags in the soup object

    relevant_story = None;
    
    if(len(content_tag_array) > 0):
        
        #check each p tag found for words from the keyword list
        for p in content_tag_array[0].findAll('p'):
            
            if(len(keyword_list) > 0): #if keyword list has values, use them to filter stories, if it is empty, automatically approve story
            
                #check if any text from page contains key words stored in list, if keyword found, print page text
                if(any(keyword in p.text for keyword in keyword_list)):
                    relevant_story = True
                    break
            
            else:
                relevant_story = True
        
        #article is relevant, build a beef record
        if(relevant_story): #execute if a story contains a keyword
            content_string = "" #init content string
            
            for p in content_tag_array[0].findAll('p'):
                content_string += p.text + " "
                
            title_tag_array = sub_page_soup.findAll("h1", {"class" : "story-body__h1"}) #find tags in the soup object for beef object title //TODO

            mini_info_panel_tag_array = sub_page_soup.findAll("li", {"class" : "mini-info-list__item"})#find tags in the soup object for beef object date //TODO

            date_string = mini_info_panel_tag_array[0].div["data-datetime"] #format date //TODO

            actors_list = extract_names(content_string) #extract actors from content_string

            highlights = extract_quotes(content_string) #extract quotes from content_string
                        
            categories = []
            
            if len(mini_info_panel_tag_array) > 1:
            
                category = mini_info_panel_tag_array[1].a.text


                if "Politics" in category:
                    categories.append(2)

                if "sport" in category:
                    categories.append(4)

                if "Technology" in category:
                    categories.append(6)
                
            img_tag_array = sub_page_soup.findAll("span", {"class" : "image-and-copyright-container"}) #find tags in the soup object
            
            img_link = ""
                        
            if len(img_tag_array) > 0:
                if img_tag_array[0].div: #if article contains references to images, extract the first one
                    img_link = img_tag_array[0].div["data-src"]
                elif img_tag_array[0].img:
                    img_link = img_tag_array[0].img["src"]
                    
                    
            #frame BeefObject( title, relevant_actors, content, date, highlights, data_source, categories, img_title)
            beef_obj = BeefObject(title_tag_array[0].text, actors_list, content_string, date_string, highlights, path, categories, img_link) #create beefObject
            
            return beef_obj