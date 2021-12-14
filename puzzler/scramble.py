import math
import re
from functools import lru_cache
from random import choice

from pipe import map

from puzzler.models import Text, AmountNorm, Word


WORD_SPLIT = re.compile(r'\b')


def _allowed_indicies(word: Word, exclude: int = -1) -> list[int]:
    return [i for i, c in enumerate([c for c in word]) if c.isalpha() if i != exclude]


def n_move_scramble(word: Word, amount: AmountNorm) -> Word:
    word_size = len(word)
    if word_size <= 1:
        return word
    indices = list(range(word_size))
    rounds = math.ceil(len(word) * amount)
    for r in range(rounds):
        move_idx = choice(_allowed_indicies(word))
        move_to = choice(_allowed_indicies(word, exclude=move_idx))
        indices.insert(move_to, indices.pop(move_idx))
    return ''.join([word[i] for i in indices])


@lru_cache(maxsize=2**16)
def scramble_word(word: Word, amount: AmountNorm) -> Word:
    if word.isalpha():
        return n_move_scramble(word, amount)
    else:
        return word


def scramble(text: Text, amount: AmountNorm) -> Text:
    amount = amount / 2
    return "".join(
        WORD_SPLIT.split(text)
        | map(lambda w: scramble_word(w, amount))
    )
