"""
    Scott Halgrim
    12/20/13 
    Main script to replicate the modified Danforth algorithm documented best in
    NLP_algorithm_Revisions_(09 19 2013)_CZ.doc. Script will take as input a
    directory of transcripts and its output will be a file indicating which are
    positive and which are negative.
"""

import logging
import os

from crn_lung_nodule.util.constants import STRING, FARJAH_20140903
from crn_lung_nodule.util.document import Document, TOKENS

# get module logger
logger = logging.getLogger('crn_lung_nodule.danforth_algorithm')
CODEC = None


def get_file_contents(fp, codec=None):
    global CODEC
    name = os.path.basename(fp)
    e, contents = None, None
    for cdc in [codec, CODEC] + ['cp1252', 'latin1', 'utf8']:
        if not cdc:
            continue
        with open(fp, encoding=cdc) as f:
            try:
                contents = f.read()
            except UnicodeDecodeError as e:
                logger.warning('Failed to decode file {} with codec {}. Retrying.'.format(name, cdc))
            else:
                if cdc != codec:
                    logger.info('Using codec {} for {}.'.format(codec, name))
                    CODEC = cdc
                return contents
    if not contents or not e:
        raise ValueError('Unable to parse file. Unknown error for file {}.'.format(name))
    else:
        raise e


def process_document(name, contents, phrase_search_method=STRING,
                     get_largest_nodule_size=False,
                     rule6_phrase_search_method=TOKENS, algorithm=FARJAH_20140903):
    doc = Document(name, contents, phrase_search_method, rule6_phrase_search_method)
    return (name,
            doc.is_positive(algorithm),
            doc.get_max_nodule_size() if get_largest_nodule_size else None)


def extract_iterators(name_iter, contents_iter, **kwargs):
    """

    :param name_iter:
    :param contents_iter:
    :param kwargs: keyword args to pass to process_document; defaults=
        * phrase_search_method=TOKENS
        * get_largest_nodule_size=False
        * rule6_phrase_search_method=None
        * algorithm=FARJAH_20140903
    :return: name, decision, [max_nodule_size]
    """
    for name, contents in zip(name_iter, contents_iter):
        result = process_document(name, contents, **kwargs)
        logger.debug('{} classified as {}'.format(result[0], result[1]))
        yield result  # name, decision, [max_nodule_size]


def extract_files(indir, codec=None, **kwargs):
    """

    :param indir:
    :param codec:
    :param kwargs: keyword args to pass to process_document; defaults=
        * phrase_search_method=TOKENS
        * get_largest_nodule_size=False
        * rule6_phrase_search_method=None
        * algorithm=FARJAH_20140903
    :return: name, decision, [max_nodule_size]
    """
    logger.debug('Processing files in {}.'.format(indir))
    for fn in sorted(os.listdir(indir)):
        contents = get_file_contents(os.path.join(indir, fn), codec)
        result = process_document(fn, contents, **kwargs)
        logger.debug('{} classified as {}'.format(result[0], result[1]))
        yield result  # name, decision, [max_nodule_size]
