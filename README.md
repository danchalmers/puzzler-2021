# Christmas Puzzler 2021: Text Scrambler / Descrambler

## The Problem

Parameters:
text: a text string
amount: 0.0 ... 1.0

Scramble should rearrange the letters within words, not across them.
Whitespace and punctuation should be preserved in place.

The amount means:
 - 0: no change
 - otherwise, a higher number is more scrambled


## My Solution

In this implementation, for each word there are `⌈ length(word) * amount * 0.5 ⌉` letter swaps in the word, 
and each occurrence of a word gets the same scrambling (although capitalization and punctuation are seen as a new word).

To run the scrambler, provide amount, in-file, out-file:
```python
$ time poetry run python -m puzzler.scramble 0.5 data/books/84-0.txt test.txt

real	0m0.391s
user	0m0.358s
sys	0m0.032s

$ time poetry run python -m puzzler.descramble test.txt test-undo.txt

real	0m1.430s
user	0m1.361s
sys	0m0.070s

$ wc data/books/84-0.txt test.txt test-undo.txt
   7743   78122  448821 data/books/84-0.txt
   7743   78122  441078 test.txt
   7743   78122  441008 test-undo.txt
  23229  234366 1330907 total
```
(The character difference is down to whitespace changes.)


### Data Not In Repo

The descrambler uses a word frequency table in `data/external/unigram_freq.csv.zip` downloaded from [Kaggle English Word Frequency derived from the Google Web Trillion Word Corpus](https://www.kaggle.com/rtatman/english-word-frequency/version/1).

The test book is [Frankenstein, from Gutenberg](https://www.gutenberg.org/ebooks/84).

### Sample Input / Output

The first paragraph of Frankenstein is
> You will rejoice to hear that no disaster has accompanied the
commencement of an enterprise which you have regarded with such evil
forebodings. I arrived here yesterday, and my first task is to assure
my dear sister of my welfare and increasing confidence in the success
of my undertaking.

Scrambled at an amount of 1 gives
> You wlil irejeoc ot rhea taht on iedstsra sah acmcdapnioe teh
omectmecenmn fo na netrerepsi cihwh oyu haev rdegeard with such liev
soifrodbeng. I aervidr eehr ysredtaye, dan ym rftis astk si ot suraes
ym edra sisrte fo ym fealrwe dan neiciansgr cfdonciene ni teh uscscse
fo ym utinnedrakg.

Descrambled gives
> You will rejoice to hear that no disaster has accompanied the
commencement of an enterprise which you have regarded with such evil
forebodings. I arrived here yesterday, and my first task is to assure
my read sister of my welfare and increasing confidence in the success
of my undertaking.
> 