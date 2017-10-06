# globals.py

def init():
    
    #define globals
    global err_prefix
    global db_connection
    global blacklisted_urls
    
    #assign globals
    err_prefix = "Error: "
    blacklisted_urls = {} #initialise the blacklist for storing URLS that cause problems
    
    