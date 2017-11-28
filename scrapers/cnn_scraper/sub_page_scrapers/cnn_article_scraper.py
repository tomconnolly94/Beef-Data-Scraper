#!/usr/bin/env python3
import globals #import globals file
import re
import demjson
from objects.beef_object import BeefObject
from interfaces.url_access.url_access import access_url
from text_extraction.text_extraction_helper_functions import extract_names
from text_extraction.text_extraction_helper_functions import extract_quotes
from decision_logic.beef_object_filter import classify_event
from interfaces.database.db_interface import insert_if_not_exist

def scrape_article(path, uReq, soup, keyword_list):
    
    sub_page_html = access_url(path, uReq)
    
    if sub_page_html is not None:

        sub_page_soup = soup(sub_page_html, "html.parser")

        content_tag_array = sub_page_soup.findAll("div", {"class" : "zn-body__paragraph"}) #find tags in the soup object

        relevant_story = None;

        if(len(content_tag_array) > 0):

            content_string = "" #init content string

            #check each p tag found for words from the keyword list
            for p in content_tag_array:
                            
                content_string += p.text + " "

                if(len(keyword_list) > 0): #if keyword list has values, use them to filter stories, if it is empty, automatically approve story
                    #check if any text from page contains key words stored in list, if keyword found, print page text
                    if(any(keyword in p.text for keyword in keyword_list)):
                        relevant_story = True

            else:
                relevant_story = True

            title = sub_page_soup.findAll("h1", {"class" : "pg-headline"})[0].text #find tags in the soup object
            
            classification_result = classify_event(content_string)
            insert_if_not_exist( { "title": title, "content": content_string, "classification": classification_result["classification"] }, "all_scraped_events_with_classifications")
            
            #article is relevant, build a beef record
            if(relevant_story): #execute if a story contains a keyword
                
                date_tag_array = sub_page_soup.findAll("p", {"class" : "update-time"}) #find tags in the soup object

                split_date = date_tag_array[0].text.split(" ") #split the date string into parts
                date_string = split_date[1] + " " + split_date[5] + " " + split_date[6] + " " + split_date[7] + " " #rebuild date string with only relevant parts

                actors_list = extract_names(content_string) #extract actors from content_string

                highlights = extract_quotes(content_string) #extract quotes from content_string

                categories = []

                if "politics" in path:
                    categories.append(2)

                if "sport" in path:
                    categories.append(4)

                if "technology" in path:
                    categories.append(6)

                img_tag_array = sub_page_soup.findAll("div", {"class" : "el__image--fullwidth"}) #find tags in the soup object

                img_link = ""

                if (img_tag_array is not None) and (len(img_tag_array) > 0) and (img_tag_array[0].div) and (img_tag_array[0].div.img) and (img_tag_array[0].div.img['data-src-large']): #if article contains references to images, extract the first one
                    img_link = img_tag_array[0].div.img['data-src-large']

                media_tag_array = sub_page_soup.findAll("div", {"class" : "media__video--thumbnail-wrapper"}) #find tags in the soup object
                    
                media_link = {
                    "link": "",
                    "type": ""                    
                }
                
                if len(media_tag_array) > 0 and media_tag_array[0] and media_tag_array[0].script and media_tag_array[0].script.text:
                    
                    json_video_data = demjson.decode(media_tag_array[0].script.text)
                    link = json_video_data["embedUrl"]
                    link_type = ""

                    if "youtube" in link:
                        link_type = "youtube"
                    elif "spotify" in link:
                        link_type = "spotify"
                    elif "soundcloud" in link:
                        link_type = "soundcloud"

                    media_link = {
                        "link": link,
                        "type": link_type 
                    }
                
                #frame BeefObject( title, relevant_actors, content, date, highlights, data_source, categories, img_title)
                beef_obj = BeefObject(title, actors_list, content_string, date_string, highlights, path, categories, img_link, media_link) #create beefObject 

                return beef_obj
    else:
        return None    