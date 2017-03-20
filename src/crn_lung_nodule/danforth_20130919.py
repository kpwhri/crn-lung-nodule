'''
# Scott Halgrim #
# 12/20/13 #
# Main script to replicate the modified Danforth algorithm documented best in
# NLP_algorithm_Revisions_(09 19 2013)_CZ.doc. Script will take as input a
# directory of transcripts and its output will be a file indicating which are
# positive and which are negative.
'''

import ConfigParser
import logging
import os
from ConfigParser import NoOptionError

from crn_lung_nodule import ConfigFileParser
from crn_lung_nodule import myos
from crn_lung_nodule.classes.document import Document

from crn_lung_nodule.util.constants import *

# get module logger
logger = logging.getLogger('ghri.scott.crn_lung_nodule.danforth_20130919')

def process_file(filename, phraseSearchMethod=TOKENS,
                 getLargestNoduleSize = False,
                 rule6PhraseSearchMethod =  None, algo=DANFORTH_20130919):

    if not rule6PhraseSearchMethod:
        rule6PhraseSearchMethod = phraseSearchMethod

    doc = Document(filename, phraseSearchMethod, rule6PhraseSearchMethod)
    classification = doc.isPositive(algo)

    if getLargestNoduleSize:
        maxNoduleSize = doc.getMaxNoduleSize()
    else:
        maxNoduleSize = None

    return classification, maxNoduleSize

def main(indir, phraseSearchMethod = TOKENS, getLargestNoduleSize = False, 
         rule6PhraseSearchMethod = None, algorithm=DANFORTH_20130919, outfn=None):

    if not rule6PhraseSearchMethod:
        rule6PhraseSearchMethod = phraseSearchMethod

    outlines = []

    fnlisting = sorted(os.listdir(indir))
    logger.debug('processing %d files in %s'%(len(fnlisting), indir))

    for fn in sorted(os.listdir(indir)):
        ffn = os.path.join(indir, fn)
        decision, maxNoduleSize = process_file(ffn, phraseSearchMethod, 
                                               getLargestNoduleSize,
                                               rule6PhraseSearchMethod, algorithm)
        logger.debug('%s classified as %s'%(fn, str(decision)))

        if getLargestNoduleSize:
            outlines.append('\t'.join([fn, str(decision), str(maxNoduleSize)]))
        else:
            outlines.append('\t'.join([fn, str(decision)]))
        
    myos.writelines(outlines, outfn)

    return

if __name__ == '__main__':

    # usage string to give if user asks for help or gets command line wrong
    usageStr = '%(prog)s configfile [options]'

    # command line parser
    parser = ConfigFileParser(usage=usageStr)

    # parse the command line into command line options
    options = parser.parse_args()

    # start logging at root according to command line
    # si.mylogger.config(logfn=options.logfile, logmode=options.logmode, \
    #                                                 loglevel=options.loglevel)

    # set module logging level to input
    logger.setLevel(options.loglevel)

    # create config file parser
    cp = ConfigParser.SafeConfigParser({'PhraseSearchMethod':
                                               'phrase_search_tokens',
                                           'GetLargestNoduleSize': False,
                                           'Algorithm': DANFORTH_20130919})    
    cp.read(options.configfile)

    # parse the config file
    indir = cp.get('Main', 'InputDirectory')
    phraseSearchMethod = cp.get('Main', 'PhraseSearchMethod')

    try:
        rule6PhraseSearchMethod = cp.get('Main', 'Rule6PhraseSearchMethod')
    except NoOptionError:
        rule6PhraseSearchMethod = phraseSearchMethod

    getLargestNoduleSize = cp.getboolean('Main', 'GetLargestNoduleSize')
    algo = cp.get('Main', 'Algorithm')
    outfn = options.outfile

    # let's get the party started
    main(indir, phraseSearchMethod, getLargestNoduleSize,
         rule6PhraseSearchMethod, algo, outfn)
