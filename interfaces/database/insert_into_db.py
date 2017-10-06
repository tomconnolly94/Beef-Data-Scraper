#!/usr/bin/env python3

from interfaces.database.db_config import open_db_connection
import time
from objects.beef_object import BeefObject

def insert_if_not_exist(beef_object):
    
    while True:
        
        print("DB insert attempt started for: ")
        print(beef_object.title)
        
        #open db connection
        db = open_db_connection()

        results = db.scraped_training_events_dump_v0_1.find({ "title" : beef_object.title })

        if results.count() < 1:

            document = ({
                "title" : beef_object.title,
                "relevant_actors" : beef_object.relevant_actors, 
                "description" : beef_object.content,
                #"date_added" : beef_object, 
                "event_date" : beef_object.date,
                "highlights" : beef_object.highlights,
                "data_source" : beef_object.data_source,
                "selected_categories" : beef_object.categories,
                "img_title" : beef_object.img_title,
                "media_link" : beef_object.media_link,
            })

            try:
                db.scraped_training_events_dump_v0_1.insert(document)
                
            except ConnectionFailure:
                print("Pymongo error, retrying db connection...")
                
            else: #execute if "try" block is successful
                print("Record inserted.")
                break       
        
        else:
            print("Record already exists.")
            break #break loop because record already exists