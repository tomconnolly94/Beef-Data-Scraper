#!/usr/bin/env python3
#imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys #make sub directory accessible
from sub_page_scrapers.bbc_article_scraper import scrape_article # import article scraper

base_url = 'http://www.bbc.co.uk' #url to scrape
init_path = "/news" #base url extension

uClient = uReq(base_url + init_path)#make request for page
page_html = uClient.read() #extract html data from request object

page_soup = soup(page_html, "html.parser") #convert the html to a soup object
raw_html = page_soup.findAll("div", {"class" : "gs-c-promo"}) #find tags in the soup object

keyword_list = ("beef", "conflict", "fight", "disagree", "rebuff", "counter-argument", "argue", "communications")

print(len(raw_html))

if len(raw_html) > 0: #only execute if tags have been found

        for x in range(0, len(raw_html)): #for each tag
        
                print(x) #print index for reference
                print(" ") #print seperator
                if(raw_html[x].a):
                                        
                    if("http://" in raw_html[x].a["href"]):
                        sub_page_url = raw_html[x].a["href"]

                    else:
                        sub_page_url = base_url + raw_html[x].a["href"]

                    print(sub_page_url)

                    scrape_article(sub_page_url, uReq, soup, keyword_list)
                
else:
        print("tag not found");

#dispose
uClient.close()
