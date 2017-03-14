from common import *
import os
import sklearn.feature_extraction.text as sk
from operator import itemgetter


def tokenizer(text):
    """
    tokenizer to use in the TfidfVectorizer
    """
    tokens = tokenize(text)
    tokens = stemwords(tokens)

    return tokens

def filelist(path):
    """
    build a list of filenames from a path
    """
    file_list = []
    for path, subdir, file in os.walk(path):
        file_list += [path + "/" + f for f in file if f[-4:] == '.xml']

    return file_list

if __name__=="__main__":
    # - Build a file list to train the TfidfVectorizer
    # use the imported 'gettext' method as a preprocessor
    # use 'tokenizer' method as the tokenizer
    files = filelist(sys.argv[1])
    tfidf = sk.TfidfVectorizer(input='filename',
                            analyzer='word',
                            preprocessor=gettext,
                            tokenizer=tokenizer,
                            stop_words='english',
                            decode_error ='ignore')

    tfidf.fit(files)
    matrix = tfidf.transform([sys.argv[2]])

    # - get the indices for nonzero elements to then get
    # the proper words and their respective scores
    indices = matrix.nonzero()
    wordbank = tfidf.get_feature_names()

    words = [wordbank[idx] for idx in indices[1]]
    scores = [matrix[0, idx] for idx in indices[1]]

    # - match up words with their respective tfidf scores and sort them
    # from high to low scores
    results = zip(words, scores)
    results = sorted(results, key=lambda x: x[1], reverse=True)

    # print scores/word combinations with a tfidf score of 0.09 or higher
    for i in range(len(results)):
        if results[i][1] >= .09:
            print "%s %.3f" % (results[i][0], round(results[i][1], 3))
