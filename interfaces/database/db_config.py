#!/usr/bin/env python3

import pymongo

def open_db_connection():
    MONGO_HOST = "ds141937.mlab.com"
    MONGO_DB = "heroku_w63fjrg6"
    MONGO_USER = "beeftracker_server"
    MONGO_PASS = "6YdmYtA+dH7LHBg4+Dn0EyUPYSKsjxz5fmvVuxSmKbW/rGH8QH+96JiY33e0tBw7"
    MONGO_PORT = 41937

    db_connection = pymongo.MongoClient(MONGO_HOST, MONGO_PORT, connect=False) # server.local_bind_port is assigned local port
    db = db_connection[MONGO_DB]
    db.authenticate(MONGO_USER, MONGO_PASS)
    
    return db