'''
# Scott Halgrim, halgrim.s@ghc.org #
# Created 11/5/13 for CRN Lung Nodule project #
'''

import token, tokenize
import logging

logger = logging.getLogger('ghri.scott.nlp.tokenizer')

class Tokenizer:
    '''
    # Basically a wrapper class around the tokenize.generate_tokens
    # functionality. It abstracts a lot of the setup away from dev, and also
    # doesn't return that ENDMARKER token at the end, instead just raising
    # StopIteration, which makes more sense to me at least.
    '''
    entered = False
    sentence = ''

    def __init__(self, text=''):
        '''
        # Creates instance of Tokenizer with insent as sentence to be tokenized
        '''
        self.sentence = text

        return

    def readtoken(self):
        '''
        # The required method to pass to tokenizer.generate_tokens that has the
        # interface of file.readline
        '''
        if self.entered:
            raise StopIteration
        else:
            self.entered = True
            return self.sentence

    def produceGenerator(self):
        '''
        # Creates and returns a generator function that works just like
        # tokenize.generate_tokens except doesn't return that last endmarker
        # token
        '''
        def mygen():
            for innerRes in tokenize.generate_tokens(self.readtoken):
                if innerRes[0] == token.ENDMARKER:
                    raise StopIteration
                else:
                    yield innerRes[1]
        return mygen

    def tokenize(self):
        myTokenGenerator = self.produceGenerator()
        tokens = []
        errcode = 0

        # adding try block 1/30/14 due to errors where it blows up with a TokenError
        # if parenlevel == -1 at end of sentence.
        try:
            for tkn in myTokenGenerator():
                tokens.append(tkn)
        except tokenize.TokenError, e:
            logger.warning('Silencing TokenError %s after sentence "%s" produced tokens %s'%
                           (e, self.sentence, tokens))
            errcode = -1

        return tokens, errcode

