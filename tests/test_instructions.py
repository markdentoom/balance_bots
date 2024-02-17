from unittest import TestCase
from src.balance_bots import Instructions


class TestInstructions(TestCase):
    def setUp(self):
        self.instructions = Instructions("tests/fixtures/test_input.txt")

    def test_initial_input_lines(self):
        expected_result = [
            "value 5 goes to bot 2",
            "bot 2 gives low to bot 1 and high to bot 0",
            "value 3 goes to bot 1",
            "bot 1 gives low to output 1 and high to bot 0",
            "bot 0 gives low to output 2 and high to output 0",
            "value 2 goes to bot 2"
        ]
        self.assertEqual(self.instructions.input_lines, expected_result)

    def test_get_initial_input_lines_with_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            Instructions("non-existant/file/path")

    def test_get_ints_from_value_line(self):
        line = self.instructions.input_lines[0]
        ints_from_line = self.instructions.get_ints_from_line(line)

        expected_result = [5, 2]
        self.assertEqual(ints_from_line, expected_result)

    def test_get_ints_from_bot_line(self):
        line = self.instructions.input_lines[1]
        ints_from_line = self.instructions.get_ints_from_line(line)

        expected_result = [2, 1, 0]
        self.assertEqual(ints_from_line, expected_result)

    def test_get_ints_from_line_empty_if_line_has_no_ints(self):
        line_without_numbers = "this line has no numbers!"
        ints_from_line = self.instructions.get_ints_from_line(line_without_numbers)

        expected_result = []
        self.assertEqual(ints_from_line, expected_result)

    def test_initial_bot_values(self):
        initial_bot_values = self.instructions.initial_bot_values()
        expected_result = {1: [3], 2: [5, 2]}
        self.assertEqual(initial_bot_values, expected_result)

    def test_bot_instructions(self):
        bot_instructions = self.instructions.bot_instructions()
        expected_result = {
            0: (('output', 2), ('output', 0)),
            1: (('output', 1), ('bot', 0)),
            2: (('bot', 1), ('bot', 0))
        }
        
        self.assertEqual(bot_instructions, expected_result)
