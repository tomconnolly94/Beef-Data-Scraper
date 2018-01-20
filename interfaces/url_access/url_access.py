#imports
import urllib.request as urllib_req
import urllib
import globals

def access_url(path, uReq):
    
    page_html = None
    
    if path not in globals.blacklisted_urls: #check path is not blacklisted
    
        try:
            hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding': 'none',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Connection': 'keep-alive'}
            
            req = urllib_req.Request(path, headers=hdr)
            page_html = uReq(req).read() #request url
            
        except urllib.error.URLError: #handle any access errors, sometimes caused by too many requests to a domain

            print("URLError thrown. Adding " + path + " to blacklist.")
            globals.blacklisted_urls[path] = 5 #add path to dictionary and wait 20 loops before requesting it again
            return None

        else:
            return page_html
        
    else:
        print("This path is blacklisted: " + path)
        print("Timeout value is at: " + str(globals.blacklisted_urls[path]))
        return None
