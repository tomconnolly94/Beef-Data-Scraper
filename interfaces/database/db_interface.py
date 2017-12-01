#!/usr/bin/env python3
import time
import pymongo
from datetime import datetime
from calendar import monthrange
from interfaces.database.db_config import open_db_connection

def insert(formatted_object, table, db):
    
    while True:
        
        logging = None

        if db is None:
            #open db connection
            db = open_db_connection()

        try:
            db[table].insert(formatted_object)

        except ConnectionFailure:
            if logging:
                print("Pymongo error, retrying db connection...")
        except pymongo.errors.NetworkTimeout:
            print("PYMONGO INSERT NETWORK TIMEOUT")
            print("######################################################")

        except pymongo.errors.AutoReconnect:
            print("PYMONGO INSERT AUTO RECONNECT")
            print("######################################################")

        else: #execute if "try" block is successful
            if logging:
                print("Record inserted into table: " + table)
            return None

    
def insert_if_not_exist(formatted_object, table):
    
    while True:
        
        logging = None
        
        if logging:
            print("DB insert attempt started for: " + formatted_object["title"])
        
        #open db connection
        db = open_db_connection()
        
        if db:

            if table == "scraped_training_events_dump_v0_1" or table == "all_scraped_events_with_classifications":
                current_objects = db[table].find({ "title" : formatted_object["title"] })
            elif table == "scraped_url_store":
                current_objects = db[table].find({ "url" : formatted_object["url"] })
            else:
                current_objects = []
                
            if current_objects.count() < 1:

                insert(formatted_object, table, db)

            else:
                if logging:
                    print("Record already exists.")
                return None #break loop because record already exists
                
def get_objects_from_db_table(table, query_field, query_value):
    
    while True:
                
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
                if len(query_field) > 0 and len(query_value) > 0:
                    query_string = { query_field : query_value }
                    
                    return list(db[table].find(query_string))
                else:
                    return list(db[table].find({}))

#create query to remove any saved scraped events that are more than a week old
def remove_expired_events():

    while True:
                
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
                
                day_num = datetime.fromtimestamp(time.time()).day - 1
                month_num = datetime.fromtimestamp(time.time()).month
                year_num = datetime.fromtimestamp(time.time()).year
                
                if day_num == 0:
                    month_num -= 1
                    
                    if month_num == 0:
                        month_num = 12
                        year_num -= 1
                
                num_of_days_in_month = monthrange(year_num, month_num)[1]
                
                if(day_num == 0):
                    day_num = num_of_days_in_month
                
                query_date = datetime(year_num, 
                                      month_num, 
                                      day_num, 
                                      datetime.fromtimestamp(time.time()).hour, 
                                      datetime.fromtimestamp(time.time()).minute )
                
                db.scraped_url_store.remove({ "date_added" : { "$lt" : query_date } } )
                db.broken_fields.remove({ "date_added" : { "$lt" : query_date } } )
                return None
