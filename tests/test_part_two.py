import time

import pytest
from textdistance import damerau_levenshtein

from puzzler.descramble import descramble
from puzzler.models import WORD_SPLIT
from puzzler.scramble import scramble
from tests.test_part_one import TEST_A, TEST_APOSTROPHE, TEST_HYPHEN, TEST_NUMBERS, TEST_PUNCTUATION, SAMPLE_TEXTS


TEST_CAPS = "One two"


def scramble_descramble_distance(text):
    scrambled = scramble(text, 0.5)
    descrambled = descramble(scrambled)
    return damerau_levenshtein(text, descrambled)


def test_descramble_caps():
    assert scramble_descramble_distance(TEST_CAPS) == 0


def test_descramble_a():
    assert scramble_descramble_distance(TEST_A) <= 1


def test_descramble_apostrophe():
    assert scramble_descramble_distance(TEST_APOSTROPHE) <= 1


def test_descramble_hyphen():
    assert scramble_descramble_distance(TEST_HYPHEN) <= 1


def test_descramble_numbers():
    assert scramble_descramble_distance(TEST_NUMBERS) <= 1


def test_descramble_punctuation():
    assert scramble_descramble_distance(TEST_PUNCTUATION) <= 1


def test_descramble_sample_texts():
    for text in SAMPLE_TEXTS:
        distance = scramble_descramble_distance(text)
        assert distance <= 0.2 * len(text)
        print(f"{text[0:25]}... distance: {distance} / {len(text)}")


def test_speed():
    with open('data/books/84-0.txt', 'r') as f:
        scrambled = scramble(f.read(), 0.6)
    start = time.time_ns()
    descrambled = descramble(scrambled)
    end = time.time_ns()
    time_usec = (end - start) / 1000
    time_per_word = time_usec / len(WORD_SPLIT.split(descrambled))
    print(f"time per word {time_per_word}us")
    assert time_per_word < 10

