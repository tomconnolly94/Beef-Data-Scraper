#!/usr/bin/env python3
#imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from scrapers.bbc_scraper.bbc_home import scrape_bbc_home # import bbc home scraper
from scrapers.cnn_scraper.cnn_home import scrape_cnn_home # import cnn home scraper
import globals #import globals file

globals.init()

keyword_list = ("beef", "conflict", "fight", "disagree", "rebuff", "counter-argument", "argue", "communications", "feud", "calls")

#scrape_bbc_home(uReq, soup, keyword_list)
scrape_cnn_home(uReq, soup, keyword_list)