import warnings

try:
    from crn_lung_nodule.nlp.punkt_sentence_splitter \
        import SentenceSplitterPunktStripped

    NLTK_SPLITTER = True
except ModuleNotFoundError as me:
    warnings.warn(f'nltk not installed or configured for punkt tokenizer;'
                  f' using base sentence splitter instead: {me}.')
    SentenceSplitterPunktStripped = None
    NLTK_SPLITTER = False

from crn_lung_nodule.nlp.base_sentence_splitter import BaseSentenceSplitter

DEFAULT_SENT_SPLITTER = SentenceSplitterPunktStripped if NLTK_SPLITTER else BaseSentenceSplitter
