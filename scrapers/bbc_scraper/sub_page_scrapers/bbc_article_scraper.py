#!/usr/bin/env python3
import globals #import globals file
import re
import demjson
from objects.beef_object import BeefObject
from interfaces.url_access.url_access import access_url
from text_extraction.text_extraction_helper_functions import extract_names
from text_extraction.text_extraction_helper_functions import extract_quotes
from interfaces.database.event_interfacing.insert_event_into_db import store_event_classification

def scrape_article(path, uReq, soup, keyword_list):

    sub_page_html = access_url(path, uReq)
        
    if sub_page_html is not None:

        sub_page_soup = soup(sub_page_html, "html.parser")

        content_tag_array = sub_page_soup.findAll("div", {"class" : "story-body__inner"}) #find tags in the soup object

        relevant_story = None;

        if len(content_tag_array) > 0:
            
            content_string = "" #init content string

            #check each p tag found for words from the keyword list
            for p in content_tag_array[0].findAll('p'):
                
                content_string += p.text

                if(len(keyword_list) > 0): #if keyword list has values, use them to filter stories, if it is empty, automatically approve story

                    #check if any text from page contains key words stored in list, if keyword found, print page text
                    if(any(keyword in p.text for keyword in keyword_list)):
                        relevant_story = True
                        #break

                else:
                    relevant_story = True

            #clean content string
            globals.scrub_content_text(content_string)
                    
            title = sub_page_soup.findAll("h1", {"class" : "story-body__h1"})[0].text #find tags in the soup object for beef object title
            
            #article is relevant, build a beef record
            if relevant_story: #execute if a story contains a keyword
                
                store_event_classification(title, content_string) #classify event and store the classification for later use
                
                mini_info_panel_tag_array = sub_page_soup.findAll("li", {"class" : "mini-info-list__item"})#find tags in the soup object for beef object date
                date_string_split = mini_info_panel_tag_array[0].div["data-datetime"].split(" ")#format date
                date_string = str(date_string_split[0]) + "/" + str(globals.get_month_number(date_string_split[1])) + "/" + str(date_string_split[2])
                
                actors_list = extract_names(content_string) #extract actors from content_string
                highlights = extract_quotes(content_string) #extract quotes from content_string

                categories = []

                if len(mini_info_panel_tag_array) > 1 and mini_info_panel_tag_array[1].a is not None and mini_info_panel_tag_array[1].a.text is not None:

                    category = mini_info_panel_tag_array[1].a.text

                    if "politics" in category.lower():
                        categories.append(2)

                    if "sport" in category.lower():
                        categories.append(4)

                    if "technology" in category.lower():
                        categories.append(6)

                img_tag_array = sub_page_soup.findAll("span", {"class" : "image-and-copyright-container"}) #find tags in the soup object

                img_link = ""

                if len(img_tag_array) > 0:
                    if img_tag_array[0].div: #if article contains references to images, extract the first one
                        img_link = img_tag_array[0].div["data-src"]
                    elif img_tag_array[0].img:
                        img_link = img_tag_array[0].img["src"]

                media_link = {
                    "link": "",
                    "type": ""                    
                }
                
                media_tag_array = sub_page_soup.findAll("figure", {"class" : "media-player"})
                                
                if len(media_tag_array) == 1:
                    link_json = demjson.decode(media_tag_array[0]["data-playable"])
                    
                    link = link_json["settings"]["externalEmbedUrl"]
                
                    link_type = ""

                    if "youtube" in link:
                        link_type = "youtube"
                    elif "spotify" in link:
                        link_type = "spotify"
                    elif "soundcloud" in link:
                        link_type = "soundcloud"
                    elif "twitter" in link:
                        link_type = "twitter"
                    elif "bbc" in link:
                        link_type = "bbc_embed"

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