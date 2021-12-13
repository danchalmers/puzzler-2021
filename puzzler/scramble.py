import re
from random import random
from collections import deque

from pipe import map

from puzzler.models import Text, AmountNorm, Word

WORD_SPLIT = re.compile(r'(\b|\W)')


def _bubble_scramble(word: Word, amount: AmountNorm) -> Word:
    rounds = int((len(word) - 1) * amount)
    amount = 0.5 * amount
    result = word
    for r in range(rounds):
        q = deque(result)
        result = []
        while len(q) > 1:
            keep = q.popleft()
            swap = q.popleft()
            if random() > amount:
                result.append(swap)
                q.appendleft(keep)
            else:
                result.append(keep)
                q.appendleft(swap)
        if q:
            result.append(q.popleft())
    return ''.join(result)


def scramble_word(word: Word, amount: AmountNorm) -> Word:
    if word.isalpha():
        return _bubble_scramble(word, amount)
    else:
        return word


def scramble(text: Text, amount: AmountNorm) -> Text:
    scrambled = "".join(
        WORD_SPLIT.split(text)
        | map(lambda w: scramble_word(w, amount))
    )
    return scrambled
