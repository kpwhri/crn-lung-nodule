'''
# Created 10/28/13 #
# Scott Halgrim, halgrim.s@ghc.org #
# Written for CRN Lung Nodule project. PI Farhood Farjah. Re-creating algorithm
# as described in
# G:\CTRHS\CRN_Lung_Nodule\PROGRAMMING\Scott\Doco\Algorithms_v6_CZ.doc
'''

from ghri.scott.nlp.tokenizer import Tokenizer

from crn_lung_nodule.classes.constants import *
from crn_lung_nodule.nlp.sentence_splitter import SentenceSplitterPunktStripped

DEFAULT_SENT_SPLITTER = SentenceSplitterPunktStripped

def textToSentences(text, splitter=DEFAULT_SENT_SPLITTER):
    '''
    # Splits text string into list of sentence text strings using splitter.
    # splitter must have tokenize method
    '''
    return splitter.tokenize(text)

def fileToSentences(fn, splitter=DEFAULT_SENT_SPLITTER):
    '''
    # Splits text in a file into list of sentence text strings using splitter.
    # splitter must have tokenize method
    '''
    with open(fn) as f:
        text = f.read()
    return textToSentences(text, splitter)

def tokenizeSentence(sentence):
    tknzr = Tokenizer(sentence)
    answer = tknzr.tokenize()

    return answer

def sentContainKeywordList(sentence, kwlist):
    # lowercase and tokenize sentence, convert to set
    sentWordSet = set(tokenizeSentence(sentence.lower()))

    # lowercase keyword list and convert to set
    kwset = set([kw.lower() for kw in kwlist])

    # if any tokens are in kwset, set answer to true
    answer = len(sentWordSet.intersection(kwset)) > 0

    return answer

def sentContainKeywordFile(sentence, kwfn):
    with open(kwfn) as f:
        lines = f.readlines(kwfn)
    lines = [line.strip().lower() for line in lines]
    answer = sentContainKeywordList(sentence, lines)

    return answer

def getLinedData(algorithm, datatype):
    '''
    # Separating code from data. This will basically just map the type of data
    # wanted for the algorithm with the file where that data is kept.
    '''
    answer = []

    for fn in DATA_MAPPING[algorithm][datatype]:
        with open(fn) as f:
            lines = f.readlines()
        answer += [line.strip() for line in lines]

    return answer


