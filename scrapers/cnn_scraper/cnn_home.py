#!/usr/bin/env python3
import globals #import globals file
import re
import demjson
#interface imports
from interfaces.url_access.url_access import access_url
from interfaces.database.url_preloading.saved_scraped_url_access import save_url # import save url function
from interfaces.database.url_preloading.saved_scraped_url_access import get_saved_urls # import preload url function
#scraper imports
from scrapers.cnn_scraper.sub_page_scrapers.cnn_article_scraper import scrape_article # import article scraper

def scrape_cnn_home(uReq, soup, keyword_list):
    
    logging = None
    
    base_url = 'http://edition.cnn.com' #url to scrape
    
    raw_page_html = access_url(base_url, uReq)#make request for page
    
    if raw_page_html is not None:
        
        print(raw_page_html)

        page_soup = soup(raw_page_html, "html.parser") #convert the html to a soup object
        tag_array = page_soup.findAll("script")#, text=pattern) #find tags in the soup object

        if len(tag_array) > 0: #only execute if tags have been found

            if(tag_array[10].text): #ensure the element has an anchor tag

                beef_objects = []
            
                #load saved urls
                saved_urls = get_saved_urls(base_url)

                script_text = tag_array[10].text
                print(script_text)
                result = re.search('CNN.contentModel = (.*);', script_text)
                if(result.group):
                    script_json = demjson.decode(result.group(1))

                    percent_per_scrape = 100/len(script_json['siblings']['articleList'])

                    for x in range(0, len(script_json['siblings']['articleList'])): #for each tag

                        print(str(round(x * percent_per_scrape)) + "% complete.")

                        sub_page_url = base_url + script_json['siblings']['articleList'][x]['uri']

                        if any(url_obj["url"] == sub_page_url for url_obj in saved_urls): #check through pre loaded urls to ensure url has not already been scraped
                            if logging:
                                print("preloaded url found, aborting scrape.")

                        else:
                            if logging:
                                print("preloaded url not found, initiating scrape.")

                            #url must be saved under these conditions: 1. it has not been previously scraped, 2. it may not be relevant to beef and therefore may not be added to selected events, 
                            save_url(base_url, sub_page_url)

                            beef_object = scrape_article(sub_page_url, uReq, soup, keyword_list)

                            if beef_object != None:
                                beef_objects.append(beef_object)

                    return beef_objects
                else:
                    return []   
    else:
        return []   