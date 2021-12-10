from flask import Flask, json, request
from flask_cors import cross_origin

# TODO
from fuzzy_match import Corpus

corpus = Corpus()
corpus.build_corpus()

dummy_json_results = {'results' : [{'docNumber' : 1,'body' : 'if you look at the two Unigram Language Models...', 'timestamp' : '12:24:01', 'week' : 7, 'lecture' : '7.2'}]}

api = Flask(__name__)

'''
Basic endpoint to check if the server is alive
'''
@api.route('/', methods=['GET', 'POST'])
@cross_origin()
def is_alive():
    return "yes, the server is alive; <br>hit /test for json response <br>or POST a JSON query to /search"


'''
Returns a dummy JSON result
'''
@api.route('/test', methods=['GET'])
@cross_origin()
def test():
    return json.dumps(dummy_json_results)

'''
POST endpoint to ingest JSON queries of the form:

{
  "query": [
    "query",
    "terms"
  ]
}

returns results as JSON in the form:

{
  "results": [
    {
      "docID": 1,
      "body": "if you look at the two Unigram Language Models...",
      "timestamp": "12:24:01",
      "week": 7,
      "lecture": "7.2"
    }
  ]
}

'''
@api.route('/search', methods=['POST'])
@cross_origin()
def search():
    
    queryJSON = request.get_json(force=True)
    print(queryJSON)
    # TODO 
    # pass JSON query to search function
    # results_json = naina_search(request.get_json())
    # return json.dumps(results_json)
    
    res = corpus.run_search(queryJSON)
    
    #return json.dumps(dummy_json_results)
    return json.dumps(res)

if __name__ == '__main__':
    api.run('localhost') 

