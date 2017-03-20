import re

POS_KEYWORD = 'posKeyword'
NLP_POSITIVE = 'nlpPositive'
NLP_NEGATIVE = 'nlpNegative'
ABS_DISQUAL_TERM = 'absolutelyDisqualifyingTerm'
EXCLUDED_TERM = 'excludedTerm'
OFFSETTING_TERM = 'hasOffsettingTerm'
POS_KEYWORD_QUAL_REQD = 'posKeywordQualReqd'
POS_KEYWORD_NO_QUAL_REQD = 'posKeywordNoQualReqd'
SIZE_GT_30_MM = 'sizeGt30mm'
SIZE_GT_5_MM = 'sizeGt5mm'
SIZE_GT_0_MM = 'sizeGt0mm'
DANFORTH_20130919 = 'Danforth20130919'
FARJAH_20140903 = 'Farjah20140903'

# phrase search methods
TOKENS = 'phrase_search_tokens'
STRING = 'phrase_search_string'

DATA_MAPPING = {
    DANFORTH_20130919: {
        # Tables 1.A, 1B
        POS_KEYWORD: [
                        'NOQUAL',
                        'QUAL'
                    ],
        ABS_DISQUAL_TERM: [
                        'DISQUAL'
                            ],
        EXCLUDED_TERM: [
                        'EXCLUDE'
                        ],
        OFFSETTING_TERM: [
                          'OFFSET'
                        ],

        # Table 1.B
        POS_KEYWORD_NO_QUAL_REQD: [
                                   'NOQUAL'
                                   ],

        # Table 1.A
        POS_KEYWORD_QUAL_REQD: [
                'QUAL'
                                ]
        }
}

# Adding here to allow me to run different experiments
SIZE_REGEXES = [
                re.compile(r'(?P<size>(\d+(\.\d+)?)|(\.\d+))(((\s)*)|-)(?P<dim>c|m)m')
                ]

