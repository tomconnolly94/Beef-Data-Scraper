#!/usr/bin/env python3
#imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from scrapers.bbc_scraper.bbc_home import scrape_bbc_home # import bbc home scraper
from scrapers.cnn_scraper.cnn_home import scrape_cnn_home # import cnn home scraper
from interfaces.insert_into_db import insert_if_not_exist # import db insert function
import globals #import globals file

globals.init()

keyword_list = ("beef", "conflict", "fight", "disagree", "rebuff", "counter-argument", "argue", "communications", "feud", "calls", "Hurricane")

file_name = "title_record.txt"

while True:

    beef_objects = scrape_bbc_home(uReq, soup, keyword_list)

    for beef_object in beef_objects:
        insert_if_not_exist(beef_object)


    beef_objects = scrape_cnn_home(uReq, soup, keyword_list)

    for beef_object in beef_objects:
        insert_if_not_exist(beef_object)
