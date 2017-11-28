#!/usr/bin/env python3

#imports
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

#import functions
from interfaces.database.db_interface import get_objects_from_db_table

def initialise_classification_module():
    #access all_scraped_events and create training set for text classifier
    db_data = get_objects_from_db_table("all_scraped_events_with_classifications", "", "")
    training_set=[ ( obj["title"], obj["classification"] ) for obj in db_data]
    
    global cl
    cl = NaiveBayesClassifier(training_set)
    
    #print(classify_event("How Houston's layout may have made its flooding worse"))

def classify_event(event_text):
    global cl
    try:
        classification = cl.classify(event_text)
    except ValueError:
        print("value error")
        classification = "definite_beef"
        
    confirm = None
    
    if classification == "definite_beef" or classification == "probable_beef" or classification == "unsure":
        confirm = True
    elif classification == "unlikely_beef" or classification == "not_beef":
        confirm = None
    
    return { "confirm": confirm, "classification": classification }
    