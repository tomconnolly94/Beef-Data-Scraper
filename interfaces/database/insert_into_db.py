#!/usr/bin/env python3

from interfaces.database.db_config import open_db_connection
import time
from objects.beef_object import BeefObject

def insert_if_not_exist(beef_object):
    
    while True:
        
        logging = None
        
        if logging:
            print("DB insert attempt started for: " + beef_object.title)
        
        #open db connection
        db = open_db_connection()

        results_current_events = db.scraped_training_events_dump_v0_1.find({ "title" : beef_object.title })
        results_historic_events = db.all_scraped_events.find({ "title" : beef_object.title })

        if results_current_events.count() < 1 and results_historic_events.count() < 1:

            document = ({
                "title" : beef_object.title,
                "relevant_actors" : beef_object.relevant_actors, 
                "description" : beef_object.content,
                "event_date" : beef_object.date,
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
                    break     
        
        else:
            if logging:
                print("Record already exists.")
            break #break loop because record already exists