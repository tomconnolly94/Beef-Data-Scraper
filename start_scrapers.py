#!/usr/bin/env python3
#imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from scrapers.bbc_scraper.bbc_home import scrape_bbc_home # import bbc home scraper
from scrapers.cnn_scraper.cnn_home import scrape_cnn_home # import cnn home scraper
import globals #import globals file

globals.init()

keyword_list = ("beef", "conflict", "fight", "disagree", "rebuff", "counter-argument", "argue", "communications", "feud", "calls", "Hurricane")

file_name = "title_record.txt"

def unique_write_to_file(text, file):
    r_file = open(file, "r")
    line_found = None
    
    for line in r_file:

        if line == text + "\n" or line == text:
            line_found = True
            break
        
    r_file.close()
    
    if line_found is None:
        w_file = open(file, "a")
        w_file.write(str("\n" + text))
        w_file.close()
    
while True:

    beef_objects = scrape_bbc_home(uReq, soup, keyword_list)

    for beef_object in beef_objects:
        unique_write_to_file(beef_object.title, file_name)


    beef_objects = scrape_cnn_home(uReq, soup, keyword_list)

    for beef_object in beef_objects:
        unique_write_to_file(beef_object.title, file_name)
