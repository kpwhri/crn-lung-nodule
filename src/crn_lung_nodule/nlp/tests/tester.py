'''
# Created 11/5/13 #
# Author: Scott Halgrim, halgrim.s@ghc.org #
# Unit tests for tokenizer 
'''

import unittest
from inspect import isgeneratorfunction

from ghri.scott.crn_lung_nodule.classes import sentence, document

from crn_lung_nodule.classes import constants
from crn_lung_nodule.nlp import tokenizer


class TokenizerTester(unittest.TestCase):
    '''
    # Tests tokenizer.Tokenizer
    '''

    def setUp(self):
        '''
        # Basically just unpack all the tokens in a test sentence into
        # self.tokens
        '''
        self.myTokenizer = tokenizer.Tokenizer('This is a test sentence.')
        self.tokens = self.myTokenizer.tokenize()[0]
        self.testDoc01 = document.Document(r'C:\code_ghri_share\ghri\scott\nlp\tests\testData\TestDoc01.txt',
                                          'phrase_search_string', 'phrase_search_tokens')
        self.testSent01_12 = sentence.Sentence("mass measuring 11-mm.", self.testDoc01,
                                               'phrase_search_string', 'phrase_search_tokens')

        return super(TokenizerTester, self).setUp()

    def tearDown(self):
        '''
        # Just delete the members
        '''
        del self.myTokenizer, self.tokens
        return super(TokenizerTester, self).tearDown()

    def test_Tokenizer_constructor_returns_tokenizer_01(self):
        '''
        # Case 1: No sentence constructor returns tokenizer
        '''
        tknzr = tokenizer.Tokenizer()
        self.assertIsInstance(tknzr, tokenizer.Tokenizer)

    def test_Tokenizer_constructor_returns_tokenizer_02(self):
        '''
        # Case 2: With sentence constructor returns tokenizer
        '''
        tknzr = tokenizer.Tokenizer('This is a test sentence.')
        self.assertIsInstance(tknzr, tokenizer.Tokenizer)

    def test_Tokenizer_produces_generator_01(self):
        '''
        # Verify I actually get a generator function from produceGenerator
        '''
        self.assertTrue(isgeneratorfunction(self.myTokenizer.produceGenerator()))

    def test_Tokenizer_empty_sentence_returns_empty_list(self):
        '''
        # Test that empty string tokenized is zero tokens
        '''
        tknzr = tokenizer.Tokenizer()
        mygen = tknzr.produceGenerator()
        tokens = []

        for tkn in mygen():
            tokens.append(tkn)

        self.assertEqual(tokens, [])

    def test_Tokenizer_tokenizes_true_result_01(self):
        '''
        # Case 1: simple
        '''
        self.assertIn('sentence', self.tokens)

    def test_Tokenizer_tokenizes_true_result_02(self):
        '''
        # Case 2: case sensitive first word
        '''
        self.assertIn('This', self.tokens)

    def test_Tokenizer_tokenizes_true_result_03(self):
        '''
        # Case 3: final period
        '''
        self.assertIn('.', self.tokens)

    def test_Tokenizer_tokenizes_false_result_01(self):
        '''
        # Case 1: Case sensitive final word.
        '''
        self.assertNotIn('Sentence', self.tokens)

    def test_Tokenizer_tokenizes_false_result_02(self):
        '''
        # Case 2: from out of nowhere word
        '''
        self.assertNotIn('foo', self.tokens)

    def test_Tokenizer_tokenizes_false_result_03(self):
        ''' Case 3: partial-word '''
        self.assertNotIn('sent', self.tokens)

    def test_Tokenizer_result_01(self):
        ''' Test Tokenizer's work '''
        self.assertEqual(self.tokens, ['This','is','a','test','sentence','.'])

    def test_Tokenizer_result_02(self):
        ''' Test Tokenizer on goofy sentence. 1/30/14 '''
        goofyTokenizer = tokenizer.Tokenizer(') uses fml adn vexol prn        Exam.')
        goofyTokens = goofyTokenizer.tokenize()[0]
        self.assertEqual(goofyTokens, [')', 'uses', 'fml', 'adn', 'vexol', 'prn', 'Exam', '.'])

    def test_Tokenizer_num_tokens_01(self):
        ''' Count number of tokens from tokenizer '''
        self.assertEqual(len(self.tokens), 6)

    def test_sizeRegexHyphen(self):
        ''' 6/5/14 Was not recognizing sizes like "11-mm" '''
        self.assertTrue(self.testSent01_12.evalThing(constants.SIZE_GT_5_MM))

if __name__ == '__main__':
    unittest.main()
