from . import pkg

__package__ = pkg()

import unittest
from ..lib import a_lib


class ALibTest(unittest.TestCase):
    def test_success_message(self):
        self.assertEquals(a_lib.get_success_message(), "It works!")

    def test_success_message_type(self):
        self.assertIsInstance(a_lib.get_success_message(), str)
