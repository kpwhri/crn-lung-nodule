"""
Scott Halgrim
Created 11/5/13 for CRN Lung Nodule project 

TODO: Why are we using the built-in tokenizer for python source code?
"""

import logging
import re

logger = logging.getLogger('crn_lung_nodule.nlp.tokenizer')


class Tokenizer:
    """
    Dumb tokenizer based on the Python tokenize module (for legacy reasons)
    """
    sentence = ''

    def __init__(self, text=''):
        """
        # Creates instance of Tokenizer with insent as sentence to be tokenized
        """
        self.sentence = text

    def tokenize(self):
        return [tok for tok in re.findall('(\w+|\S)', self.sentence)], 0
