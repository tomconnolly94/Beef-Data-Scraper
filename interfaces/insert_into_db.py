#!/usr/bin/env python3

from pymongo import MongoClient

client = MongoClient('mongodb://beeftracker_server:6YdmYtA+dH7LHBg4+Dn0EyUPYSKsjxz5fmvVuxSmKbW/rGH8QH+96JiY33e0tBw7@ds141937.mlab.com:41937')

db = client.heroku_w63fjrg6

print(db.find({}))