import re


with open("input.txt") as input_file:
    input_lines = input_file.read().splitlines()

bots = {}
instructions = {}
for line in input_lines:
    line_numbers = [int(v) for v in re.findall(r"\d+", line)]
    if line.startswith("bot"):
        bot, gives_low_to, gives_high_to = line_numbers
        recipient1, recipient2 = re.findall(r" (bot|output)", line)
        instructions[bot] = (recipient1, gives_low_to), (recipient2, gives_high_to)
    if line.startswith("value"):
        microchip, bot = line_numbers
        bots.setdefault(bot, []).append(microchip)


output = {}
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
