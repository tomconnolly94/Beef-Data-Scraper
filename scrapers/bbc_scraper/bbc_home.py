#!/usr/bin/env python3
import globals
#interface imports
from interfaces.url_access.url_access import access_url
from interfaces.database.url_preloading.saved_scraped_url_access import save_url # import save url function
from interfaces.database.url_preloading.saved_scraped_url_access import get_saved_urls # import preload url function
#sub scraper imports
from scrapers.bbc_scraper.sub_page_scrapers.bbc_article_scraper import scrape_article # import article scraper

def scrape_bbc_home(uReq, soup, keyword_list):
    
    logging = None
    
    base_url = 'http://www.bbc.co.uk' #url to scrape
    init_path = "/news" #base url extension
    
    page_html = access_url(base_url + init_path, uReq)#make request for page
    
    if page_html is not None:
    
        page_soup = soup(page_html, "html.parser") #convert the html to a soup object
        tag_array = page_soup.findAll("div", {"class" : "gs-c-promo"}) #find tags in the soup object

        if len(tag_array) > 0: #only execute if tags have been found

            beef_objects = []
            
            #load saved urls
            saved_urls = get_saved_urls(base_url)
            
            percent_per_scrape = 100/len(tag_array)

            for x in range(0, len(tag_array)): #for each tag
                
                print(str(round(x * percent_per_scrape)) + "% complete.")

                if(tag_array[x].a): #ensure the element has an anchor tag

                    if("http://" in tag_array[x].a["href"]): #check if the a href is an absolute url or an absolute path
                        sub_page_url = tag_array[x].a["href"]

                    else:
                        sub_page_url = base_url + tag_array[x].a["href"]
                        
                    path_split_1 = sub_page_url.split("/")#split path by /
                    path_split_2 = path_split_1[len(path_split_1) - 1 ].split("-")#get final field in path_split_1 and split by -
                    
                    if path_split_2[0] != "blogs": #ensure we are not scraping a blog page
                        
                        if any(url_obj["url"] == sub_page_url for url_obj in saved_urls): #check through pre loaded urls to ensure url has not already been scraped
                            if logging:
                                print("preloaded url found, aborting scrape.")
                        
                        else:
                            if logging:
                                print("preloaded url not found, initiating scrape.")
                                
                            #url must be saved under these conditions: 1. it has not been previously scraped, 2. it may not be relevant to beef and therefore may not be added to selected events, 
                            save_url(base_url, sub_page_url)
                            
                            beef_object = scrape_article(sub_page_url, uReq, soup, keyword_list) #scrape this article
                            
                            if beef_object != None:
                                beef_objects.append(beef_object)
                                #beef_object.print_beef()

            return beef_objects
    else:
        return []