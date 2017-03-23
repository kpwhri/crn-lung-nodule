"""
# Scott Halgrim #
# 12/20/13 #
# Main script to replicate the modified Danforth algorithm documented best in
# NLP_algorithm_Revisions_(09 19 2013)_CZ.doc. Script will take as input a
# directory of transcripts and its output will be a file indicating which are
# positive and which are negative.
"""

import logging
import os

from crn_lung_nodule.util.document import Document, TOKENS, DANFORTH_20130919

# get module logger
logger = logging.getLogger('ghri.scott.crn_lung_nodule.danforth_20130919')


def process_file(filename, phrase_search_method=TOKENS,
                 get_largest_nodule_size=False,
                 rule6_phrase_search_method=None, algorithm=DANFORTH_20130919):
    doc = Document(filename, phrase_search_method, rule6_phrase_search_method)
    return (doc.isPositive(algorithm),
            doc.getMaxNoduleSize() if get_largest_nodule_size else None)


def extract(indir, phrase_search_method=TOKENS, get_largest_nodule_size=False,
            rule6_phrase_search_method=None, algorithm=DANFORTH_20130919, outfn=None):
    logger.debug('Processing files in {}.'.format(indir))
    with open(outfn, 'w') as out:
        for fn in sorted(os.listdir(indir)):
            ffn = os.path.join(indir, fn)
            decision, max_nodule_size = process_file(ffn, phrase_search_method,
                                                     get_largest_nodule_size,
                                                     rule6_phrase_search_method, algorithm)
            logger.debug('{} classified as {}'.format(fn, str(decision)))
            if get_largest_nodule_size:
                out.write('{}\t{}\t{}\n'.format(fn, decision, max_nodule_size))
            else:
                out.write('{}\t{}\n'.format(fn, decision))
