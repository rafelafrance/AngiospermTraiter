# import unittest
#
# from angiosperm.pylib.rules.flowers_in_an_inflorescence import (
#     FlowersInAnInflorescence,
# )
# from tests.setup import parse
#
#
# class TestFlowersInAnInflorescence(unittest.TestCase):
#     def test_flowers_in_an_inflorescence_01(self):
#         self.assertEqual(
#             parse("general_floral", "flowers (8–)10(–16)."),
#             [FlowersInAnInflorescence(min=8, low=10, max=16, start=0, end=19)],
#         )
#
#     def test_flowers_in_an_inflorescence_02(self):
#         self.assertEqual(
#             parse("general_floral", "8–10–flowered"),
#             [FlowersInAnInflorescence(low=8, high=10, start=0, end=13)],
#         )
