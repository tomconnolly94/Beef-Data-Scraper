#!/usr/bin/env python3
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

'''
#funnel function to apply the filtering to each beef_object
def filter_beef_objects(beef_objects):
    
    for beef_object in beef_objects:
        filter_beef_object(beef_object)
        

def filter_beef_object(beef_object):
    #classification into three categories 'definite_beef', 'possible_beef' and 'not_beef'
 '''   

#create training set
training_set = [
    ("Chance Responds", 'definite_beef'),
    ("The Tweet Storm", 'definite_beef'),
    ("Maybe it wasn't tough enough...", 'definite_beef'),
    ("Locked and Loaded", 'definite_beef'),
    ("Guam attack Plans", 'definite_beef'),
    ("They will be met with Fire, Fury...", 'definite_beef'),
    ("Two Birds. One Stone", 'definite_beef'),
    ("Cudi Tweets from Rehab", 'definite_beef'),
    ("'Divorce bill' row frustrates Brexit talks", 'definite_beef'),
    
    ("Birmingham bin strike: Industrial action could resume on Friday", 'possible_beef'),
    ("Man charged over Buckingham Palace incident", 'possible_beef'),
    ("North Korean ambassador summoned by the UK", 'possible_beef'),
    ("Surrey v Middlesex: Play abandoned after crossbow arrow lands on pitch", 'possible_beef'),
    
    ("Frankfurt to evacuate 70,000 after British WW2 bomb found", 'not_beef'),
    ("Transfer deadline day with the UK's youngest football agent", 'not_beef')
]

cl = NaiveBayesClassifier(training_set)

print(cl.classify("How Houston's layout may have made its flooding worse"))
print(cl.classify("Apple will likely unveil new iPhones on Sept. 12"))
print(cl.classify("US retaliates against Russia ordering closure of consulate and annexes"))
print(cl.classify("The North Korea crisis needs a grown-up -- Trump is making it worse"))

cl.show_informative_features(20)