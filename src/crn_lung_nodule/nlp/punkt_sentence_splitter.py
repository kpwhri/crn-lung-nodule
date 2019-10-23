"""
    Created 11/22/13 for CRN Lung Nodule project
"""

from nltk.tokenize.punkt import PunktSentenceTokenizer


class SentenceSplitterPunktStripped(PunktSentenceTokenizer):
    """
    Basically wraps PunktSentenceTokenizer but strips whitespace that
    surrounds sentences
    """

    def tokenize(self, text, **kwargs):
        """
        Only behavior I want to modify is this method
        :param text:
        :param kwargs:
        """
        for x in PunktSentenceTokenizer.tokenize(self, text):
            yield x
