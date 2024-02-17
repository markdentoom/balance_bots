import re


class Instructions:
    def __init__(self, file_path):
        self.file_path = file_path

    def input_lines(self):
        with open(self.file_path) as file_content:
            return file_content.read().splitlines()

    @staticmethod
    def get_ints_from_line(line: str) -> list[int]:
        return [int(v) for v in re.findall(r"\d+", line)]

    def initial_bot_values(self) -> dict[int, list[int]]:
        """
        Example output: {119: [61], 2: [11, 17]}
        This means bot 119 starts with microchip value 61
        and that bot 2 start with microchip values 11 and 17.
        """
        initial_bot_values = {}

        for line in self.input_lines():
            if not line.startswith("value"):
                continue

            value, bot = self.get_ints_from_line(line)
            initial_bot_values.setdefault(bot, []).append(value)

        return initial_bot_values

    def bot_instructions(self) -> dict[int, tuple[tuple[str, int], tuple[str, int]]]:
        """
        Example output: {119: (('bot', 18), ('bot', 3)), 69: (('output', 47), ('bot', 172))}
        This means bot 119 gives low values to bot 18 and high values to bot 3
        and that bot 69 gives low values to output 47 and high values to bot 172.
        """
        bot_instructions = {}

        for line in self.input_lines():
            if not line.startswith("bot"):
                continue

            bot, gives_low_to, gives_high_to = self.get_ints_from_line(line)
            recipient1, recipient2 = re.findall(r" (bot|output)", line)
            bot_instructions[bot] = (recipient1, gives_low_to), (recipient2, gives_high_to)

        return bot_instructions


input_file_instructions = Instructions("input.txt")
bots = input_file_instructions.initial_bot_values()
instructions = input_file_instructions.bot_instructions()


output = {}
# {17: [2], 4: [3],
# output 17 contains microchips [2], output 4 contains microchips [3]
while bots:
    for bot, microchips in dict(bots).items():
        if len(microchips) != 2:
            continue

        bot_instructions = bots.pop(bot)
        microchip1, microchip2 = sorted(bot_instructions)
        if microchip1 == 17 and microchip2 == 61:
            print(
                f"Bot {bot} is responsible for comparing value-61 microchips with value-17 microchips"
            )

        (recipient1, gives_low_to), (recipient2, gives_high_to) = instructions[bot]
        type1 = bots if recipient1 == "bot" else output
        type2 = bots if recipient2 == "bot" else output
        type1.setdefault(gives_low_to, []).append(microchip1)
        type2.setdefault(gives_high_to, []).append(microchip2)

microchip1 = output[0][0]
microchip2 = output[1][0]
microchip3 = output[2][0]
result = microchip1 * microchip2 * microchip3
print(
    f"You get {result} if you multiply together the values of one chip in each of outputs 0, 1, and 2"
)

# Answers are 73 and 3965
