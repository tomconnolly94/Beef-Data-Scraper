#!/usr/bin/env python3
#imports
import globals #import globals file
import re
import demjson
from interfaces.url_access.url_access import access_url
from scrapers.hiphopdx_scraper.sub_page_scrapers.hiphopdx_article_scraper import scrape_article # import article scraper

def scrape_hiphopdx_home(uReq, soup, keyword_list):
    
    base_url = 'https://hiphopdx.com' #url to scrape

    initial_suffix = "/news"

    raw_page_html = access_url(base_url + initial_suffix, uReq)#make request for page

    if raw_page_html is not None:
        
        page_soup = soup(raw_page_html, "html.parser") #convert the html to a soup object

        news_tag = page_soup.find("div", {"class", "wire"})#, text=pattern) #find tags in the soup object

        beef_objects = []

        if len(news_tag) > 0: #only execute if tags have been found
            
            for a in news_tag.findAll("a"):
                
                if a and a["href"] and a["class"][0] != "next":
                    
                    beef_object = scrape_article(base_url + a["href"], uReq, soup, keyword_list)                

                    if beef_object != None:
                        beef_objects.append(beef_object)
                    
        return beef_objects
    else:
        return []    