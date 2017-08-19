#!/usr/bin/env python3
#imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from bbc_scraper.bbc_home import scrape_bbc_home # import article scraper

keyword_list = ("beef", "conflict", "fight", "disagree", "rebuff", "counter-argument", "argue", "communications")

scrape_bbc_home(uReq, soup, keyword_list)