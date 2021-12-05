def make_hot_chocolate(input_number, part):

    elf_one_position = 0
    elf_two_position = 1

    if part == 1:
        scoreboard = [3, 7]
        while len(scoreboard) < input_number + 10:
            elf_one_current_recipe = scoreboard[elf_one_position]
            elf_two_current_recipe = scoreboard[elf_two_position]

            sum_of_current_recipes = elf_one_current_recipe + elf_two_current_recipe

            scoreboard.append(int(str(sum_of_current_recipes)[0]))

            if len(str(sum_of_current_recipes)) == 2:
                scoreboard.append(int(str(sum_of_current_recipes)[-1]))

            elf_one_position = (elf_one_position + 1 + elf_one_current_recipe) % len(scoreboard)
            elf_two_position = (elf_two_position + 1 + elf_two_current_recipe) % len(scoreboard)

        return "".join([str(number) for number in scoreboard[-10:]])

    elif part == 2:
        scoreboard = "37"  # Scoreboard as a string for part 2 as buffer is easier and no need to use join method on list every time (which is very memory intensive and time consuming)
        buffer = str()
        stringed_input = str(input_number)

        while stringed_input not in buffer:
            elf_one_current_recipe = int(scoreboard[elf_one_position])
            elf_two_current_recipe = int(scoreboard[elf_two_position])

            sum_of_current_recipes = str(elf_one_current_recipe + elf_two_current_recipe)

            scoreboard += sum_of_current_recipes[0]

            if len(sum_of_current_recipes) == 2:
                scoreboard += sum_of_current_recipes[-1]

            scoreboard_length = len(scoreboard)
            elf_one_position = (elf_one_position + 1 + elf_one_current_recipe) % scoreboard_length
            elf_two_position = (elf_two_position + 1 + elf_two_current_recipe) % scoreboard_length

            try:
                buffer = scoreboard[-10:]  # A buffer of the last 10 values in the scoreboard is needed so that program is actually complete in a reasonable time (i.e. 1 minute as opposed to 20 minutes)
            except IndexError:
                continue

        return len(scoreboard.split(stringed_input)[0])


print("Part 1: ", make_hot_chocolate(323081, 1))  # Puzzle input
print("Part 2: ", make_hot_chocolate(323081, 2))  # Puzzle input
