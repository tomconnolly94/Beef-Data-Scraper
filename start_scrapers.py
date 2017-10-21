#!/usr/bin/env python3
#imports
import sys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from scrapers.bbc_scraper.bbc_home import scrape_bbc_home # import bbc home scraper
from scrapers.cnn_scraper.cnn_home import scrape_cnn_home # import cnn home scraper
from scrapers.hip_hop_beef_scraper.hip_hop_beef_home import scrape_hip_hop_beef_home # import hip hop beef home scraper
from scrapers.hiphopdx_scraper.hiphopdx_home import scrape_hiphopdx_home # import hip hop dx home scraper
from interfaces.database.insert_into_db import insert_if_not_exist # import db insert function
import globals #import globals file

globals.init()

#keyword_list = ("beef", "conflict", "fight", "disagree", "rebuff", "counter-argument", "argue", "communications", "feud", "calls", "Hurricane")
keyword_list = ()

file_name = "title_record.txt"

def insert_loop(beef_objects):

    for beef_object in beef_objects:
        insert_if_not_exist(beef_object)
'''        
#scraper loop
while True:
    
    for path in list(globals.blacklisted_urls): #loop through blacklist, decrease timeout counts and remove the paths with timeout counts at 0
        
        if globals.blacklisted_urls[path] == 0:
            del globals.blacklisted_urls[path]
        else:
            globals.blacklisted_urls[path] = globals.blacklisted_urls[path] - 1
    
    print("Scraping BBC...")
    insert_loop(scrape_bbc_home(uReq, soup, keyword_list))
    print("BBC Scraped.")
    print("Scraping CNN...")
    insert_loop(scrape_cnn_home(uReq, soup, keyword_list))
    print("CNN Scraped.")
    print("Scraping HHB...")
    insert_loop(scrape_hip_hop_beef_home(uReq, soup, keyword_list))
    print("HHB Scraped")
'''

scrape_hiphopdx_home(uReq, soup, keyword_list)