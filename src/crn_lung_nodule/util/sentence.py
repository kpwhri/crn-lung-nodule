import logging

from crn_lung_nodule.crn_lung_nodule import get_lined_data

from crn_lung_nodule.util.constants import *
from crn_lung_nodule.nlp.tokenizer import Tokenizer

logger = logging.getLogger('crn_lung_nodule.util.sentence')


class Sentence(object):
    """
    Basically stores state of a sentence as it goes through classification
    process as described in
    NLP_algorithm_Revisions_(09 19 2013)_CZ.doc
    """

    def __init__(self, text, doc, psm=TOKENS, r6psm=None):
        """
        
        :param text: 
        :param doc: 
        :param psm: 
        :param r6psm: rule6 phrase search method 
        """
        self.dcmt = doc
        self.text = text
        self.tokens = []
        self.tags = {}
        self.psm = psm  # do we search for phrases by tokens or just string?
        self.r6psm = r6psm if r6psm else psm
        self.max_nodule_size = -1
        logger.debug('Created Sentence for {} with {} characters'.format(self.dcmt.name, len(self.text)))

    def tokenize(self, text):
        tknzr = Tokenizer(text)
        tokens, errcode = tknzr.tokenize()
        if errcode:
            logger.warning('Errcode {} in file {}'.format(errcode, self.dcmt.name))
        logger.debug('Tokenized into {} tokens'.format(len(tokens)))
        return tokens

    def has_tag(self, tag):
        """
        Returns true iff tag is in keys AND the value is true #
                                                              #
        A way to check to see if previously tagged but not do eval. B/c if on
        the document level if you are checking for tags you don't want to eval
        something if it never should have reached that step in the flow.
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

    def get_tokens(self):
        if not self.tokens:
            self.tokens = self.tokenize(self.text)
        return self.tokens

    def has_tokens(self, target_phrase):
        """
        returns True if the tokenized target phrase is inside the tokenized sentence.
        TODO: improve tokenization
        """
        sent_tokens = [tok.lower() for tok in self.get_tokens()]
        phrase_tokens = [t.lower() for t in self.tokenize(target_phrase)]
        for i in range(len(sent_tokens) - (len(phrase_tokens) - 1)):
            if sent_tokens[i:i + len(phrase_tokens)] == phrase_tokens:
                return True
        return False

    def has_string(self, strphrase):
        return strphrase.lower() in self.text.lower()

    def has_phrase(self, phr, rule6=False):
        if rule6:
            return self.PHRASE_SEARCH_METHODS[self.r6psm](self, phr)
        return self.PHRASE_SEARCH_METHODS[self.psm](self, phr)

    def has_pos_keyword(self, algo=DANFORTH_20130919, r6psm=TOKENS):
        """
        From newer Danforth algo, checks to see if sentence has positive
        keyword. I.e., keyword from Tables 1.A or 1.B #
        9/5/14 updating so that it treats tables 1.a and 1.b differently if
        rule6PhraseSearchMethod set to tokens
        """
        return self.has_term(POS_KEYWORD_QUAL_REQD, algo, False) or self.has_term(POS_KEYWORD_NO_QUAL_REQD, algo, r6psm)

    def has_abs_disqual_term(self, algo=DANFORTH_20130919):
        """
        Step 2 in newer Danforth algo. Checks for absolutely disqualifying
        term (Table 2). TODO: This is virutally identical to hasPosKeyword.
        Can I do refactoring here? Also see later steps
        """
        return self.has_term(ABS_DISQUAL_TERM, algo, False)

    def has_excluded_term(self, algo=DANFORTH_20130919):
        """
        Step 3 in newer Danforth algo. Checks for excluded term (Table 3)
        """
        return self.has_term(EXCLUDED_TERM, algo, False)

    def has_offsetting_term(self, algo=DANFORTH_20130919):
        """
        Step 4 in newer Danforth algo. Checks for offsetting term (Table 4).
        TODO: Can I make less read/write to/fron disk for corpus? Maybe by
        modifying getLinedData to store stuff?
        """
        return self.has_term(OFFSETTING_TERM, algo, False)

    def has_pos_keyword_no_qual_reqd(self, algo=DANFORTH_20130919):
        """
        Step 6 in newer Danforth algo. Checks for pos keyword with no
        qualifiying term required (Table 1B). #
        TODO: Can be made more efficient in combo with step 1?
        """
        return self.has_term(POS_KEYWORD_NO_QUAL_REQD, algo)

    def has_term(self, term, algo=DANFORTH_20130919, r6psm=True):
        """
        Step 6 in newer Danforth algo. Checks for pos keyword with no
        qualifiying term required (Table 1B). #
        TODO: Can be made more efficient in combo with step 1?
        """
        for term in get_lined_data(algo, term):
            if self.has_phrase(term, r6psm):
                self.set_thing(term, True)
                return True
        return False

    def has_size_gt_mm(self, size, reindex=0):
        """
        TODO: need test cases
        """
        return self.calc_max_size() > size

    def calc_max_size(self, reindex=0):
        """
        TODO: Refactor. Lots of repeat code here vs hasSizeGtMm.  DONE 9/5/14
        """
        regex = SIZE_REGEXES[reindex]
        match = regex.search(self.text)

        while match:
            found_size = float(match.groupdict()['size'])
            dim = match.groupdict()['dim']

            if dim == 'c':
                found_size *= 10

            if found_size > self.max_nodule_size:
                self.max_nodule_size = found_size

            next_start = match.end()
            match = regex.search(self.text, next_start)

        return self.max_nodule_size

    def has_size_gt_30_mm(self):
        return self.has_size_gt_mm(30)

    def has_size_gt_5_mm(self):
        return self.has_size_gt_mm(5)

    def has_size_gt_0_mm(self):
        return self.has_size_gt_mm(0)

    EVAL_METHODS = {
        POS_KEYWORD: has_pos_keyword,

        # putting self as arguments for these lambdas to make consistent with rest
        NLP_POSITIVE: lambda self: False,  # if it's not tagged, it's not nlpPos
        NLP_NEGATIVE: lambda self: False,  # if it's not tagged, it's not nlpNeg

        ABS_DISQUAL_TERM: has_abs_disqual_term,
        EXCLUDED_TERM: has_excluded_term,
        OFFSETTING_TERM: has_offsetting_term,
        POS_KEYWORD_NO_QUAL_REQD: has_pos_keyword_no_qual_reqd,
        SIZE_GT_0_MM: has_size_gt_0_mm,  # TODO: Way to skip method, put arg of 30 in here?
        SIZE_GT_30_MM: has_size_gt_30_mm,  # TODO: Way to skip method, put arg of 30 in here?
        SIZE_GT_5_MM: has_size_gt_5_mm  # TODO: Way to skip method, put arg of 30 in here?`
    }

    PHRASE_SEARCH_METHODS = {
        TOKENS: has_tokens,
        STRING: has_string
    }
