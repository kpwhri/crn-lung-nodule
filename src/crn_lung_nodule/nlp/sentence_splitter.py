'''
# Scott Halgrim, halgrim.s@ghc.org #
# Created 11/22/13 for CRN Lung Nodule project #
'''

from nltk.tokenize.punkt import PunktSentenceTokenizer

class SentenceSplitterPunktStripped(PunktSentenceTokenizer):
    '''
    # Basically wraps PunktSentenceTokenizer but strips whitespace that
    # surrounds sentences
    '''

    def tokenize(self, text):
        '''
        # Only behavior I want to modify is this method
        '''
        rawSents = PunktSentenceTokenizer.tokenize(self, text)
        output = [rs.strip() for rs in rawSents]

        return output
