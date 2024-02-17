from unittest import TestCase
from unittest.mock import MagicMock
from src.balance_bots import Instructions, Factory


class TestFactory(TestCase):
    def setUp(self):
        self.instructions = Instructions("tests/fixtures/test_input.txt")
        self.factory = Factory(self.instructions)

    def test_dynamic_initial_values(self):
        self.assertEqual(self.factory.bot_instructions, self.instructions.bot_instructions())
        self.assertEqual(self.factory.current_bot_values, self.instructions.initial_bot_values())
        self.assertEqual(self.factory.stack, [2])

    def test_first_bot_with_2_microchips(self):
        expected_result = 2
        self.assertEqual(self.factory.first_bot_with_2_microchips(), expected_result)

    def test_give_microchip_to_bot_with_existing_microchip(self):
        expected_initial = [3]
        self.assertEqual(self.factory.current_bot_values[1], expected_initial)

        self.factory.give_microchip_to_bot(1, 2)
        expected_result = [3, 2]
        self.assertEqual(self.factory.current_bot_values[1], expected_result)

    def test_give_microchip_to_bot_without_existing_microchip(self):
        expected_initial = {2: [5, 2], 1: [3]}
        self.assertEqual(self.factory.current_bot_values, expected_initial)

        self.factory.give_microchip_to_bot(0, 2)
        expected_result = {2: [5, 2], 1: [3], 0: [2]}
        self.assertEqual(self.factory.current_bot_values, expected_result)

    def test_give_microchip_to_recipient_bot(self):
        self.factory.give_microchip_to_bot = MagicMock()
        self.factory.give_microchip_to_recipient("bot", 1, 2)
        self.factory.give_microchip_to_bot.assert_called_once_with(1, 2)

    def test_give_microchip_to_recipient_bin_with_existing_microchip(self):
        self.factory.current_bin_values[0] = [2]
        self.factory.give_microchip_to_recipient("output", 0, 1)
        expected_result = [2, 1]
        self.assertEqual(self.factory.current_bin_values[0], expected_result)

    def test_give_microchip_to_recipient_bin_without_existing_microchip(self):
        expected_initial = {}
        self.assertEqual(self.factory.current_bin_values, expected_initial)

        self.factory.give_microchip_to_recipient("output", 0, 2)
        expected_result = {0: [2]}
        self.assertEqual(self.factory.current_bin_values, expected_result)

    def test_run_using_fixture(self):
        self.assertEqual(self.factory.current_bot_values, {2: [5, 2], 1: [3]})
        self.assertEqual(self.factory.current_bin_values, {})
        self.assertEqual(self.factory.special_bot, None)
        self.factory.run()

        self.assertEqual(self.factory.current_bot_values, {})
        self.assertEqual(self.factory.current_bin_values, {0: [5], 1: [2], 2: [3]})
        self.assertEqual(self.factory.special_bot, None)

    def test_run_special_bot_value(self):
        self.factory.bot_instructions = {2: (('output', 0), ('output', 1))}
        self.factory.current_bot_values = {2: [61, 17]}
        self.factory.run()

        self.assertEqual(self.factory.special_bot, 2)

    def test_multiplied_bin_0_1_2_outputs_before_running(self):
        with self.assertRaises(IndexError):
            self.factory.multiplied_bin_0_1_2_outputs()

    def test_multiplied_bin_0_1_2_outputs(self):
        self.factory.current_bin_values = {0: [2], 1: [2], 2: [2]}
        expected_result = 8
        self.assertEqual(self.factory.multiplied_bin_0_1_2_outputs(), expected_result)

    def test_multiplied_bin_0_1_2_outputs_from_fixtures(self):
        self.factory.run()
        expected_result = 30
        self.assertEqual(self.factory.multiplied_bin_0_1_2_outputs(), expected_result)

    def test_assignment_answers(self):
        instructions = Instructions("src/input.txt")
        factory = Factory(instructions)
        factory.run()

        self.assertEqual(factory.special_bot, 73)
        self.assertEqual(factory.multiplied_bin_0_1_2_outputs(), 3965)
