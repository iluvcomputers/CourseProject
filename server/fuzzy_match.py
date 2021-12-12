import numpy as np
import sys, json
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import glob
import math

'''
pack the resulting documents as json
'''
def packJSON(ls):

    keys = ["videoname", "id", "timestamp", "doc"]
    
    out = []
    for r in range(len(ls)):
        out.append({k:v for k,v in zip(keys,ls[r][1])})
        out[-1]['score'] = ls[r][0]

    res = {}
    res['results'] = out
    return res
'''
returns 2d array with fields: videoname, offset, timestamp, and document
'''
def getDocs():
    docs = []
    for fname in glob.glob("data/*.srt"):

        with open(fname) as data:
            #lines = [line.split('\n') for line in data.read().split('\n\n')]
            lines = [line for line in data.read().split('\n\n')]

            for l in lines:
                record = [fname.split('/')[1].split('_')[1].split('.')[0]]
                record += l.split('\n')
                record[3:] = [' '.join(record[3:])]
                if record[-1] != '':
                    docs.append(record)

    return np.array(docs)

'''
score a document based on tf-idf
'''
def score_func(query, doc, tf, N):
    """
    Returns 0 if doc is not a match for query, and 1 if it is.
    """
    threshold = 10
    term_matrix = np.zeros(len(query))

    for i in range(len(query)):
        term_matrix[i] = doc.count(query[i])
    '''
    use idf and tf to score docs -- no length norm bc doc lengths are very similar
    '''
    sc = 0
    for t in range(len(term_matrix)):
        sc += int((math.log(N/(tf.get(query[t], N)+1), 2) + 1) * (math.log(term_matrix[t]+1, 2)+1))
    if sc >= threshold and np.count_nonzero(term_matrix == 1) > 0:
        return sc
    else:
        return 0

class Corpus(object):

    """
    A collection of documents.
    """

    def __init__(self):
        """
        Initialize empty document list.
        """
        self.documents = []
        self.subtitles = getDocs()

        self.query = []

        self.match_list = []

        self.tf = {}
    
    def clear_query(self):

        self.query = []
        self.match_list = []

    def build_query(self, query):

        self.clear_query()
        stop_words = set(stopwords.words('english'))
        ps = PorterStemmer()

        data = query#json.loads(query)
        for w in (data['query']):
            # get rid of stop words
            if w not in stop_words:
                # no duplicates
                if w not in self.query:
                    # stem query terms 
                    self.query.append(ps.stem(w))

    def build_corpus(self):

        # only want index 3
        docs = self.subtitles[:,3]

        ps = PorterStemmer()

        for i in range(len(docs)):
            new_words = ''

            # get rid of punctuation
            docs[i] = docs[i].replace('.', '')
            docs[i] = docs[i].replace(',', '')
            docs[i] = docs[i].replace('!', '')
            docs[i] = docs[i].replace('?', '')
            docs[i] = docs[i].replace(':', '')
            docs[i] = docs[i].replace('-', '')
            words = word_tokenize(docs[i])
            for w in words:
                #stem words in subtitles
                pstem = ps.stem(w)
                new_words = new_words + pstem + ' '
                self.tf[pstem] = self.tf.get(pstem, 0) + 1
            self.documents.append(new_words)
            
    def build_match_list(self):
        """
        Get match/no match for each document based on query
        """
        for i in range(len(self.documents)):
            score = score_func(self.query, self.documents[i], self.tf, len(self.documents))
            if score >= 1:
                # list of matched records
                self.match_list.append([score, list(self.subtitles[i])])

    def run_search(self, queryJSON, rank=True):
        
        self.build_query(queryJSON)
        self.build_match_list()
        if rank:
            self.match_list.sort(key = lambda x: x[0], reverse=True)
            # save without rank info
            #self.match_list = [x[1] for x in self.match_list] 
       
        # return only top 25
        return(packJSON(self.match_list[:25]))

def run(queryJSON):
    corpus = Corpus()
    corpus.build_corpus()
if __name__ == '__main__':
    run(json.loads(sys.argv[1]))
