#!/usr/bin/env python3
#imports
import sys
import json
from actor_scraping.actor_scraper_controller import scrape_actor

print("scrape_actor.py started.")

result = scrape_actor(sys.argv[1])

print(json.dumps(result))