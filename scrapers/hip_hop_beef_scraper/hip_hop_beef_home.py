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
from scrapers.hip_hop_beef_scraper.sub_page_scrapers.hip_hop_beef_article_scraper import scrape_article # import article scraper
from scrapers.hip_hop_beef_scraper.sub_page_scrapers.hip_hop_beef_video_scraper import scrape_video # import article scraper

def scrape_hip_hop_beef_home(uReq, soup, keyword_list):
    
    logging = None
    
    base_url = 'http://hiphopbeef.com/' #url to scrape
    
    raw_page_html = access_url(base_url, uReq)#make request for page

    if raw_page_html is not None:

        page_soup = soup(raw_page_html, "html.parser") #convert the html to a soup object

        news_tag_array = page_soup.find("div", {"class", "latest_news"})#, text=pattern) #find tags in the soup object
        news_tag_array = news_tag_array.findAll("li")#, text=pattern) #find tags in the soup object

        beef_objects = []
            
        #load saved urls
        saved_urls = get_saved_urls(base_url)

        if len(news_tag_array) > 0: #only execute if tags have been found

            percent_per_scrape = 100/len(news_tag_array)
            
            for x, tag in enumerate(news_tag_array):
                
                print(str(round(x * percent_per_scrape)) + "% complete.")
                
                a = tag.find("a")

                if a and a["href"]:
                    beef_object = scrape_article(a["href"], uReq, soup, keyword_list)

                    if beef_object != None:
                        beef_objects.append(beef_object)

        video_tag_array = page_soup.find("div", {"class", "items_list"})#, text=pattern) #find tags in the soup object
        video_tag_array = video_tag_array.findAll("li")#, text=pattern) #find tags in the soup object

        if len(video_tag_array) > 0: #only execute if tags have been found

            percent_per_scrape = 100/len(news_tag_array)
            
            for x, tag in enumerate(video_tag_array):
                
                print(str(round(x * percent_per_scrape)) + "% complete.")
                
                a = tag.find("a")

                if a and a["href"]:
                    
                    sub_page_url = a["href"]

                    if any(url_obj["url"] == sub_page_url for url_obj in saved_urls): #check through pre loaded urls to ensure url has not already been scraped
                        if logging:
                            print("preloaded url found, aborting scrape.")

                    else:
                        if logging:
                            print("preloaded url not found, initiating scrape.")

                        #url must be saved under these conditions: 1. it has not been previously scraped, 2. it may not be relevant to beef and therefore may not be added to selected events, 
                        save_url(base_url, sub_page_url)

                        beef_object = scrape_video(sub_page_url, uReq, soup, keyword_list)

                        if beef_object != None:
                            beef_objects.append(beef_object)
                            break;
        
        return beef_objects
    else:
        return []    