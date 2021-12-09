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

# returns 2d array with fields: videoname, offset, timestamp, and document
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

def score_func(query, doc, tf, N):
    """
    Returns 0 if doc is not a match for query, and 1 if it is.
    """

    term_matrix = np.zeros(len(query))

    for i in range(len(query)):
        term_matrix[i] = doc.count(query[i])
        #if query[i] in doc:
        #    term_matrix[i] += 1
        #else:
        #    term_matrix[i] = 0

    # if the terms are mostly not matched, the doc is not a match
    if  2*(np.count_nonzero(term_matrix == 0)) <= len(query):
        sc = 0
        for t in range(len(term_matrix)):
            sc += int((math.log(N/(tf[query[t]]+1), 2) + 1) * (math.log(term_matrix[t]+1, 2)+1))
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

    def build_query(self, query):

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
            
        #print(self.tf)
        #exit(0)

    def build_match_list(self):
        """
        Get match/no match for each document based on query
        """
        for i in range(len(self.documents)):
            score = score_func(self.query, self.documents[i], self.tf, len(self.documents))
            if score >= 1:
                # list of matched records
                self.match_list.append([score, list(self.subtitles[i])])
                #self.match_list.append(list(self.subtitles[i]))

    def run_search(self, queryJSON, rank=True):
        
        self.build_query(queryJSON)
        print(self.query)
        self.build_match_list()
        if rank:
            self.match_list.sort(key = lambda x: x[0], reverse=True)
            #self.match_list = [x[1] for x in self.match_list] 
        #print(self.match_list[:20])
        print(self.match_list)
        return(self.match_list)

def run(queryJSON):
    corpus = Corpus()
    corpus.build_corpus()
    corpus.run_search(queryJSON)

if __name__ == '__main__':
    run(json.loads(sys.argv[1]))
