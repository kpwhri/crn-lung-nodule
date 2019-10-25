import logging
from typing import List

from crn_lung_nodule.nlp import BaseSentenceSplitter, SentenceSplitterPunktStripped, NLTK_SPLITTER
from crn_lung_nodule.util.sentence import Sentence

from crn_lung_nodule.util.constants import *

logger = logging.getLogger('crn_lung_nodule.util.document')


class Document(object):
    """
    Basically stores state of a document as it goes through classification
    process as described in
    NLP_algorithm_Revisions_(09 19 2013)_CZ.doc
    """

    def __init__(self, name, contents, psm, r6psm=None, use_base_sentence_splitter=False):
        self.name = name
        self.contents = contents
        self.psm = psm
        self.r6psm = r6psm if r6psm else psm
        if use_base_sentence_splitter or not NLTK_SPLITTER:
            self.splitter = BaseSentenceSplitter()
        else:
            self.splitter = SentenceSplitterPunktStripped()
        self.sentences = self._ssplit()  # requires splitter to be defined

        logger.debug('Document {} created with {} characters'.format(self.name, len(self.contents)))

    def _ssplit(self) -> List[Sentence]:
        sentences = [Sentence(ts, self, self.psm, self.r6psm)
                     for ts in self.splitter.tokenize(self.contents)]
        logger.debug('Split %s into %d sentences'.format(self.name, len(sentences)))
        return sentences

    def danforth20130919(self):
        answer = False
        for sent in self.sentences:
            if sent.has_tag(SIZE_GT_30_MM):
                logger.info('Document has sentence tagged {}'.format(SIZE_GT_30_MM))
                return False
            elif sent.has_tag(NLP_POSITIVE):
                logger.info('Document has sentence tagged {}'.format(NLP_POSITIVE))
                answer = True
        return answer

    def farjah20140903(self):
        """
        Returns true if any sentence tagged NLP_POSITIVE, else False
        """
        for sent in self.sentences:
            if sent.has_tag(NLP_POSITIVE):
                logger.info(str.format('Document has sentence tagged {0}', NLP_POSITIVE))
                answer = True
                break
        else:
            answer = False

        return answer

    def is_positive(self, algo=DANFORTH_20130919):
        """
        And here we have the meat of the algorithm. 
        TODO: need test cases
        """
        logger.info(str.format('processing document {0}', self.name))
        self.process_sentences(algo)
        return self.ALGORITHMS[algo](self)

    def get_max_nodule_size(self, reindex=0, algo=DANFORTH_20130919):
        answer = max(sent.max_nodule_size for sent in self.sentences)

        if answer == -1 and algo == FARJAH_20140903:
            # if we didn't get a max size before, let's try on all sentences
            logger.info(str.format('Calcing size on all sents for document {0}', self.name))
            for sent in self.sentences:
                sent.calc_max_size()
            return max(sent.max_nodule_size for sent in self.sentences)
        else:
            return answer

    def process_sentences(self, algo=DANFORTH_20130919):
        try:
            enumerator = enumerate(self.sentences)
        except AttributeError:
            self._ssplit()
            enumerator = enumerate(self.sentences)

        prev_sent: Sentence = None
        for i, sent in enumerator:
            logger.info(str.format('Processing sentence {0}: {1}', i + 1, sent.text))

            # have to set prev_sent at top of loop due to all the continues
            if i > 0:
                prev_sent = self.sentences[i - 1]

            # Step 1
            logger.debug('Entering step 1 for sent %d' % (i + 1))
            if sent.eval_thing(POS_KEYWORD):
                pass  # tagging done in evaluateThing
            else:
                if prev_sent and prev_sent.eval_thing(POS_KEYWORD) \
                        and prev_sent.eval_thing(NLP_POSITIVE):

                    # continuing to search in step 1
                    # NB: algo says don't tag
                    pass
                else:
                    # go to next sentence
                    logger.info(str.format('Rule 1\t{0}\tTrue', NLP_NEGATIVE))
                    sent.set_thing(NLP_NEGATIVE, True)
                    continue

                    # Step 2
            logger.debug('Entering step 2 for sent %d' % (i + 1))

            if not sent.eval_thing(ABS_DISQUAL_TERM):
                pass  # "keep searching this sentence"
            else:
                # go to next sentence
                logger.info(str.format('Rule 2\t{0}\tTrue', NLP_NEGATIVE))
                sent.set_thing(NLP_NEGATIVE, True)
                continue

                # Step 3
            logger.debug('Entering step 3 for sent %d' % (i + 1))
            sent.eval_thing(EXCLUDED_TERM)  # tagging done in eval

            # Step 4
            logger.debug('Entering step 4 for sent %d' % (i + 1))
            sent.eval_thing(OFFSETTING_TERM)  # tagging done in eval

            # Step 5
            logger.debug('Entering step 5 for sent %d' % (i + 1))
            if not sent.has_tag(EXCLUDED_TERM):
                pass  # continue searching sentence
            else:
                if sent.has_tag(OFFSETTING_TERM):
                    pass  # continue searching sentence
                else:
                    logger.info(str.format('Rule 5\t{0}\tTrue', NLP_NEGATIVE))
                    sent.set_thing(NLP_NEGATIVE, True)
                    continue  # move on to next sentence

                    # Step 6
                    #            sent.calcMaxSize()
            # if algo == FARJAH_20140903:
            #    sent.setThing(NLP_POSITIVE, True)
            #    logger.info(str.format('Rule 6\t{0}\tTrue', NLP_POSITIVE))
            # else:
            logger.debug('Entering step 6 for sent %d' % (i + 1))
            if sent.eval_thing(POS_KEYWORD_NO_QUAL_REQD):
                logger.info(str.format('Rule 6\t{0}\tTrue', NLP_POSITIVE))
                sent.set_thing(NLP_POSITIVE, True)

                if algo == FARJAH_20140903:
                    sent.calc_max_size()
                continue  # move to next sentence
            else:
                pass  # keep searching

            # Step 7
            logger.debug('Entering step 7 for sent %d' % (i + 1))
            if algo == FARJAH_20140903 and sent.eval_thing(SIZE_GT_0_MM):
                logger.info(str.format('Rule 7_Farjah\t{0}\tTrue', NLP_POSITIVE))
                sent.set_thing(NLP_POSITIVE, True)
            elif sent.eval_thing(SIZE_GT_30_MM):
                logger.info(str.format('Rule 7_Danforth\t{0}\tTrue', NLP_NEGATIVE))
                sent.set_thing(NLP_NEGATIVE, True)
                continue  # move on to next sentence
            elif sent.eval_thing(SIZE_GT_5_MM):
                logger.info(str.format('Rule 7_Danforth\t{0}\tTrube', NLP_POSITIVE))
                sent.set_thing(NLP_POSITIVE, True)
                continue  # move on to next sentence
        return

    ALGORITHMS = {
        DANFORTH_20130919: danforth20130919,
        FARJAH_20140903: farjah20140903  # no size qualifier ever needed, always put out size
    }
