
import pytest
from textdistance import damerau_levenshtein

from puzzler.scramble import scramble


SAMPLE_TEXTS = [
"""
The Nascom 1 and 2 were single-board computer kits issued in the United Kingdom in 1977 and 1979, respectively, based
on the Zilog Z80 and including a keyboard and video interface, a serial port that could be used to store data on a
tape cassette using the Kansas City standard, and two 8-bit parallel ports. At that time, including a full keyboard
and video display interface was uncommon, as most microcomputer kits were then delivered with only a hexadecimal
keypad and seven-segment display. To minimize cost, the buyer had to assemble a Nascom by hand-soldering about 3,000
joints on the single circuit board.
""",
]

TEST_A = "A single character word."
TEST_APOSTROPHE = "Apostrophes, they're enjoyed by grocer's and pedants!"
TEST_HYPHEN = "Hyphens for double-barrelled stuff?"
TEST_NUMBERS = "2020 was the 19th year of the 21st century."
TEST_PUNCTUATION = "A lot of punctuation, can be confusing?!!!1?eleven! #*!?* Yes?"


@pytest.fixture
def scrambled_samples_zero():
    return zip(SAMPLE_TEXTS, [scramble(t, 0) for t in SAMPLE_TEXTS])


@pytest.fixture
def scrambled_samples_zero_one():
    return zip(SAMPLE_TEXTS, [scramble(t, 0.4) for t in SAMPLE_TEXTS])


@pytest.fixture
def scrambled_samples_zero_three():
    return zip(SAMPLE_TEXTS, [scramble(t, 0.3) for t in SAMPLE_TEXTS])


@pytest.fixture
def scrambled_samples_zero_five():
    return zip(SAMPLE_TEXTS, [scramble(t, 0.5) for t in SAMPLE_TEXTS])


@pytest.fixture
def scrambled_samples_one():
    return zip(SAMPLE_TEXTS, [scramble(t, 1) for t in SAMPLE_TEXTS])


def test_a():
    result = scramble(TEST_A, 0.5).split()
    assert 'A' == result[0]


def test_apostrophe():
    original_result = zip(TEST_APOSTROPHE.split(), scramble(TEST_APOSTROPHE, 0.5).split())
    for word in original_result:
        if "'" in word[0]:
            assert "'" in word[1]
            parts = zip(word[0].split("'"), word[1].split("'"))
            for part in parts:
                assert len(part[1]) == len(part[0])
                assert set(part[1]) == set(part[0])


def test_hyphen():
    original_result = zip(TEST_HYPHEN.split(), scramble(TEST_HYPHEN, 0.5).split())
    for word in original_result:
        if "-" in word[0]:
            assert "-" in word[1]
            parts = zip(word[0].split("-"), word[1].split("-"))
            for part in parts:
                assert len(part[1]) == len(part[0])
                assert  set(part[1]) == set(part[0])


def test_numbers():
    original_result = zip(TEST_NUMBERS.split(), scramble(TEST_NUMBERS, 0.5).split())
    for word in original_result:
        if word[0].isnumeric():
            assert word[1] == word[0]


def test_punctuation():
    original_result = zip(TEST_PUNCTUATION, scramble(TEST_PUNCTUATION, 0.5))
    for c in original_result:
        if not c[0].isalpha():
            assert c[1] == c[0]


def test_zero_is_not_scrambled(scrambled_samples_zero):
    for sample in scrambled_samples_zero:
        assert sample[1] == sample[0]


def _is_scrambled(sample):
    return any([sample[0][i] != sample[1][i] for i in range(len(sample[0])) if sample[0][i].isalpha()])


def test_zero_one_is_scrambled(scrambled_samples_zero_one):
    for sample in scrambled_samples_zero_one:
        assert _is_scrambled(sample), sample[1]


def test_zero_five_is_scrambled(scrambled_samples_zero_five):
    for sample in scrambled_samples_zero_five:
        assert _is_scrambled(sample), sample[1]


def test_one_is_scrambled(scrambled_samples_one):
    for sample in scrambled_samples_one:
        assert _is_scrambled(sample), sample[1]


def test_zero_less_scrambed_than_one(scrambled_samples_zero, scrambled_samples_one):
    low_distances = [damerau_levenshtein(orig_scrambled[0], orig_scrambled[1]) for orig_scrambled in scrambled_samples_zero]
    for d in low_distances:
        assert d == 0
    high_distances = [damerau_levenshtein(orig_scrambled[0], orig_scrambled[1]) for orig_scrambled in scrambled_samples_one]
    for i in range(len(low_distances)):
        assert low_distances[i] < high_distances[i]


def test_zero_one_less_scrambed_than_one(scrambled_samples_zero_one, scrambled_samples_one):
    low_distances = [damerau_levenshtein(orig_scrambled[0], orig_scrambled[1]) for orig_scrambled in scrambled_samples_zero_one]
    high_distances = [damerau_levenshtein(orig_scrambled[0], orig_scrambled[1]) for orig_scrambled in scrambled_samples_one]
    for i in range(len(low_distances)):
        assert low_distances[i] < high_distances[i]


def test_zero_five_less_scrambed_than_one(scrambled_samples_zero_five, scrambled_samples_one):
    low_distances = [damerau_levenshtein(orig_scrambled[0], orig_scrambled[1]) for orig_scrambled in scrambled_samples_zero_five]
    high_distances = [damerau_levenshtein(orig_scrambled[0], orig_scrambled[1]) for orig_scrambled in scrambled_samples_one]
    for i in range(len(low_distances)):
        assert low_distances[i] < high_distances[i]


def test_zero_four_less_scrambed_than_zero_five(scrambled_samples_zero_three, scrambled_samples_zero_five):
    low_distances = [damerau_levenshtein(orig_scrambled[0], orig_scrambled[1]) for orig_scrambled in scrambled_samples_zero_three]
    high_distances = [damerau_levenshtein(orig_scrambled[0], orig_scrambled[1]) for orig_scrambled in scrambled_samples_zero_five]
    for i in range(len(low_distances)):
        assert low_distances[i] < high_distances[i]