"""
Created 10/28/13 
Scott Halgrim, halgrim.s@ghc.org 
Written for CRN Lung Nodule project. PI Farhood Farjah. 
Re-creating algorithm Algorithms_v6_CZ.doc
"""

from crn_lung_nodule.nlp.tokenizer import Tokenizer

from crn_lung_nodule.util.constants import *
from crn_lung_nodule.nlp.sentence_splitter import SentenceSplitterPunktStripped

DEFAULT_SENT_SPLITTER = SentenceSplitterPunktStripped


def ssplit(text, splitter=DEFAULT_SENT_SPLITTER):
    """
    Splits text string into list of sentence text strings using splitter.
    splitter must have tokenize method
    """
    return splitter().tokenize(text)


def file_to_sentences(fn, splitter=DEFAULT_SENT_SPLITTER):
    """
    Splits text in a file into list of sentence text strings using splitter.
    splitter must have tokenize method
    """
    with open(fn) as f:
        text = f.read()
    return ssplit(text, splitter)


def tokenize_sentence(sentence):
    return Tokenizer(sentence).tokenize()[0]  # index 0 is the sentence


def has_keyword(sentence, kwlist):
    """
    
    :param sentence: 
    :param kwlist: 
    :return: True if token is in keyword list 
    """
    words = set(tokenize_sentence(sentence.lower()))
    keywords = {kw.lower() for kw in kwlist}
    # if any tokens are in kwset, set answer to true
    return bool(words & keywords)


def sent_has_keyword(sentence, kwfn):
    lines = []
    with open(kwfn) as f:
        for line in f:
            lines.append(line.strip())
    return has_keyword(sentence, lines)


def get_lined_data(algorithm, datatype):
    """
    Separating code from data. This will basically just map the type of data
    wanted for the algorithm with the file where that data is kept.
    """
    answer = []
    for fn in DATA_MAPPING[algorithm][datatype]:
        with open(fn) as f:
            lines = f.readlines()
        answer += [line.strip() for line in lines]
    return answer
