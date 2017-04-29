"""
Scott Halgrim
Created 11/5/13 for CRN Lung Nodule project 
"""

import logging
import token
import tokenize

logger = logging.getLogger('crn_lung_nodule.nlp.tokenizer')


class Tokenizer:
    """
    Basically a wrapper class around the tokenize.generate_tokens
    functionality. It abstracts a lot of the setup away from dev, and also
    doesn't return that ENDMARKER token at the end, instead just raising
    StopIteration, which makes more sense to me at least.
    """
    entered = False
    sentence = ''

    def __init__(self, text=''):
        """
        Creates instance of Tokenizer with insent as sentence to be tokenized
        """
        self.sentence = text

        return

    def read_token(self):
        """
        The required method to pass to tokenizer.generate_tokens that has the
        interface of file.readline
        """
        if self.entered:
            raise StopIteration
        else:
            self.entered = True
            return self.sentence

    def produce_generator(self):
        """
        Creates and returns a generator function that works just like
        tokenize.generate_tokens except doesn't return that last endmarker
        token
        """
        def mygen():
            for inner_res in tokenize.generate_tokens(self.read_token):
                if inner_res[0] == token.ENDMARKER:
                    raise StopIteration
                else:
                    yield inner_res[1]
        return mygen

    def tokenize(self):
        tokens = []
        errcode = 0
        try:
            for tkn in self.produce_generator()():
                tokens.append(tkn)
        except tokenize.TokenError as e:
            logger.warning('TokenError {} after sentence "{}" produced tokens {}'.format(e, self.sentence, tokens))
            errcode = -1
        return tokens, errcode
