#!/usr/bin/env python3
#imports
import sys

def save_url(source, url):
    
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
            results_current_events = db.url_dump_v0_1.find({ "url" : url })
            #TODO: ensure url doesnt already exist, and then insert it as object: { source: "cnn", url: "http://cnn.com/story/123", date_added: Date(01,01,2019)}
            
            #TODO: put in clause to remove any records that are more than a week old (use the date_added field)

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