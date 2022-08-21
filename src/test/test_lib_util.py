from . import pkg

__package__ = pkg()

import unittest
from ..lib import util


class FlattenTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual([1, 2, 3, 4, 5, 6], util.flatten([[1, 2], [3, 4], [5, 6]]))

    def test_single_wrapped_list(self):
        self.assertEqual([1, 2, 3, 4, 5, 6], util.flatten([[1, 2, 3, 4, 5, 6]]))

    def test_empty_lists(self):
        self.assertEqual([1, 2, 3, 4, 5, 6], util.flatten([[], [1, 2], [], [], [3, 4], [], [5, 6], []]))

    def test_all_empty_lists(self):
        self.assertEqual([], util.flatten([[], [], []]))

    def test_no_lists(self):
        self.assertEqual([], util.flatten([]))


class WordWrapTest(unittest.TestCase):
    def test_split(self):
        provided = "123 56 890 234 67"
        expected = ["123 56", "890", "234 67"]
        self.assertEqual(expected, util.wordwrap(provided, 6))

    def test_long_word(self):
        provided = "The Loooooooooooooooooong cat jumped over the lazy dog."
        expected = ["The", "Loooooooooooooooooong", "cat jumped", "over the", "lazy dog."]
        self.assertEqual(expected, util.wordwrap(provided, 10))

    def test_no_split_necessary(self):
        provided = "The quick brown fox jumped over the lazy dog."
        expected = ["The quick brown fox jumped over the lazy dog."]
        self.assertEqual(expected, util.wordwrap(provided, 100))

    def test_collapse_spaces(self):
        provided = "   In    space,    no    one   can   hear   you   scream."
        expected = ["In space,", "no one can", "hear you", "scream."]
        self.assertEqual(expected, util.wordwrap(provided, 10))

    def test_empty(self):
        provided = ""
        expected = []
        self.assertEqual(expected, util.wordwrap(provided, 10))

    def test_only_spaces(self):
        provided = "        "
        expected = []
        self.assertEqual(expected, util.wordwrap(provided, 10))


if __name__ == '__main__':
    unittest.main()
