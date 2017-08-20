#!/usr/bin/env python3
#from cnn_scraper.sub_page_scrapers.bbc_article_scraper import scrape_article # import article scraper

def scrape_cnn_home(uReq, soup, keyword_list):
    
    base_url = 'http://edition.cnn.com/' #url to scrape

    uClient = uReq(base_url)#make request for page
    page_html = uClient.read() #extract html data from request object

    page_soup = soup(page_html, "html.parser") #convert the html to a soup object
    raw_html = page_soup.findAll("h3", {"class" : "cn__listitem"}) #find tags in the soup object

    print(len(raw_html))
    print(len(page_html))
    print(raw_html)
    
    
    if len(raw_html) > 0: #only execute if tags have been found

            for x in range(0, len(raw_html)): #for each tag
                                                                                               
                    print(x) #print index for reference
                    print(" ") #print seperator

                    if(raw_html[x].a): #ensure the element has an anchor tag

                        if("http://" in raw_html[x].a["href"]): #check if the a href is an absolute url or an absolute path
                            sub_page_url = raw_html[x].a["href"]

                        else:
                            sub_page_url = base_url + raw_html[x].a["href"]

                        print(sub_page_url)

                        scrape_article(sub_page_url, uReq, soup, keyword_list) #scrape this article

    else:
            print("tag not found");
    

    #dispose
    uClient.close()