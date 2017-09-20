#!/usr/bin/env python3
#imports
import sys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from wikipedia_scraper import pre_scrape_page_check
from wikipedia_scraper import scrape_actor_from_wiki

pre_scrape_check_result = pre_scrape_page_check(uReq, soup, sys.argv[1])

if isinstance(pre_scrape_check_result, list):
    
    print("1")
    print(pre_scrape_check_result)

elif isinstance(pre_scrape_check_result, str):
    
    print("2")
    print(scrape_actor_from_wiki(uReq, soup, pre_scrape_check_result))

else:
    
    print("3")
    print("pre-scrape check returned un-recognised value")