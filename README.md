# Ranked Search for Coursera Video Subtitles

Presently, Coursera video subtitles search provides exact match only for queries. Due to the inaccuracies in subtitles, as well as the frequency of typos, there is a clear benefit to implementing approximate string matching, or fuzzy search. Fuzzy search will help ensure students do not miss out on important information.

We originally intended to implement Fuzzy search, however early on we shifted to Ranked Search

---

## Project Demo

https://uofi.box.com/s/3fhxuug2sym52l4h9h3nsr9gjx9b1y2u

---

## Browser Extension

### Requirements

- Firefox (Tested on v94.0.1)

### Installation Instructions

First, import the add-on:

1. In Firefox, go to about:debugging
2. Click "This Firefox"
3. Click "Load Temporary Add-On"
4. Navigate to your saved `manifest.json` file and click on it

![Install Gif](./browser-extension/images/Install_Fuzzy_Search.gif)

### Using the Extension

1. Right-Click on any page in Firefox
2. Click "Fuzzy Search"
3. On the Fuzzy Search page, enter a query you'd like to search for

![Using Fuzzy Search Gif](./browser-extension/images/Using_Fuzzy_Search.gif)

### Required JS files

- background.js: This script is required for the "Fuzzy search" context menu option
- tabs.js: This script is related to the Fuzzy Script page and sends queries/receives responses for the application logic

---

## Ranked Matching Algorithm 

### Requirements 

- pip install nltk

### Inputs & Outputs

- input: corpus of subtitles, search query 
- output: matches (video name, timestamp, subtitle snippet)

### Implementation 

- stemming of query and documents (subtitles)
- removal of stop words from query 
- bag of words representation of query
- results returned in ranked order based on closeness of match (count of query term matches in document)

---

## Server

### Installation
- flask
- flask-cors
- nltk
- glob
- numpy

from the server directory, run:
- python3 server.py

### Implementation & Endpoints

/       - GET, check if server is running
/test   - GET, takes no params, returns dummy result JSON
/search - POST, takes JSON search query, returns JSON results

query JSON: 
  ```json
  {  
      "query": [  
        "query",  
        "terms"  
    ]  
  }
  ```  

results JSON:  
  ```json
  {  
    "results": [  
      {  
        "doc": "even parts of ancients tags or even syntax to the structures",  
        "id": "66",  
        "score": 38,  
        "timestamp": "00:05:08,860 --> 00:05:13,020",  
        "videoname": "10-8-text-categorization-methods"  
      }  
    ]  
  }
  ```


