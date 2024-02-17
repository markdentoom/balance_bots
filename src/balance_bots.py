import re
from collections import defaultdict
from typing import Optional


class Instructions:
    def __init__(self, file_path: str):
        self._input_lines = self.get_initial_input_lines(file_path)

    @property
    def input_lines(self) -> list[str]:
        return self._input_lines

    @staticmethod
    def get_initial_input_lines(file_path: str) -> list[str]:
        with open(file_path) as file_content:
            return file_content.read().splitlines()

    @staticmethod
    def get_ints_from_line(line: str) -> list[int]:
        return [int(v) for v in re.findall(r"\d+", line)]

    def initial_bot_values(self) -> dict[int, list[int]]:
        """
        Example: {119: [61], 2: [11, 17]}
        This means bot 119 starts with microchip value 61
        and that bot 2 start with microchip values 11 and 17.
        """
        initial_bot_values = defaultdict(list)

        for line in self.input_lines:
            if not line.startswith("value"):
                continue

            value, bot = self.get_ints_from_line(line)
            initial_bot_values[bot].append(value)

        return initial_bot_values

    def bot_instructions(self) -> dict[int, tuple[tuple[str, int], tuple[str, int]]]:
        """
        Example: {119: (('bot', 18), ('bot', 3)), 69: (('output', 47), ('bot', 172))}
        This means bot 119 gives low values to bot 18 and high values to bot 3
        and that bot 69 gives low values to output 47 and high values to bot 172.
        """
        bot_instructions = {}

        for line in self.input_lines:
            if not line.startswith("bot"):
                continue

            bot, gives_low_to, gives_high_to = self.get_ints_from_line(line)
            low_recipient, high_recipient = re.findall(r" (bot|output)", line)
            bot_instructions[bot] = (low_recipient, gives_low_to), (high_recipient, gives_high_to)

        return bot_instructions


class Factory:
    def __init__(self, instructions: Instructions):
        self._bot_instructions = instructions.bot_instructions()

        self.current_bot_values = instructions.initial_bot_values()
        self.current_bin_values = defaultdict(list)
        self.stack = [self.get_initial_bot_with_2_microchips()]
        self.special_bot: Optional[int] = None  # Compares microchips 17 and 61

    @property
    def bot_instructions(self):
        return self._bot_instructions

    def get_initial_bot_with_2_microchips(self) -> int:
        for bot, values in self.current_bot_values.items():
            if len(values) == 2:
                return bot

    def give_microchip_to_bot(self, bot: int, value: int) -> None:
        self.current_bot_values[bot].append(value)
        if len(self.current_bot_values[bot]) == 2:
            self.stack.append(bot)

    def give_microchip_to_recipient(self, recipient_type: str, recipient: int, value: int) -> None:
        if recipient_type == "bot":
            self.give_microchip_to_bot(recipient, value)
        elif recipient_type == "output":
            self.current_bin_values[recipient].append(value)
        else:
            raise ValueError(f"recipient_type should be 'bot' or 'output', not '{recipient_type}'")

    def run(self) -> None:
        """
        self.stack consists of a list of bots that currently have two microchips.
        The while loop below has the bots pass them on until none of them have two anymore.
        """

        while self.stack:
            bot = self.stack.pop()
            low_value, high_value = sorted(self.current_bot_values.pop(bot))

            if low_value == 17 and high_value == 61:
                self.special_bot = bot

            (low_recipient_type, low_recipient), (high_recipient_type, high_recipient) = self.bot_instructions[bot]
            self.give_microchip_to_recipient(low_recipient_type, low_recipient, low_value)
            self.give_microchip_to_recipient(high_recipient_type, high_recipient, high_value)

    def multiplied_bin_0_1_2_outputs(self) -> int:
        """Answers question 2 after having run the factory"""
        bin0, bin1, bin2 = (self.current_bin_values[bin][0] for bin in [0, 1, 2])
        return bin0 * bin1 * bin2


if __name__ == "__main__":
    instructions = Instructions("src/input.txt")
    factory = Factory(instructions)
    factory.run()

    print(f"Answer 1: {factory.special_bot}")
    print(f"Answer 2: {factory.multiplied_bin_0_1_2_outputs()}")
