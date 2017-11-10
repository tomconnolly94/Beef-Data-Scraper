#!/usr/bin/env python3
#imports
import sys
from datetime import datetime
#interface imports
from interfaces.database.db_config import open_db_connection
from interfaces.database.insert_into_db import insert_if_not_exist
from interfaces.database.insert_into_db import get_objects_from_db_table

saved_urls = ()

def save_url(source, url):
    
    document = ({
        "url" : url,
        "source" : source, 
        "event_date" : datetime.utcnow(),
    })

    insert_if_not_exist(document, "scraped_url_store")

    
def get_saved_urls(source):
        
    saved_urls = get_objects_from_db_table("scraped_url_store", "source", source)

def check_url_history(target, source):
    
    saved_urls = get_saved_urls(source)
    
    return any(url_obj["url"] == target for url_obj in saved_urls)