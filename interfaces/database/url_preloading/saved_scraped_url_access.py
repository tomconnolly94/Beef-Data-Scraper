#!/usr/bin/env python3
#imports
import sys
import datetime  
#interface imports
from interfaces.database.db_config import open_db_connection
from interfaces.database.db_interface import insert_if_not_exist
from interfaces.database.db_interface import get_objects_from_db_table

saved_urls = ()

def save_url(source, url):
    
    document = ({
        "url" : url,
        "source" : source,
        "date_added" : datetime.datetime.utcnow(),
    })

    insert_if_not_exist(document, "scraped_url_store")

    
def get_saved_urls(source):
        
    return get_objects_from_db_table("scraped_url_store", "source", source)

    
def get_all_saved_urls():
        
    return get_objects_from_db_table("scraped_url_store", "source", "")
    
    
def check_url_history(target, source):
    
    saved_urls = get_saved_urls(source)
    
    return any(url_obj["url"] == target for url_obj in saved_urls)