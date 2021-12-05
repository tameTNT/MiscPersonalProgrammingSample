from collections import deque


def play_game(number_of_players, number_of_marbles):
    marbles = deque([0])
    number_of_players, number_of_marbles = number_of_players, number_of_marbles
    current_player = 0
    player_scores = {player_number: 0 for player_number in [i for i in range(number_of_players)]}

    for marble in range(1, number_of_marbles + 1):
        if marble % 23 == 0:
            player_scores[current_player] += marble
            marbles.rotate(7)  # "the marble 7 marbles counter-clockwise from the current marble is removed"
            player_scores[current_player] += marbles.pop()
            marbles.rotate(-1)  # "marble located immediately clockwise of the marble that was removed becomes the new current marble"
        else:
            marbles.rotate(-1)
            marbles.append(marble)

        current_player = (current_player + 1) % number_of_players

    return max(player_scores.values())


print("Part 1: ", play_game(418, 71339))  # Puzzle input
print("Part 2: ", play_game(418, 7133900))  # Puzzle input
