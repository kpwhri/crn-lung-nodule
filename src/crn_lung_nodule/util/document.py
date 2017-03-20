import logging

from crn_lung_nodule.classes.sentence import Sentence

from crn_lung_nodule.util.constants import *
from crn_lung_nodule.nlp.sentence_splitter \
    import SentenceSplitterPunktStripped as SentSplitter

logger = logging.getLogger('ghri.scott.crn_lung_nodule.util.document')

class Document(object):
    '''
    # Scott Halgrim #
    # 12/20/13 #
    # Basically stores state of a document as it goes through classification
    # process as described in
    # G:\CTRHS\CRN_Lung_Nodule\PROGRAMMING\Scott\Doco\NLP_algorithm_Revisions_(09
    # 19 2013)_CZ.doc
    '''

    def __init__(self, fn, phrSrchMethod=TOKENS, rule6PhrSrchMethod=None):
        self.fn = fn
        with open(self.fn) as f:
            self.contents = f.read()
        self.phraseSearchMethod = phrSrchMethod
        self.rule6PhraseSearchMethod = rule6PhrSrchMethod if rule6PhrSrchMethod else phrSrchMethod

        logger.debug('Created Document from %s with %d characters'% \
                                                (self.fn, len(self.contents)))
        return

    def sentencify(self):
        sentSplitter = SentSplitter()
        self.textSentences = sentSplitter.tokenize(self.contents)
        self.sentences = [Sentence(ts, self, self.phraseSearchMethod, self.rule6PhraseSearchMethod)
                          for ts in self.textSentences]
        logger.debug('Split %s into %d sentences'% \
                        (self.fn, len(self.textSentences)))
        return self.textSentences

    def danforth20130919(self):
        answer = False
        for sent in self.sentences:
            if sent.isTagged(SIZE_GT_30_MM):
                logger.info(str.format('Document has sentence tagged {0}', SIZE_GT_30_MM))
                answer = False
                break
            elif sent.isTagged(NLP_POSITIVE):
                logger.info(str.format('Document has sentence tagged {0}', NLP_POSITIVE))
                answer = True

        return answer

    def farjah20140903(self):
        '''
        # Returns true if any sentence tagged NLP_POSITIVE, else False
        '''
        for sent in self.sentences:
            if sent.isTagged(NLP_POSITIVE):
                logger.info(str.format('Document has sentence tagged {0}', NLP_POSITIVE))
                answer = True
                break
        else:
            answer = False

        return answer

    def isPositive(self, algo=DANFORTH_20130919):
        '''
        # And here we have the meat of the algorithm. TODO: need test cases
        '''
        logger.info(str.format('processing document {0}', self.fn))
        self.processSentences(algo)
        answer = self.ALGORITHMS[algo](self)

        return answer

    def getMaxNoduleSize(self, reIndex=0, algo=DANFORTH_20130919):
        try:
            answer = max([sent.maxNoduleSize for sent in self.sentences])
        except AttributeError:
            self.sentencify()
            answer = max([sent.maxNoduleSize for sent in self.sentences])

        if answer == -1 and algo == FARJAH_20140903:
            # if we didn't get a max size before, let's try on all sentences
            logger.info(str.format('Calcing size on all sents for document {0}', self.fn))

            for sent in self.sentences:
                 sent.calcMaxSize()

            answer = max([sent.maxNoduleSize for sent in self.sentences])

        return answer

    def processSentences(self, algo=DANFORTH_20130919):
        prevSent = None

        try:
            enumerator = enumerate(self.sentences)
        except AttributeError:
            self.sentencify()
            enumerator = enumerate(self.sentences)

        for i, sent in enumerator:
            logger.info(str.format('Processing sentence {0}: {1}', i+1, sent.text))

            # have to set prevSent at top of loop due to all the continues
            if i == 0:
                prevSent = None
            else:
                prevSent = self.sentences[i-1]

            # Step 1
            logger.debug('Entering step 1 for sent %d'%(i+1))
            if sent.evalThing(POS_KEYWORD, 1):    
                pass    # tagging done in evaluateThing
            else:
                if prevSent and prevSent.evalThing(POS_KEYWORD, 1) \
                            and prevSent.evalThing(NLP_POSITIVE, 1):

                    # continuing to search in step 1
                    # NB: algo says don't tag
                    pass            
                else:
                    # go to next sentence
                    logger.info(str.format('Rule 1\t{0}\tTrue', NLP_NEGATIVE))
                    sent.setThing(NLP_NEGATIVE, True)
                    continue 

            # Step 2
            logger.debug('Entering step 2 for sent %d'%(i+1))

            if not sent.evalThing(ABS_DISQUAL_TERM, 2):
                pass    # "keep searching this sentence"
            else:
                # go to next sentence
                logger.info(str.format('Rule 2\t{0}\tTrue', NLP_NEGATIVE))
                sent.setThing(NLP_NEGATIVE, True)
                continue 

            # Step 3
            logger.debug('Entering step 3 for sent %d'%(i+1))
            sent.evalThing(EXCLUDED_TERM, 3) # tagging done in eval

            # Step 4
            logger.debug('Entering step 4 for sent %d'%(i+1))
            sent.evalThing(OFFSETTING_TERM, 4) # tagging done in eval

            # Step 5
            logger.debug('Entering step 5 for sent %d'%(i+1))
            if not sent.isTagged(EXCLUDED_TERM):
                pass    # continue searching sentence
            else:
                if sent.isTagged(OFFSETTING_TERM):
                    pass # continue searching sentence
                else:
                    logger.info(str.format('Rule 5\t{0}\tTrue', NLP_NEGATIVE))
                    sent.setThing(NLP_NEGATIVE, True)
                    continue # move on to next sentence

            # Step 6
#            sent.calcMaxSize()
            #if algo == FARJAH_20140903:
            #    sent.setThing(NLP_POSITIVE, True)
            #    logger.info(str.format('Rule 6\t{0}\tTrue', NLP_POSITIVE))
            #else:
            logger.debug('Entering step 6 for sent %d'%(i+1))
            if sent.evalThing(POS_KEYWORD_NO_QUAL_REQD):
                logger.info(str.format('Rule 6\t{0}\tTrue', NLP_POSITIVE))
                sent.setThing(NLP_POSITIVE, True)
                
                if algo == FARJAH_20140903:
                    sent.calcMaxSize()
                continue    # move to next sentence
            else:
                pass    # keep searching

            # Step 7
            logger.debug('Entering step 7 for sent %d'%(i+1))
            if algo == FARJAH_20140903 and sent.evalThing(SIZE_GT_0_MM, 7):
                logger.info(str.format('Rule 7_Farjah\t{0}\tTrue', NLP_POSITIVE))
                sent.setThing(NLP_POSITIVE, True)
            elif sent.evalThing(SIZE_GT_30_MM, 7):
                logger.info(str.format('Rule 7_Danforth\t{0}\tTrue', NLP_NEGATIVE))
                sent.setThing(NLP_NEGATIVE, True)
                continue # move on to next sentence
            elif sent.evalThing(SIZE_GT_5_MM, 7):
                logger.info(str.format('Rule 7_Danforth\t{0}\tTrube', NLP_POSITIVE))
                sent.setThing(NLP_POSITIVE, True)
                continue # move on to next sentence
        return

    ALGORITHMS = {
                  DANFORTH_20130919: danforth20130919,
                  FARJAH_20140903: farjah20140903 # no size qualifier ever needed, always put out size
                  }


