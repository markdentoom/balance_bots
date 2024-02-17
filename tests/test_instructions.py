import unittest
from src.balance_bots import Instructions


class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.instructions = Instructions("tests/fixtures/test_input.txt")

    def test_input_lines(self):
        input_lines = self.instructions.input_lines()
        expected_result = [
            "bot 119 gives low to bot 18 and high to bot 3",
            "value 61 goes to bot 119"
        ]
        self.assertEqual(input_lines, expected_result)

    def test_input_lines_invalid_path(self):
        instructions = Instructions("non-existant/file/path")
        with self.assertRaises(FileNotFoundError):
            instructions.input_lines()

    def test_get_ints_from_line(self):
        first_line = self.instructions.input_lines()[0]
        ints_from_line = self.instructions.get_ints_from_line(first_line)
        expected_result = [119, 18, 3]
        self.assertEqual(ints_from_line, expected_result)

    def test_get_ints_from_line_empty_if_line_has_no_ints(self):
        line_without_numbers = "this line has no numbers!"
        ints_from_line = self.instructions.get_ints_from_line(line_without_numbers)
        expected_result = []
        self.assertEqual(ints_from_line, expected_result)

    def test_initial_bot_values(self):
        initial_bot_values = self.instructions.initial_bot_values()
        expected_result = {119: [61]}
        self.assertEqual(initial_bot_values, expected_result)

    def test_bot_instructions(self):
        bot_instructions = self.instructions.bot_instructions()
        expected_result = {119: (('bot', 18), ('bot', 3))}
        self.assertEqual(bot_instructions, expected_result)
