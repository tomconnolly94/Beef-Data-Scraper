#!/usr/bin/env python3
from scrapers.bbc_scraper.sub_page_scrapers.bbc_article_scraper import scrape_article # import article scraper
import globals

def scrape_bbc_home(uReq, soup, keyword_list):
    
    base_url = 'http://www.bbc.co.uk' #url to scrape
    init_path = "/news" #base url extension

    uClient = uReq(base_url + init_path)#make request for page
    page_html = uClient.read() #extract html data from request object

    page_soup = soup(page_html, "html.parser") #convert the html to a soup object
    raw_html = page_soup.findAll("div", {"class" : "gs-c-promo"}) #find tags in the soup object

    print(len(raw_html))

    if len(raw_html) > 0: #only execute if tags have been found

        beef_objects = []
        
        for x in range(0, len(raw_html)): #for each tag

                print(x) #print index for reference
                print(" ") #print seperator

                if(raw_html[x].a): #ensure the element has an anchor tag

                    if("http://" in raw_html[x].a["href"]): #check if the a href is an absolute url or an absolute path
                        sub_page_url = raw_html[x].a["href"]

                    else:
                        sub_page_url = base_url + raw_html[x].a["href"]

                    print(sub_page_url)

                    beef_objects.append(scrape_article(sub_page_url, uReq, soup, keyword_list)) #scrape this article

                else:
                    print(globals.err_prefix + "element has no anchor tag")
    else:
            print(globals.err_prefix + "tag not found")

    #dispose
    uClient.close()
