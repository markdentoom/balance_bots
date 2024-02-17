from unittest import TestCase
from src.balance_bots import Instructions, Factory


class TestAssignment(TestCase):
    def setUp(self):
        instructions = Instructions("src/input.txt")
        self.factory = Factory(instructions)
        self.factory.run()

    def test_first_assignment_question(self):
        self.assertEqual(self.factory.special_bot, 73)

    def test_second_assignment_question(self):
        self.assertEqual(self.factory.multiplied_bin_0_1_2_outputs(), 3965)
