# globals.py

def init():
    
    #define globals
    global err_prefix
    global db_connection
    global blacklisted_urls
    
    #assign globals
    err_prefix = "Error: "
    blacklisted_urls = {} #initialise the blacklist for storing URLS that cause problems
    

def get_month_number(month_string):
    
    months = { "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12,}
    
    return months[month_string]

def scrub_content_text(text):
    
    import re
    result_w_double_white_space = re.sub("[\(\[].*?[\)\]]", "", text).strip()
    result = " ".join(result_w_double_white_space.split())

    return result