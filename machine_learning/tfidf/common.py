import xml.etree.cElementTree as ET
import re
import string
import nltk
import sklearn
import sys
from collections import Counter
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS


def getxmltext(filename):
    """
    get the xml code from the file name to
    then be parsed by 'gettext' method
    """
    f= open(filename, 'r')
    text = f.read().strip()
    f.close()
    return text


def gettext(xmltext):
    """
    parse xmltext and return the text from <title> and <text> tags
    """
    text = ''
    xml = ET.fromstring(xmltext)
    text += xml.findall("title")[0].text
    elements = xml.findall('.//text/*')

    for ptag in elements:
        text += " " + ptag.text

    return text


def tokenize(text):

    """
        Tokenize text and return a non-unique list of tokenized words
        found in the text. Normalize to lowercase, strip punctuation,
        remove stop words, drop words of length < 3.
    """
    regex = re.compile('[%s0-9\\r\\t\\n]' % re.escape(string.punctuation))
    text = regex.sub(' ', text).lower()

    words = nltk.word_tokenize(text)
    words = [word for word in words if len(word) > 2 and word not in ENGLISH_STOP_WORDS]

    return words


def stemwords(words):
    """
        Given a list of tokens/words, return a new list with each word
        stemmed using a PorterStemmer.
    """
    stemmer = nltk.PorterStemmer()
    stems = [stemmer.stem(word) for word in words]

    return stems

if __name__=="__main__":
    # get the xml code from a filename passed in cmdline
    xmltext = getxmltext(sys.argv[1])

    # tokenize the words in the text and reduce them to stems
    text = gettext(xmltext)
    tokens = tokenize(text)
    tokens = stemwords(tokens)

    counts = Counter(tokens)
    mostcommon = counts.most_common()

    # print the top 10 most common words
    for i in range(10):
        print mostcommon[i][0], mostcommon[i][1]
