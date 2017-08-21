#!/usr/bin/env python3
#imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from bbc_scraper.bbc_home import scrape_bbc_home # import bbc home scraper
from cnn_scraper.cnn_home import scrape_cnn_home # import bbc home scraper

keyword_list = ("beef", "conflict", "fight", "disagree", "rebuff", "counter-argument", "argue", "communications")

global err_prefix
err_prefix = "Error: "

#scrape_bbc_home(uReq, soup, keyword_list)
scrape_cnn_home(uReq, soup, keyword_list)