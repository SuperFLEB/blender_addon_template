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


class UIListSortTest(unittest.TestCase):
    def test_empty(self):
        provided = []
        expected = []
        self.assertEqual(util.uilist_sort(provided), expected)

    def test_one_item(self):
        provided = ["A"]
        expected = [0]
        self.assertEqual(util.uilist_sort(provided, lambda value: value), expected)

    def test_many_shuffled(self):
        provided = list("BFCAED")
        expected = [1, 5, 2, 0, 4, 3]
        self.assertEqual(util.uilist_sort(provided, lambda value: value), expected)

    def test_many_shuffled_except_first_and_last(self):
        provided = list("ADCBEF")
        expected = [0, 3, 2, 1, 4, 5]
        self.assertEqual(util.uilist_sort(provided, lambda value: value), expected)

    def test_many_inverted(self):
        provided = list("FEDCBA")
        expected = [5, 4, 3, 2, 1, 0]
        self.assertEqual(util.uilist_sort(provided, lambda value: value), expected)

    def test_many_already_sorted(self):
        provided = list("ABCDEF")
        expected = [0, 1, 2, 3, 4, 5]
        self.assertEqual(util.uilist_sort(provided, lambda value: value), expected)

    def test_many_numeric_shuffled(self):
        # Just to make sure numeric sort values work
        provided = [2, 30, 3, 1, 20, 10]
        expected = [1, 5, 2, 0, 4, 3]
        self.assertEqual(util.uilist_sort(provided, lambda value: value), expected)

    def test_make_sortable(self):
        """Verify that the make_sortable_fn param actually runs, by having it invert the expected order"""
        provided = [0, 1, 2, 3, 4, 5]

        def make_sortable_fn(val: int) -> int:
            return 100 - val

        expected = [5, 4, 3, 2, 1, 0]
        self.assertEqual(util.uilist_sort(provided, make_sortable_fn), expected)


if __name__ == '__main__':
    unittest.main()
