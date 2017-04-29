"""
# Created 10/28/13 #
# Author: Scott Halgrim, halgrim.s@ghc.org
# Unit tests for CRNLungNodule 
"""

import unittest
from crn_lung_nodule.crn_lung_nodule import has_keyword, sent_has_keyword, tokenize_sentence, file_to_sentences, ssplit


class CrnLungNoduleTester(unittest.TestCase):
    def test_sentContainKeywordList_returns_true_result_01(self):
        # Case 1: simple
        result = has_keyword('Sentence with word in it.', ['word'])
        self.assertEqual(result, True)

    def test_sentContainKeywordList_returns_true_result_02(self):
        # Case 2: case shouldn't matter
        result = has_keyword('Sentence with word in it.', ['wORd'])
        self.assertEqual(result, True)

    def test_sentContainKeywordList_returns_true_result_03(self):
        # Case 3: puncutation shouldn't matter
        result = has_keyword('Sentence with word in it.', ['it'])
        self.assertEqual(result, True)
        # same as self.assertTrue(result), I guess?

    def test_sentContainsKeywordList_returns_false_result_01(self):
        # Case 1: simple
        result = has_keyword('Sentence with word in it.', ['foo'])
        self.assertFalse(result)

    def test_sentContainsKeywordList_returns_false_result_02(self):
        # Case 2: partial word
        result = has_keyword('Sentence with word in it.', ['wit'])
        self.assertEqual(result, False)

    def test_sentContainsKeywordFile_returns_true_result_01(self):
        result = sent_has_keyword('Sentence with word in it.',
                                  r'.\data\test_sentContainsKeywordFileTrue01.txt')
        self.assertEqual(result, True)

    def test_sentContainsKeywordFile_returns_true_result_02(self):
        result = sent_has_keyword('Sentence with word in it.',
                                  r'.\data\test_sentContainsKeywordFileTrue02.txt')
        self.assertEqual(result, True)

    def test_sentContainsKeywordFile_returns_true_result_03(self):
        result = sent_has_keyword('Sentence with word in it.',
                                  r'.\data\test_sentContainsKeywordFileTrue03.txt')
        self.assertEqual(result, True)

    def test_sentContainsKeywordFile_returns_true_result_04(self):
        result = sent_has_keyword('Sentence with word in it.',
                                  r'.\data\test_sentContainsKeywordFileTrue04.txt')
        self.assertEqual(result, True)

    def test_sentContainsKeywordFile_returns_false_result_01(self):
        result = sent_has_keyword('Sentence with word in it.',
                                  r'.\data\test_sentContainsKeywordFileFalse01.txt')
        self.assertEqual(result, False)

    def test_sentContainsKeywordFile_returns_false_result_02(self):
        result = sent_has_keyword('Sentence with word in it.',
                                  r'.\data\test_sentContainsKeywordFileFalse02.txt')
        self.assertEqual(result, False)

    def test_sentContainsKeywordFile_raises_error(self):
        self.assertRaises(IOError, sent_has_keyword,
                          'Sentence with word in it.',
                          r'.\data\test_nonExistentFile.txt')

    def test_tokenizeSentence_01(self):
        """ Test tokenize results straight up """
        result = tokenize_sentence('Sentence with word in it.')
        self.assertEqual(result, ['Sentence', 'with', 'word', 'in', 'it', '.'])

    def test_splitText_01(self):
        """ Test results of sentence splitter """
        result = ssplit('I have two sentences here. The previous sentence is true.')
        self.assertEqual(result, ['I have two sentences here.', 'The previous sentence is true.'])

    def test_splitFileText_01(self):
        """ Test results of file sentence splitter """
        result = file_to_sentences(r'.\data\test_fileToSentences01.txt')
        self.assertEqual(result, ['I have two sentences in this file.', 'The previous sentence is true.'])


if __name__ == '__main__':
    unittest.main()
