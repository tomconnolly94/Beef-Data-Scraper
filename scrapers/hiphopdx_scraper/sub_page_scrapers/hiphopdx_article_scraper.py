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

        body_tag = sub_page_soup.find("div", {"class" : "article-body"}) #find tags in the soup object
        
        relevant_story = None;

        if body_tag:
            
            content_string = "" #init content string

            #check each p tag found for words from the keyword list
            for p in body_tag.findAll('p'):

                content_string += p.text

                if(len(keyword_list) > 0): #if keyword list has values, use them to filter stories, if it is empty, automatically approve story

                    #check if any text from page contains key words stored in list, if keyword found, print page text
                    if(any(keyword in p.text for keyword in keyword_list)):
                        relevant_story = True
                        
                else:
                    relevant_story = True

            title= ""
            header_tag = sub_page_soup.find("div", {"class" : "article-header"}) #find tags in the soup object

            if header_tag and header_tag.div and header_tag.div.h1 and header_tag.div.text:
                title = header_tag.div.h1.text
                
            classification_result = classify_event(content_string)
            insert_if_not_exist( { "title": title, "content": content_string, "classification": classification_result["classification"] }, "all_scraped_events_with_classifications")

            #article is
            #article is relevant, build a beef record
            if(relevant_story): #execute if a story contains a keyword

                header_divs = header_tag.findAll("div")

                img_link = ""

                if header_divs[3].img:
                    img_link = header_divs[3].img["src"]

                #relevant_story = None;

                date_string = header_tag.find("div", {"class" : "date"}).text.replace("\n", "") #find tags in the soup object
                date_split = date_string.lstrip().split(", ") #split to get month and day in slot [0] and year and rest of string in [1]
                secondary_date_split = date_split[0].split(" ") #split to seperate month and day
                tertiary_date_split = date_split[1].split(" ") #split to seperate year from rest of string

                final_date_string = str(secondary_date_split[1]) + "/" + str(globals.get_month_number(secondary_date_split[0])) + "/" + str(tertiary_date_split[0])

                actors_list = extract_names(content_string) #extract actors from content_string
                highlights = extract_quotes(content_string) #extract quotes from content_string
                categories = [1]

                link_raw = body_tag.findAll("iframe")
                link = ""
                link_type = ""
                media_link = {
                    "link": "",
                    "type": "" 
                }

                if len(link_raw) > 0:
                    link = link_raw[0]["src"]

                    if "youtube" in link:
                        link_type = "youtube_embed"
                    elif "spotify" in link:
                        link_type = "spotify_embed"
                    elif "soundcloud" in link:
                        link_type = "soundcloud_embed"
                    elif "twitter" in link:
                        link_type = "twitter_embed"

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
        else:
            return None
    else:
        return None