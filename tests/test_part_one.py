import unittest

from puzzler.scramble import scramble


SAMPLE_TEXT_1 = """
The Nascom 1 and 2 were single-board computer kits issued in the United Kingdom in 1977 and 1979, respectively, based 
on the Zilog Z80 and including a keyboard and video interface, a serial port that could be used to store data on a 
tape cassette using the Kansas City standard, and two 8-bit parallel ports. At that time, including a full keyboard 
and video display interface was uncommon, as most microcomputer kits were then delivered with only a hexadecimal 
keypad and seven-segment display. To minimize cost, the buyer had to assemble a Nascom by hand-soldering about 3,000 
joints on the single circuit board. 
"""

TEST_A = "A single character word."
TEST_APOSTROPHE = "Apostrophes, they're enjoyed by grocer's and pedants!"
TEST_HYPHEN = "Hyphens for double-barrelled stuff?"
TEST_NUMBERS = "2020 was the 19th year of the 21st century."


class PartOneTestCase(unittest.TestCase):
    def test_a(self):
        result = scramble(TEST_A, 0.5).split()
        self.assertEqual('A', result[0])

if __name__ == '__main__':
    unittest.main()
