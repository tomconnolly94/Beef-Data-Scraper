#!/usr/bin/env python3
import re

def extract_quotes(text):
    
    return re.findall(r'"([^"]*)"', text)
