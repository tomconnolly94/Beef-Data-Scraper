#!/usr/bin/env python3
from scrapers.cnn_scraper.sub_page_scrapers.cnn_article_scraper import scrape_article # import article scraper
import globals #import globals file
import re
import demjson

def scrape_cnn_home(uReq, soup, keyword_list):
    
    base_url = 'http://edition.cnn.com' #url to scrape
    
    uClient = uReq(base_url)#make request for page
    raw_page_html = uClient.read() #extract html data from request object

    page_soup = soup(raw_page_html, "html.parser") #convert the html to a soup object
    tag_array = page_soup.findAll("script")#, text=pattern) #find tags in the soup object

    if len(tag_array) > 0: #only execute if tags have been found
        
        if(tag_array[10].text): #ensure the element has an anchor tag

            beef_objects = []
            
            script_text = tag_array[10].text
            result = re.search('CNN.contentModel = (.*);', script_text)
            script_json = demjson.decode(result.group(1))
            
            for x in range(0, len(script_json['siblings']['articleList'])): #for each tag
                                
                beef_object = scrape_article(base_url + script_json['siblings']['articleList'][x]['uri'], uReq, soup, keyword_list)

                if beef_object != None:
                    beef_objects.append(beef_object)
                    #beef_object.print_beef()
                                
            return beef_objects

    #dispose
    uClient.close()