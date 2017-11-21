#!/usr/bin/env python3
import time
import datetime
from interfaces.database.insert_into_db import insert_if_not_exist
from interfaces.database.insert_into_db import insert

def insert_loop(beef_objects):
    
    print("Events Scraped: " + str(len(beef_objects)))
    insert_count = 0

    for beef_object in beef_objects:
        if format_and_insert_scraped_beef_event(beef_object):
            insert_count += 1
        
        
    print("Events Inserted: " + str(insert_count))


def format_and_insert_scraped_beef_event(beef_object):
    
    inspect_beef_event_for_broken_fields(beef_object)
    
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

    #insert_if_not_exist(document, "scraped_training_events_dump_v0_1")

    document_min = ({
        "title" : beef_object.title
    })

    #insert_if_not_exist(document_min, "all_scraped_events") 

def inspect_beef_event_for_broken_fields(beef_object):
    
    beef_object_fields = beef_object.get_fields_as_array()
    
    for index, field in enumerate(beef_object_fields):
        
        #check string type or array type fields that length is larger than 0
        if index in [0, 1, 2, 3, 4, 6, 7]:
            if len(field) == 0:
                
                #check fields for empty values
                if index == 0:
                    record_broken_field("title", beef_object_fields[5], "empty", field)
                elif index == 1:
                    record_broken_field("relevant_actors", beef_object_fields[5], "empty", field)
                elif index == 2:
                    record_broken_field("content", beef_object_fields[5], "empty", field)    
                elif index == 3:
                    record_broken_field("date", beef_object_fields[5], "empty", field)          
                elif index == 4:
                    record_broken_field("quotes", beef_object_fields[5], "empty", field)     
                elif index == 6:
                    record_broken_field("categories", beef_object_fields[5], "empty", field)            
                elif index == 7:
                    record_broken_field("img_link", beef_object_fields[5], "empty", field)
            
            #check field values for incorrect formatting or too long/short values
            if index == 1 and len(field) < 2:
                record_broken_field("relevant_actors", beef_object_fields[5], "too_short", field)
            elif index == 2:
                if len(field) < 100:
                    record_broken_field("relevant_actors", beef_object_fields[5], "too_long", field)
                elif len(field) > 1000:
                    record_broken_field("relevant_actors", beef_object_fields[5], "too_long", field)
            elif index == 3:
                if len(field.split("/")) != 3:
                    record_broken_field("date", beef_object_fields[5], "incorrect_format", field)
                
        elif index == 8:
            if len(field["type"]) == 0 or len(field["link"]) == 0:
                record_broken_field("special_feature", beef_object_fields[5], "empty", field)
                
def record_broken_field(field_name, source, mode, value):
    
    insert_object = ({
        "broken_field": field_name,
        "source": source,
        "broken_mode": mode, #empty/incorrect_format/too_short/too_long
        "value": value
    })
    
    insert(insert_object, "broken_fields", None)