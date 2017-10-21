#!/usr/bin/env python3
#imports
import globals #import globals file
import re
import demjson
from interfaces.url_access.url_access import access_url
from scrapers.hiphopdx_scraper.sub_page_scrapers.hiphopdx_article_scraper import scrape_article # import article scraper

def scrape_hiphopdx_home(uReq, soup, keyword_list):
    
    base_url = 'https://hiphopdx.com/news' #url to scrape

    

    raw_page_html = access_url(base_url, uReq)#make request for page

    if raw_page_html is not None:

        #print(raw_page_html)
        
        page_soup = soup(raw_page_html, "html.parser") #convert the html to a soup object

        news_tag_array = page_soup.find("div", {"class", "content"})#, text=pattern) #find tags in the soup object
        
        print(len(news_tag_array))

        beef_objects = []

        if len(news_tag_array) > 0: #only execute if tags have been found

            for tag in news_tag_array:
                                
                if tag and hasattr(tag, "div") and hasattr(tag.div, "div") and tag.div and tag.div.div and tag.div.div.h2 and tag.div.div.h2.text:

                    print(tag)
                    print("go")

                    news_identifier = tag.div.div.h2.text
                    
                    if news_identifier == "HipHopDX ":
                        
                        
                        news_tag_array = tag.find("a")#, text=pattern) #find tags in the soup object
                        
                        print(news_tag_array)
                        print(len(news_tag_array))
                        
                        #beef_object = scrape_article(a["href"], uReq, soup, keyword_list)
                    
                    

                    if beef_object != None:
                        beef_objects.append(beef_object)
                
        video_tag_array = page_soup.find("div", {"class", "items_list"})#, text=pattern) #find tags in the soup object
        video_tag_array = video_tag_array.findAll("li")#, text=pattern) #find tags in the soup object

        if len(video_tag_array) > 0: #only execute if tags have been found

            for tag in video_tag_array:
                a = tag.find("a")

                if a and a["href"]:
                    beef_object = scrape_video(a["href"], uReq, soup, keyword_list)

                    if beef_object != None:
                        beef_objects.append(beef_object)
                        break;
        
        return beef_objects
    else:
        return []    