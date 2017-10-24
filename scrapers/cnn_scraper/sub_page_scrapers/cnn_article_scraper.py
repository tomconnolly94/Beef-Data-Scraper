#!/usr/bin/env python3
import globals #import globals file
import re
import demjson
from objects.beef_object import BeefObject
from interfaces.url_access.url_access import access_url
from text_extraction.extract_names import extract_names
from text_extraction.extract_quotes import extract_quotes

def scrape_article(path, uReq, soup, keyword_list):
    
    sub_page_html = access_url(path, uReq)
    
    if sub_page_html is not None:

        sub_page_soup = soup(sub_page_html, "html.parser")

        content_tag_array = sub_page_soup.findAll("div", {"class" : "zn-body__paragraph"}) #find tags in the soup object

        relevant_story = None;

        if(len(content_tag_array) > 0): 

            #check each p tag found for words from the keyword list
            for p in content_tag_array:

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

                for p in content_tag_array: #parse content_tag_array and build one long string of content
                    content_string += p.text + " "

                title_tag_array = sub_page_soup.findAll("h1", {"class" : "pg-headline"}) #find tags in the soup object
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

                media_tag_array = sub_page_soup.findAll("div", {"class" : "el__image--fullwidth"}) #find tags in the soup object

                img_link = ""

                if (media_tag_array is not None) and (len(media_tag_array) > 0) and (media_tag_array[0].div) and (media_tag_array[0].div.img) and (media_tag_array[0].div.img['data-src-large']): #if article contains references to images, extract the first one
                    img_link = media_tag_array[0].div.img['data-src-large']

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

                
                '''
                if len(media_tag_array) > 0 and media_tag_array[0].div.video: #if article contains references to images, extract the first one
                    script_text = tag_array[10].text
                    result = re.search('CNN.contentModel = (.*);', script_text)
                    script_json = demjson.decode(result.group(1))
                    media_link = media_tag_array[0].div.video['data-src-large']
                '''
                #frame BeefObject( title, relevant_actors, content, date, highlights, data_source, categories, img_title)
                beef_obj = BeefObject(title_tag_array[0].text, actors_list, content_string, date_string, highlights, path, categories, img_link, media_link) #create beefObject 

                return beef_obj
    else:
        return None    