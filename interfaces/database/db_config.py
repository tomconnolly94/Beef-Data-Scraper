#!/usr/bin/env python3
import pymongo
import os

def open_db_connection():
    
    MONGO_HOST = os.environ['MONGO_HOST']
    MONGO_DB = os.environ['MONGO_DB']
    MONGO_USER = os.environ['MONGO_USER']
    MONGO_PASS = os.environ['MONGO_PASS']
    MONGO_PORT = os.environ['MONGO_PORT']
    
    os.environ['S3_KEY']

    db_connection = pymongo.MongoClient(MONGO_HOST, MONGO_PORT, connect=False) # server.local_bind_port is assigned local port
    
    try:
        db = db_connection[MONGO_DB]
        db.authenticate(MONGO_USER, MONGO_PASS)
    except pymongo.errors.AutoReconnect:
        print("PYMONGO AUTH AUTO RECONNECT")
        print("######################################################")    
    except pymongo.errors.NetworkTimeout:
        print("PYMONGO CONNECTION NETWORK TIMEOUT")
        print("######################################################")
    else:
        return db