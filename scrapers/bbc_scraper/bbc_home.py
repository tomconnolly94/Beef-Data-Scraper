#!/usr/bin/env python3
import globals
from interfaces.url_access.url_access import access_url
from scrapers.bbc_scraper.sub_page_scrapers.bbc_article_scraper import scrape_article # import article scraper

def scrape_bbc_home(uReq, soup, keyword_list):
    
    base_url = 'http://www.bbc.co.uk' #url to scrape
    init_path = "/news" #base url extension
    
    page_html = access_url(base_url + init_path, uReq)#make request for page

    page_soup = soup(page_html, "html.parser") #convert the html to a soup object
    raw_html = page_soup.findAll("div", {"class" : "gs-c-promo"}) #find tags in the soup object

    if len(raw_html) > 0: #only execute if tags have been found

        beef_objects = []
        
        for x in range(0, len(raw_html)): #for each tag

            if(raw_html[x].a): #ensure the element has an anchor tag

                if("http://" in raw_html[x].a["href"]): #check if the a href is an absolute url or an absolute path
                    sub_page_url = raw_html[x].a["href"]

                else:
                    sub_page_url = base_url + raw_html[x].a["href"]
                    
                path_split_1 = sub_page_url.split("/")#split path by /
                path_split_2 = path_split_1[len(path_split_1) - 1 ].split("-")#get final field in path_split_1 and split by -
                
                if path_split_2[0] != "blogs": #ensure we are not scraping a blog page

                    beef_object = scrape_article(sub_page_url, uReq, soup, keyword_list) #scrape this article

                    if beef_object != None:
                        beef_objects.append(beef_object)
                        #beef_object.print_beef()

        return beef_objects

    #dispose
    uClient.close()
