def scrape_article(path, uReq, soup, keyword_list):
    sub_page_html = uReq(path).read()
    sub_page_soup = soup(sub_page_html, "html.parser")

    sub_page_raw_html = sub_page_soup.findAll("div", {"class" : "story-body__inner"})

    #print(sub_page_raw_html)
    
    if(len(sub_page_raw_html) > 0): 

        for p in sub_page_raw_html[0].findAll('p'):
            #check if any text from page contains key words stored in list, if keyword found, print page text
            if(any(keyword in p.text for keyword in keyword_list)):
                print(p.text)