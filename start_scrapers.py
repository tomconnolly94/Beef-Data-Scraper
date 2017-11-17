#!/usr/bin/env python3
#imports
import sys
import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import globals #import globals file
#interface imports
from interfaces.database.event_interfacing.insert_event_into_db import insert_loop # import db insert function
from interfaces.database.insert_into_db import remove_expired_events
from interfaces.database.url_preloading.saved_scraped_url_access import get_all_saved_urls # import preload url function
#import scraper function
from scrapers.bbc_scraper.bbc_home import scrape_bbc_home # import bbc home scraper
from scrapers.cnn_scraper.cnn_home import scrape_cnn_home # import cnn home scraper
from scrapers.hip_hop_beef_scraper.hip_hop_beef_home import scrape_hip_hop_beef_home # import hip hop beef home scraper
from scrapers.hiphopdx_scraper.hiphopdx_home import scrape_hiphopdx_home # import hip hop dx home scraper
from scrapers.hot_new_hip_hop_scraper.hot_new_hip_hop_home import scrape_hot_new_hip_hop_home # import hip hop dx home scraper

globals.init() #initiate globals

#define keyword lists for scrapers to use
broad_keyword_list = ("beef", "conflict", "fight", "disagree", "rebuff", "counter", "argument", "argue", "communications", "feud", "calls", "Hurricane")
cnn_keyword_list = ("conflict", "argument", "feud")
empty_keyword_list = ()

#scraper loop
while True:
    
    #loop through blacklist, decrease timeout counts and remove the paths with timeout counts at 0
    for path in list(globals.blacklisted_urls):
        
        if globals.blacklisted_urls[path] == 0:
            del globals.blacklisted_urls[path]
        else:
            globals.blacklisted_urls[path] = globals.blacklisted_urls[path] - 1
    
    
    
    #check on expired events
    remove_expired_events()    
    
    #start scraping
    
    print("Scraping BBC...")
    insert_loop(scrape_bbc_home(uReq, soup, broad_keyword_list))
    print("BBC Scraped.")
    
    print("Scraping CNN...")
    insert_loop(scrape_cnn_home(uReq, soup, cnn_keyword_list))
    print("CNN Scraped.")
    
    print("Scraping Hip Hop Beef...")
    insert_loop(scrape_hip_hop_beef_home(uReq, soup, empty_keyword_list))
    print("Hip Hop Beef Scraped")
    
    print("Scraping Hip Hop DX...")
    insert_loop(scrape_hiphopdx_home(uReq, soup, broad_keyword_list))
    print("Hip Hop DX Scraped")
    
    print("Scraping Hot New Hip Hop...")
    insert_loop(scrape_hot_new_hip_hop_home(uReq, soup, empty_keyword_list))
    print("Hot New Hip Hop Scraped")
    
    
    #initiate hold sequence to prevent over-scraping
    sleep_secs = 180
    
    print("Sleeping for " + str(sleep_secs) + " seconds")
    time.sleep(sleep_secs)
