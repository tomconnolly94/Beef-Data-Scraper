#!/usr/bin/env python3
#imports
import globals #import globals file
import re
import demjson
#interface imports
from interfaces.url_access.url_access import access_url
from interfaces.database.url_preloading.saved_scraped_url_access import save_url # import save url function
from interfaces.database.url_preloading.saved_scraped_url_access import get_saved_urls # import preload url function
#scraper imports
from scrapers.hot_new_hip_hop_scraper.sub_page_scrapers.hot_new_hip_hop_article_scraper import scrape_article # import article scraper

def scrape_hot_new_hip_hop_home(uReq, soup, keyword_list):
    
    base_url = 'http://hotnewhiphop.com' #url to scrape

    initial_suffix = "/tags/beef/news"

    raw_page_html = access_url(base_url + initial_suffix, uReq)#make request for page
        
    if raw_page_html is not None:
        
        page_soup = soup(raw_page_html, "html.parser") #convert the html to a soup object

        news_tag_array = page_soup.findAll("li", {"class", "endlessScrollCommon-list-item"})#, text=pattern) #find tags in the soup object
        
        beef_objects = []
            
        #load saved urls
        saved_urls = get_saved_urls(base_url)

        if len(news_tag_array) > 0: #only execute if tags have been found
            
            for news_tag in news_tag_array:
                
                if news_tag and news_tag.div and news_tag.div.a and news_tag.div.a["href"]:
                    
                    sub_page_url = base_url + news_tag.div.a["href"]

                    if any(url_obj["url"] == sub_page_url for url_obj in saved_urls): #check through pre loaded urls to ensure url has not already been scraped
                        print("preloaded url found, aborting scrape.")

                    else:

                        beef_object = scrape_article(sub_page_url, uReq, soup, keyword_list)                

                        save_url(base_url, sub_page_url)
                            
                        if beef_object != None:
                            beef_objects.append(beef_object)

        return beef_objects
    else:
        return []
    