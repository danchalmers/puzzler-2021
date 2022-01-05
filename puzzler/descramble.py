
import csv
import sys
from collections import defaultdict
from io import TextIOWrapper
from zipfile import ZipFile

from pipe import sort, map


from .models import WORD_SPLIT, ALPHA_RE, Word, Text, WordKey, ScrambledWord, Count, Vocab, ScrambledKeyUse, \
    DecodeLookup


WORD_FREQ_FILE = 'data/external/unigram_freq.csv.zip'


def word_to_key(word: Word) -> str:
    return tuple(word.casefold() | sort)


def load_vocab() -> Vocab:
    vocab = defaultdict(dict)
    with ZipFile(WORD_FREQ_FILE) as zf:
        with zf.open('unigram_freq.csv', 'r') as infile:
            reader = csv.DictReader(TextIOWrapper(infile, 'utf-8'))
            for row in reader:
                key = word_to_key(row['word'])
                vocab[key][row['word']] = int(row['count'])
    return vocab


def split_text(text: Text) -> tuple[ScrambledKeyUse, list[ScrambledWord]]:
    key_use = defaultdict(lambda: defaultdict(int))
    part_seq = []
    for word in WORD_SPLIT.split(text):
        for part in ALPHA_RE.split(word):
            if len(part) > 0:
                key = word_to_key(part)
                key_use[key][part] += 1
                part_seq.append(part)
    return key_use, part_seq


def create_decode_lookup(vocab: Vocab, key_use: ScrambledKeyUse) -> DecodeLookup:
    decode_lookup = {}
    for key, part_count in key_use.items():
        if all(key | map(lambda k: k.isalpha())) and key in vocab:
            for part_vocab in zip(
                    sorted({p: c for p, c in part_count.items() if p.islower()}.items(), key=lambda kv: kv[1], reverse=True),
                    sorted(vocab.get(key, {}).items(), key=lambda kv: kv[1], reverse=True)
            ):
                scrambled = part_vocab[0][0]
                word = part_vocab[1][0]
                decode_lookup[scrambled] = word

            # Capitalised words need to restart the word frequency lookup
            for part_vocab in zip(
                    sorted({p: c for p, c in part_count.items() if not p.islower()}.items(), key=lambda kv: kv[1], reverse=True),
                    sorted(vocab.get(key, {}).items(), key=lambda kv: kv[1], reverse=True)
            ):
                scrambled = part_vocab[0][0]
                word = part_vocab[1][0].capitalize()
                decode_lookup[scrambled] = word
        else:
            for p, c in part_count.items():
                decode_lookup[p] = p
    return decode_lookup


def descramble_word(decode_lookup: DecodeLookup, word: ScrambledWord) -> Word:
    decoded_word = decode_lookup.get(word, word)
    return decoded_word


def descramble(text: Text):
    vocab = load_vocab()
    key_use, part_seq = split_text(text)
    decode_lookup = create_decode_lookup(vocab, key_use)
    return ''.join([descramble_word(decode_lookup, sw) for sw in part_seq])


if __name__ == "__main__":
    from_file_name = sys.argv[1]
    to_file_name = sys.argv[2]
    with open(from_file_name, 'r') as from_file:
        descrambled = descramble(from_file.read())
    with open(to_file_name, 'w') as to_file:
        to_file.write(descrambled)
