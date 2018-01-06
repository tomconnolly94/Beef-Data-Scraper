#!/usr/bin/env python3
import globals #import globals file
import re
import demjson
from interfaces.url_access.url_access import access_url
from objects.beef_object import BeefObject
from text_extraction.text_extraction_helper_functions import extract_names
from text_extraction.text_extraction_helper_functions import extract_quotes
from decision_logic.beef_object_filter import classify_event
from interfaces.database.db_interface import insert_if_not_exist

def scrape_article(path, uReq, soup, keyword_list):
    
    
    sub_page_html = access_url(path, uReq)
    
    if sub_page_html is not None:
    
        sub_page_soup = soup(sub_page_html, "html.parser")

        content_tag_array = sub_page_soup.findAll("div", {"class" : "page-content"}) #find tags in the soup object
        
        relevant_story = None;
        
        if(len(content_tag_array) > 0):
            
            content_string = "" #init content string
            img_link = "" #init content string

            #check each p tag found for words from the keyword list
            for p in content_tag_array[0].findAll('p'):

                if p.a is None:
                    content_string += p.text
                elif p.a.img is not None and p.a.img["src"] is not None:
                    img_link = p.a.img["src"]

                if(len(keyword_list) > 0): #if keyword list has values, use them to filter stories, if it is empty, automatically approve story

                    #check if any text from page contains key words stored in list, if keyword found, print page text
                    if(any(keyword in p.text for keyword in keyword_list)):
                        relevant_story = True

                else:
                    relevant_story = True

            #clean content string
            globals.scrub_content_text(content_string)

            title = sub_page_soup.findAll("div", {"class" : "page_header"})[0].h2.text #find tags in the soup object
            
            #article is relevant, build a beef record
            if(relevant_story): #execute if a story contains a keyword

                classification_result = classify_event(content_string)
                insert_if_not_exist( { "title": title, "content": content_string, "classification": classification_result["classification"] }, "all_scraped_events_with_classifications")
            
                media_tag_aray = sub_page_soup.findAll("iframe") #find tags in the soup object

                date_string = sub_page_soup.find("span", {"class" : "date"}).text.replace("Posted ", "") #find tags in the soup object
                date_split = date_string.split("/")
                date_string = date_split[1] + "/" + date_split[0] + "/" + date_split[2]

                actors_list = extract_names(content_string) #extract actors from content_string
                highlights = extract_quotes(content_string) #extract quotes from content_string
                categories = [1]

                media_link = {
                    "link": "",
                    "type": ""                    
                }

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
                beef_obj = BeefObject(title, actors_list, content_string, date_string, highlights, path, categories, img_link, media_link) #create beefObject 

                return beef_obj
            else:
                return None
        else:
            return None
    else:
        return None