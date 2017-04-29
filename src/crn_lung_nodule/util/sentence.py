import logging

from crn_lung_nodule.CrnLungNodule import get_lined_data

from crn_lung_nodule.util.constants import *
from crn_lung_nodule.nlp.tokenizer import Tokenizer

logger = logging.getLogger('ghri.scott.crn_lung_nodule.util.sentence')


class Sentence(object):
    """
    # Scott Halgrim #
    # 12/20/13 #
    # Basically stores state of a sentence as it goes through classification
    # process as described in
    # G:\CTRHS\CRN_Lung_Nodule\PROGRAMMING\Scott\Doco\NLP_algorithm_Revisions_(09
    # 19 2013)_CZ.doc
    """

    def __init__(self, text, doc, psm=TOKENS, r6psm=None):
        self.dcmt = doc
        self.text = text
        self.tokens = []
        self.tags = {}
        self.phraseSearchMethod = psm  # do we search for phrases by tokens or just string?
        self.rule6PhraseSearchMethod = r6psm if r6psm else psm
        self.maxNoduleSize = -1
        logger.debug('Created Sentence for %s with %d characters' % \
                     (self.dcmt.fn, len(self.text)))
        return

    def tokenize(self):
        tknzr = Tokenizer(self.text)
        self.tokens, errcode = tknzr.tokenize()

        if errcode:
            logger.warning('Errcode %d in file %s' % (errcode, self.dcmt.fn))

        logger.debug('Tokenized into %d tokens' % (len(self.tokens)))
        return self.tokens

    def has_tag(self, tag):
        """
        # Returns true iff tag is in keys AND the value is true #
        #                                                       #
        # A way to check to see if previously tagged but not do eval. B/c if on
        # the document level if you are checking for tags you don't want to eval
        # something if it never should have reached that step in the flow.
        """
        return self.tags.get(tag, False)

    def eval_thing(self, thing_to_eval):
        """
        
        :param thing_to_eval: 
        :return: function corresponding thing_to_eval
        """
        if thing_to_eval not in self.tags:
            self.tags[thing_to_eval] = self.EVAL_METHODS[thing_to_eval](self)
            logger.info('{0}\t{1}'.format(thing_to_eval, self.tags[thing_to_eval]))
        return self.tags[thing_to_eval]

    def set_thing(self, thing, val):
        prev_val = self.tags.get(thing, None)
        if prev_val and prev_val != val:
            logger.debug('Changing %s from %s to %s'.format(thing, self.tags[thing], val))
        self.tags[thing] = val

    def hasTokens(self, targetPhrase):
        """
        # returns True if the tokenized target phrase is inside the tokenized sentence.
        # TODO: improve tokenization
        """
        answer = False

        if not self.tokens:
            self.tokenize()

        sentTokens = [tok.lower() for tok in self.tokens]
        phraseTknzr = Tokenizer(targetPhrase)
        phraseTokens, errcode = phraseTknzr.tokenize()

        if errcode:
            logger.warning('Errcode %d in file %s' % (errcode, self.dcmt.fn))

        phraseTokens = [tok.lower() for tok in phraseTokens]
        sentTokenLen = len(sentTokens)
        phraseTokenLen = len(phraseTokens)

        for i in range(sentTokenLen - (phraseTokenLen - 1)):
            sentSlice = sentTokens[i:i + phraseTokenLen]

            if sentSlice == phraseTokens:
                answer = True
                break

        return answer

    def hasString(self, strphrase):
        if strphrase.lower() in self.text.lower():
            answer = True
        else:
            answer = False

        return answer

    def hasPhrase(self, phr, rule6=False):
        if rule6:
            answer = self.PHRASE_SEARCH_METHODS[self.rule6PhraseSearchMethod](self, phr)
        else:
            answer = self.PHRASE_SEARCH_METHODS[self.phraseSearchMethod](self, phr)

        return answer

    def hasPosKeyword(self, algo=DANFORTH_20130919, rule6PhraseSearchMethod=TOKENS):
        """
        # From newer Danforth algo, checks to see if sentence has positive
        # keyword. I.e., keyword from Tables 1.A or 1.B #
        # 9/5/14 updating so that it treats tables 1.a and 1.b differently if
        # rule6PhraseSearchMethod set to tokens
        """
        posKeywordsQualReqd = get_lined_data(algo, POS_KEYWORD_QUAL_REQD)
        posKeywordsNoQualReqd = get_lined_data(algo, POS_KEYWORD_NO_QUAL_REQD)

        for pk in posKeywordsQualReqd:
            if self.hasPhrase(pk):
                answer = True
                self.set_thing(POS_KEYWORD, True)
                break
        else:
            for pk in posKeywordsNoQualReqd:
                if self.hasPhrase(pk, rule6PhraseSearchMethod):
                    answer = True
                    self.set_thing(POS_KEYWORD, True)
                    break
            else:
                answer = False

        return answer

    def hasAbsDisqualTerm(self, algo=DANFORTH_20130919):
        """
        # Step 2 in newer Danforth algo. Checks for absolutely disqualifying
        # term (Table 2). TODO: This is virutally identical to hasPosKeyword.
        # Can I do refactoring here? Also see later steps
        """
        answer = False
        absDisqualTerms = get_lined_data(algo, ABS_DISQUAL_TERM)

        for adt in absDisqualTerms:
            if self.hasPhrase(adt):
                answer = True
                self.set_thing(ABS_DISQUAL_TERM, True)
                break

        return answer

    def hasExcludedTerm(self, algo=DANFORTH_20130919):
        """
        # Step 3 in newer Danforth algo. Checks for excluded term (Table 3)
        """
        answer = False
        excludedWords = get_lined_data(algo, EXCLUDED_TERM)

        for ew in excludedWords:
            if self.hasPhrase(ew):
                answer = True
                self.set_thing(EXCLUDED_TERM, True)
                break

        return answer

    def hasOffsettingTerm(self, algo=DANFORTH_20130919):
        """
        # Step 4 in newer Danforth algo. Checks for offsetting term (Table 4).
        # TODO: Can I make less read/write to/fron disk for corpus? Maybe by
        # modifying getLinedData to store stuff?
        """
        for ot in get_lined_data(algo, OFFSETTING_TERM):
            if self.hasPhrase(ot):
                self.set_thing(OFFSETTING_TERM, True)
                return True
        return False

    def hasPosKeywordNoQualReqd(self, algo=DANFORTH_20130919):
        """
        # Step 6 in newer Danforth algo. Checks for pos keyword with no
        # qualifiying term required (Table 1B). #
        # TODO: Can be made more efficient in combo with step 1?
        """
        posKeywordsNoQualReqd = get_lined_data(algo, POS_KEYWORD_NO_QUAL_REQD)
        for pknqr in posKeywordsNoQualReqd:
            if self.hasPhrase(pknqr, True):
                self.set_thing(POS_KEYWORD_NO_QUAL_REQD, True)
                return True
        return False

    def hasSizeGtMm(self, size, reIndex=0):
        """
        # TODO: need test cases
        """
        return self.calcMaxSize() > size

    def calcMaxSize(self, reIndex=0):
        """
        # TODO: Refactor. Lots of repeat code here vs hasSizeGtMm.  DONE 9/5/14
        """
        regex = SIZE_REGEXES[reIndex]
        match = regex.search(self.text)

        while match:
            foundSize = float(match.groupdict()['size'])
            dim = match.groupdict()['dim']

            if dim == 'c':
                foundSize *= 10

            if foundSize > self.maxNoduleSize:
                self.maxNoduleSize = foundSize

            nextStart = match.end()
            match = regex.search(self.text, nextStart)

        return self.maxNoduleSize

    def hasSizeGt30mm(self):
        return self.hasSizeGtMm(30)

    def hasSizeGt5mm(self):
        return self.hasSizeGtMm(5)

    def hasSizeGt0mm(self):
        return self.hasSizeGtMm(0)

    EVAL_METHODS = {
        POS_KEYWORD: hasPosKeyword,

        # putting self as arguments for these lambdas to make consistent with rest
        NLP_POSITIVE: lambda self: False,  # if it's not tagged, it's not nlpPos
        NLP_NEGATIVE: lambda self: False,  # if it's not tagged, it's not nlpNeg

        ABS_DISQUAL_TERM: hasAbsDisqualTerm,
        EXCLUDED_TERM: hasExcludedTerm,
        OFFSETTING_TERM: hasOffsettingTerm,
        POS_KEYWORD_NO_QUAL_REQD: hasPosKeywordNoQualReqd,
        SIZE_GT_0_MM: hasSizeGt0mm,  # TODO: Way to skip method, put arg of 30 in here?
        SIZE_GT_30_MM: hasSizeGt30mm,  # TODO: Way to skip method, put arg of 30 in here?
        SIZE_GT_5_MM: hasSizeGt5mm  # TODO: Way to skip method, put arg of 30 in here?`
    }

    PHRASE_SEARCH_METHODS = \
        {
            TOKENS: hasTokens,
            STRING: hasString
        }

    # EVAL_METHODS = \
    #    {
    #     POS_KEYWORD: self.hasPosKeyword,
    #     NLP_POSITIVE: lambda: False, # if it's not tagged, it's not nlpPos
    #     NLP_NEGATIVE: lambda: False, # if it's not tagged, it's not nlpNeg
    #     ABS_DISQUAL_TERM: self.hasAbsDisqualTerm,
    #     EXCLUDED_TERM: self.hasExcludedTerm,
    #     OFFSETTING_TERM: self.hasOffsettingTerm,
    #     POS_KEYWORD_NO_QUAL_REQD: self.hasPosKeywordNoQualReqd,
    #     SIZE_GT_30_MM: self.hasSizeGt30mm, # TODO: Way to skip method, put arg of 30 in here?
    #     SIZE_GT_5_MM: self.hasSizeGt5mm # TODO: Way to skip method, put arg of 30 in here?`
    #     }
