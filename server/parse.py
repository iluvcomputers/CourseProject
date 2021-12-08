
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

    return docs

docs = getDocs()
print(docs[0])
print(docs[137:140])
print(len(docs))
