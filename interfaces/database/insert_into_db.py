#!/usr/bin/env python3

import time
import pymongo
import datetime
from interfaces.database.db_config import open_db_connection

def insert_if_not_exist(formatted_object, table):
    
    while True:
        
        logging = None
        
        if logging:
            print("DB insert attempt started for: " + formatted_object["title"])
        
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
                
                if table == "scraped_training_events_dump_v0_1" or table == "all_scraped_events":
                    current_objects = db[table].find({ "title" : formatted_object["title"] })
                elif table == "scraped_url_store":
                    current_objects = db[table].find({ "url" : formatted_object["url"] })

                if current_objects.count() < 1:
                    
                    try:
                        db[table].insert(formatted_object)

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
                            print("Record inserted into table: " + table)
                        return None

                else:
                    if logging:
                        print("Record already exists.")
                    return None #break loop because record already exists
                
def get_objects_from_db_table(table, query_field, query_value):
    
    while True:
        
        logging = None
        
        if logging:
            print("DB find attempt started for: " + formatted_object.title)
        
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
                return db[table].find({})
