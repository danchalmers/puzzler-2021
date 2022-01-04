# Christmas Puzzler 2021

## Part One: Text Scrambler

Parameters:
text: a text string
amount: 0.0 ... 1.0

Scramble should rearrange the letters within words, not across them.
Whitespace and punctuation should be preserved in place.

The amount means:
 - 0: no change
 - otherwise, a higher number is more scrambled

In this implementation, for each word there are `⌈ length(word) * amount * 0.5 ⌉` letter swaps in the word, 
and each occurrence of a word gets the same scrambling (although capitalization and punctuation are seen as a new word).

To run the scrambler, provide amount, in-file, out-file:
```python
dan@pleiades:~/Code/puzzler-2021$ time poetry run python puzzler/scramble.py 0.5 data/books/84-0.txt test.txt

real	0m0.367s
user	0m0.336s
sys	0m0.033s

$ wc data/books/84-0.txt test.txt
  7743  78122 448821 data/books/84-0.txt
  7743  78122 441078 test.txt
 15486 156244 889899 total
```
(The character difference is down to whitespace changes.)
