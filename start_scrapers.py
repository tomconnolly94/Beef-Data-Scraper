#!/usr/bin/env python3
#imports
import sys
import time
import os
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import globals #import globals file
#interface imports
from interfaces.database.event_interfacing.insert_event_into_db import insert_loop #import db insert function
from interfaces.database.db_interface import remove_expired_events
from interfaces.database.url_preloading.saved_scraped_url_access import get_all_saved_urls #import preload url function
#import home scraper functions
from scrapers.bbc_scraper.bbc_home import scrape_bbc_home #import bbc home scraper
from scrapers.bet_scraper.bet_home import scrape_bet_home #import bbc home scraper
from scrapers.bossip_scraper.bossip_home import scrape_bossip_home #import bbc home scraper
from scrapers.cnn_scraper.cnn_home import scrape_cnn_home #import cnn home scraper
from scrapers.give_me_sport_scraper.give_me_sport_home import scrape_give_me_sport_home #import cnn home scraper
from scrapers.hip_hop_beef_scraper.hip_hop_beef_home import scrape_hip_hop_beef_home #import hip hop beef home scraper
from scrapers.hiphopdx_scraper.hiphopdx_home import scrape_hiphopdx_home #import hip hop dx home scraper
from scrapers.hot_new_hip_hop_scraper.hot_new_hip_hop_home import scrape_hot_new_hip_hop_home #import hip hop dx home scraper
#import classification init function
from decision_logic.beef_object_filter import initialise_classification_module #import classification module initialisation
from dotenv import load_dotenv, find_dotenv #import environment variable handling functions

#load environment variables
load_dotenv(find_dotenv())

globals.init() #initiate globals
loop = True

print("Training classification module...")

#initialise the text classification script for use later on
initialise_classification_module()

print("Complete.")

#define keyword lists for scrapers to use
broad_keyword_list = ("beef", "conflict", "fight", "disagree", "rebuff", "counter-", "argument", "argue", "communications", "feud", "calls", "Hurricane")
cnn_keyword_list = ("conflict", "argument", "feud")
empty_keyword_list = ()

#scraper loop
while loop:
    
    print("Preparing...")
    
    #loop through blacklist, decrease timeout counts and remove the paths with timeout counts at 0
    for path in list(globals.blacklisted_urls):
        
        if globals.blacklisted_urls[path] == 0:
            del globals.blacklisted_urls[path]
        else:
            globals.blacklisted_urls[path] = globals.blacklisted_urls[path] - 1
        
    #check expired events, remove any unecessary data
    remove_expired_events()
    
    #start scraping
    print("Scraping BBC...")
    insert_loop(scrape_bbc_home(uReq, soup, empty_keyword_list))
    print("BBC Scraped.")
    
    print("Scraping BET...")
    insert_loop(scrape_bet_home(uReq, soup, empty_keyword_list))
    print("BET Scraped.")
    
    print("Scraping Bossip...")
    insert_loop(scrape_bossip_home(uReq, soup, empty_keyword_list))
    print("Bossip Scraped.")
    
    print("Scraping CNN...")
    insert_loop(scrape_cnn_home(uReq, soup, empty_keyword_list))
    print("CNN Scraped.")
    
    print("Scraping Give me Sport...")
    insert_loop(scrape_give_me_sport_home(uReq, soup, empty_keyword_list))
    print("Give me Sport Scraped.")
    
    print("Scraping Hip Hop Beef...")
    insert_loop(scrape_hip_hop_beef_home(uReq, soup, empty_keyword_list))
    print("Hip Hop Beef Scraped")
    
    print("Scraping Hip Hop DX...")
    insert_loop(scrape_hiphopdx_home(uReq, soup, empty_keyword_list))
    print("Hip Hop DX Scraped")
    
    print("Scraping Hot New Hip Hop...")
    insert_loop(scrape_hot_new_hip_hop_home(uReq, soup, empty_keyword_list))
    print("Hot New Hip Hop Scraped")
    
    #initiate hold sequence to prevent over-scraping
    sleep_secs = 300 # 5 minutes
    
    print("Sleeping for " + str(sleep_secs) + " seconds")
    time.sleep(sleep_secs)