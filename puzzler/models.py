import re

AmountNorm = float
Count = int
ScrambledWord = str
Text = str
Word = str
WordKey = tuple

Vocab = dict[WordKey, dict[Word, Count]]
ScrambledKeyUse = dict[WordKey, dict[ScrambledWord, Count]]
DecodeLookup = dict[ScrambledWord, Word]

WORD_SPLIT = re.compile(r'\b')
ALPHA_RE = re.compile(r'(\W+)')