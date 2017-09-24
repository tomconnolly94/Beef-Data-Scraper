#!/usr/bin/env python3
#imports
import sys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from actor_scraping.wikipedia_scraper import pre_scrape_page_check
from actor_scraping.wikipedia_scraper import scrape_actor_from_wiki
import pprint
pp = pprint.PrettyPrinter(indent=4)

def scrape_actor(name):
    
    pre_scrape_check_result = pre_scrape_page_check(uReq, soup, name)

    if isinstance(pre_scrape_check_result, list):
        print(pre_scrape_check_result)

    elif isinstance(pre_scrape_check_result, str):
        return scrape_actor_from_wiki(uReq, soup, pre_scrape_check_result)["field_data_dump"]
