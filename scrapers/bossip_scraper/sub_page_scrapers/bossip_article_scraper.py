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

        #body_tag = sub_page_soup.find("div", {"class" : "article-content-container"}) #find tags in the soup object
        
        relevant_story = None;
        
        if sub_page_soup:
        
            content_string = "" #init content string

            #check each p tag found for words from the keyword list
            for p in sub_page_soup.findAll("p"):
                
                if p is not None and (p.a == None or "bossip" in p.a["href"]) and "Bossip Newsletter" not in p.text and "WENN" not in p.text:
                    content_string += p.text

                if p is not None and len(keyword_list) > 0: #if keyword list has values, use them to filter stories, if it is empty, automatically approve story

                    #check if any text from page contains key words stored in list, if keyword found, print page text
                    if any(keyword in p.text for keyword in keyword_list) or len(keyword_list) == 0:
                        relevant_story = True

                else:
                    relevant_story = True

            #clean content string
            globals.scrub_content_text(content_string)

            title_tag = sub_page_soup.find("h1")
            
            if title_tag and title_tag.text:
                title = title_tag.text.split("[")[0]
                
            #article is relevant, build a beef record
            if(relevant_story): #execute if a story contains a keyword

                classification_result = classify_event(content_string)
                insert_if_not_exist( { "title": title, "content": content_string, "classification": classification_result["classification"] }, "all_scraped_events_with_classifications")

                img_tag_array = sub_page_soup.findAll("img", {"class": ["size-large", "size-full"] })
                
                if len(img_tag_array) > 0 and img_tag_array[0]["src"]:
                    img_link = img_tag_array[0]["src"]
                else:
                    return None
                date_string = sub_page_soup.find("time", {"class" : "date"})["datetime"]#find tags in the soup object
                date_split = date_string.lstrip().split("-") #split to get month and day in slot [0] and year and rest of string in [1]

                final_date_string = date_split[2].split(" ")[0] + "/" + date_split[1] + "/" + date_split[0]

                actors_list = extract_names(content_string) #extract actors from content_string
                highlights = extract_quotes(content_string) #extract quotes from content_string
                categories = [1]

                link_raw = sub_page_soup.findAll("iframe")
                link = ""
                link_type = ""
                media_link = {
                    "link": "",
                    "type": "" 
                }

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
                    else:
                        link_type = "video_embed"

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