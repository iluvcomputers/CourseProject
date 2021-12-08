import numpy as np
import sys, json
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import glob

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

def score_func(query, doc):
    """
    Returns 0 if doc is not a match for query, and 1 if it is.
    """

    term_matrix = np.zeros(len(query))

    for i in range(len(query)):
        if query[i] in doc:
            term_matrix[i] = 1
        else:
            term_matrix[i] = 0

    # if the terms are mostly not matched, the doc is not a match
    if  2*(np.count_nonzero(term_matrix == 0)) <= len(query):
        return 1
    else:
        return 0

class Corpus(object):

    """
    A collection of documents.
    """

    def __init__(self, query_path):
        """
        Initialize empty document list.
        """
        self.documents = []
        self.subtitles = getDocs()

        self.query_path = query_path
        self.query = []

        self.match_list = []

    def build_query(self, query_path):

        stop_words = set(stopwords.words('english'))
        ps = PorterStemmer()

        f = open(query_path)
        data = json.load(f)
        for w in (data['query']):
            # get rid of stop words
            if w not in stop_words:
                # no duplicates
                if w not in self.query:
                    # stem query terms 
                    self.query.append(ps.stem(w))
        f.close()

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
                new_words = new_words + ps.stem(w) + ' '
            self.documents.append(new_words)

    def build_match_list(self):
        """
        Get match/no match for each document based on query
        """

        for i in range(len(self.documents)):
            if score_func(self.query, self.documents[i]) == 1:
                # list of matched records
                self.match_list.append(list(self.subtitles[i]))


def main(query_path):
    corpus = Corpus(query_path)
    corpus.build_query(query_path)
    print(corpus.query)
    corpus.build_corpus()
    corpus.build_match_list()
    print(corpus.match_list)
    #return list of matched records
    return(corpus.match_list)

if __name__ == '__main__':
    main(sys.argv[1])
