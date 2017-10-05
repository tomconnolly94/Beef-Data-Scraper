#!/usr/bin/env python3
#imports
import globals #import globals file
import re
import demjson
from interfaces.url_access.url_access import access_url
from scrapers.hip_hop_beef_scraper.sub_page_scrapers.hip_hop_beef_article_scraper import scrape_article # import article scraper
from scrapers.hip_hop_beef_scraper.sub_page_scrapers.hip_hop_beef_video_scraper import scrape_video # import article scraper

def scrape_hip_hop_beef_home(uReq, soup, keyword_list):
    
    base_url = 'http://hiphopbeef.com/' #url to scrape
    
    raw_page_html = access_url(base_url, uReq)#make request for page

    page_soup = soup(raw_page_html, "html.parser") #convert the html to a soup object
    
    news_tag_array = page_soup.find("div", {"class", "latest_news"})#, text=pattern) #find tags in the soup object
    news_tag_array = news_tag_array.findAll("li")#, text=pattern) #find tags in the soup object

    beef_objects = []
    
    if len(news_tag_array) > 0: #only execute if tags have been found
        
        for tag in news_tag_array:
            a = tag.find("a")
            
            if a and a["href"]:
                print(a["href"])
                beef_object = scrape_article(a["href"], uReq, soup, keyword_list)
                
                if beef_object != None:
                    beef_objects.append(beef_object)
                    #beef_object.print_beef()
    
    video_tag_array = page_soup.find("div", {"class", "items_list"})#, text=pattern) #find tags in the soup object
    video_tag_array = video_tag_array.findAll("li")#, text=pattern) #find tags in the soup object
    
    if len(video_tag_array) > 0: #only execute if tags have been found
        
        for tag in video_tag_array:
            a = tag.find("a")
            
            if a and a["href"]:
                print(a["href"])
                beef_object = scrape_video(a["href"], uReq, soup, keyword_list)
                
                if beef_object != None:
                    beef_objects.append(beef_object)
                    #beef_object.print_beef()
                    break;
                    
    return beef_objects
    #dispose
    uClient.close()