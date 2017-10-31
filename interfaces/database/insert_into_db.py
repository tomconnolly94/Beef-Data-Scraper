#!/usr/bin/env python3

import time
import pymongo
import datetime
from objects.beef_object import BeefObject
from interfaces.database.db_config import open_db_connection

def insert_loop(beef_objects):
    
    print("Events Scraped: " + str(len(beef_objects)))
    insert_count = 0

    for beef_object in beef_objects:
        if insert_if_not_exist(beef_object):
            insert_count += 1
        
        
    print("Events Inserted: " + str(insert_count))


def insert_if_not_exist(beef_object):
    
    while True:
        
        logging = None
        
        if logging:
            print("DB insert attempt started for: " + beef_object.title)
        
        try:
            #open db connection
            db = open_db_connection()
            
        except pymongo.errors.NetworkTimeout:
            print("PYMONGO CONNECTION NETWORK TIMEOUT")
            print("######################################################")
        
        except pymongo.errors.AutoReconnect:
            print("PYMONGO CONNECTION AUTO RECONNECT")
            print("######################################################")
                    
        else:
            if db:
                results_current_events = db.scraped_training_events_dump_v0_1.find({ "title" : beef_object.title })
                results_historic_events = db.all_scraped_events.find({ "title" : beef_object.title })

                if results_current_events.count() < 1 and results_historic_events.count() < 1:

                    document = ({
                        "title" : beef_object.title,
                        "relevant_actors" : beef_object.relevant_actors, 
                        "description" : beef_object.content,
                        "event_date" : beef_object.date,
                        "date_added" : datetime.datetime.utcnow(),
                        "highlights" : beef_object.highlights,
                        "data_source" : beef_object.data_source,
                        "selected_categories" : beef_object.categories,
                        "img_title" : beef_object.img_title,
                        "media_link" : beef_object.media_link,
                    })

                    document_min = ({
                        "title" : beef_object.title
                    })

                    try:
                        db.scraped_training_events_dump_v0_1.insert(document)

                    except ConnectionFailure:
                        if logging:
                            print("Pymongo error, retrying db connection...")
                    except pymongo.errors.NetworkTimeout:
                        print("PYMONGO INSERT NETWORK TIMEOUT")
                        print("######################################################")
                        raise

                    except pymongo.errors.AutoReconnect:
                        print("PYMONGO INSERT AUTO RECONNECT")
                        print("######################################################")
                        raise

                    else: #execute if "try" block is successful
                        if logging:
                            print("Record inserted into main scraping table.")

                        try:
                            db.all_scraped_events.insert(document_min)

                        except ConnectionFailure:

                            if logging:
                                print("Pymongo error, retrying db connection...")

                        else: #execute if "try" block is successful

                            if logging:
                                print("Record inserted into historic scraped events table.")
                            return True    

                else:
                    if logging:
                        print("Record already exists.")
                    return None #break loop because record already exists