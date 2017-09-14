#!/usr/bin/env python3

from interfaces.db_config import open_db_connection
import time
from objects.beef_object import BeefObject

def insert_if_not_exist(beef_object):
    
    
    while True:
        
        print("loop entered")
        
        #open db connection
        db = open_db_connection()

        results = db.scraped_training_events_dump_v0_1.find({ "title" : beef_object.title })

        if results.count() < 1:

            print("insert procedure started")

            document = ({
                "title" : beef_object.title,
                "relevant_actors" : beef_object.relevant_actors, 
                "description" : beef_object.content,
                #"date_added" : beef_object, 
                "event_date" : beef_object.date,
                "highlights" : beef_object.highlights,
                "data_sources" : beef_object.data_source,
                "selected_categories" : beef_object.categories,
                "img_title" : beef_object.img_title,
                "media_link" : beef_object.media_link,
            })

            try:
                db.scraped_training_events_dump_v0_1.insert(document)
                db.close()
                print("inserted")
                break

            except exceptions as e:
                print("Pymongo error, retrying db connection...")
                db.close()
        
'''      
beef_object = BeefObject(
    "Storm Harvey: Trump to make second visit to Texas", 
    ['Donald Trump', 'Trump', 'Louisiana', 'Abbott', 'Melania', 'Mrs Trump', 'Houston', 'Lake Charles', 'Mick Mulvaney', 'Mulvaney', 'Harvey', 'Texas', 'Major League Baseball', 'Reid Ryan'],
    "We have already learned how to insert records into a collection and also learned how to update the document within a collection based on certain criteria. In this page, we are going to discuss how to remove document and entire collection.remove() is used to remove a document and a collection. It may be a good practice if you execute a find() before removing a document as you can can fix a criteria for removing the document.",
    "2 September 2017", 
    ['National Day of Prayer', "This request is a down-payment on the president's commitment to help affected states recover from the storm, and future requests will address longer-term rebuilding needs,", 'expeditiously to ensure that the debt ceiling does not affect these critical response and recovery efforts', 'multi-year project', 'This is going to be a massive, massive clean-up process,', 'poses an ongoing threat', 'We hope that these games can serve as a welcome distraction for our city that is going through a very difficult time,', 'We hope that we can put smiles on some faces.'], 
    "http://www.bbc.co.uk/news/world-us-canada-41134799", 
    [], 
    "https://ichef-1.bbci.co.uk/news/320/cpsprodpb/32EA/production/_97643031_mediaitem97643030.jpg",
    ""
    )

insert(beef_object)
'''
