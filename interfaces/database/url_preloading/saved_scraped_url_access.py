#!/usr/bin/env python3
#imports
import sys
from datetime import datetime
#interface imports
from interfaces.database.db_config import open_db_connection
from interfaces.database.insert_into_db import insert_if_not_exist
from interfaces.database.insert_into_db import get_objects_from_db_table
from interfaces.database.insert_into_db import remove_expired_events

def save_url(source, url):
    
    document = ({
        "url" : url,
        "source" : source, 
        "event_date" : datetime.utcnow(),
    })

    insert_if_not_exist(document, "scraped_url_store")

    
def get_saved_urls(source):
    
    #check on expired events
    remove_expired_events()
    
    return get_objects_from_db_table("scraped_url_store", "source", source)