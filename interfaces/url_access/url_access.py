#imports
import urllib
import globals

def access_url(path, uReq):
    
    page_html = None
    
    if path not in globals.blacklisted_urls: #check path is not blacklisted
    
        try:

            page_html = uReq(path).read() #request url
            
        except urllib.error.URLError: #handle any access errors, sometimes caused by too many requests to a domain

            print("URLError thrown, handling initiated.")
            print("##############################################################################")
            globals.blacklisted_urls[path] = 20 #add path to dictionary and wait 20 loops before requesting it again
            return None

        else:
            return page_html
        
    else:
        print("This path is blacklisted: " + path)
        print("Timeout value is at: " + str(globals.blacklisted_urls[path]))
        return None
