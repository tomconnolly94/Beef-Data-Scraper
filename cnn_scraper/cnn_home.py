#!/usr/bin/env python3
#from cnn_scraper.sub_page_scrapers.bbc_article_scraper import scrape_article # import article scraper

def scrape_cnn_home(uReq, soup, keyword_list):
    
    base_url = 'http://edition.cnn.com/' #url to scrape

    uClient = uReq(base_url)#make request for page
    raw_page_html = uClient.read() #extract html data from request object

    page_soup = soup(raw_page_html, "html.parser") #convert the html to a soup object
    tag_array = page_soup.findAll("article", {"class" : "cd--article"}) #find tags in the soup object

    print(len(tag_array))
    print(len(raw_page_html))
    print(raw_page_html)
    print(tag_array)
    
    
    if len(tag_array) > 0: #only execute if tags have been found

            for x in range(0, len(tag_array)): #for each tag
                                                                                               
                    print(x) #print index for reference
                    print(" ") #print seperator

                    if(tag_array[x].a): #ensure the element has an anchor tag

                        if("http://" in tag_array[x].a["href"]): #check if the a href is an absolute url or an absolute path
                            sub_page_url = tag_array[x].a["href"]

                        else:
                            sub_page_url = base_url + tag_array[x].a["href"]

                        print(sub_page_url)

                        scrape_article(sub_page_url, uReq, soup, keyword_list) #scrape this article

                    else:
                        print(err_prefix + "element does not have an anchor tag");
    
    else:
            print(err_prefix + "Error: tag not found");
    

    #dispose
    uClient.close()