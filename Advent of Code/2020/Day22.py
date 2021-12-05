from aocscrapper import get_AoC_input

if __name__ == '__main__':
    player0_deck, player1_deck = [x.split('\n', maxsplit=1)[1] for x in get_AoC_input(2020, 22, get_test=False).strip().split('\n\n')]
    player0_start_deck = list(map(int, player0_deck.split('\n')))
    player1_start_deck = list(map(int, player1_deck.split('\n')))

    def play_game(deck_a, deck_b, part2):
        deck_a = list(deck_a)
        deck_b = list(deck_b)
        a_states = set()
        b_states = set()

        while len(deck_a) > 0 and len(deck_b) > 0:
            if part2 and tuple(deck_a) in a_states and tuple(deck_b) in b_states:
                return 0, deck_a, deck_b

            a_states.add(tuple(deck_a))
            b_states.add(tuple(deck_b))

            player0_turn = deck_a.pop(0)
            player1_turn = deck_b.pop(0)

            if part2 and player0_turn <= len(deck_a) and player1_turn <= len(deck_b):
                round_winner, _, _ = play_game(deck_a[:player0_turn], deck_b[:player1_turn], part2)
            else:
                round_winner = int(player0_turn < player1_turn)  # True (1) if player1's card greater

            if round_winner == 0:
                deck_a += [player0_turn, player1_turn]
            else:
                deck_b += [player1_turn, player0_turn]

        return int(len(deck_a) == 0), deck_a, deck_b  # len(deck_a) == 0 True (1) if player0's deck is empty

    def score_game(deck):
        score = 0
        for i in range(1, len(deck)+1):
            score += deck.pop() * i
        return score

    winning_player, player0_deck, player1_deck = play_game(player0_start_deck, player1_start_deck, part2=False)
    print('Part 1:', score_game([player0_deck, player1_deck][winning_player]))

    winning_player, player0_deck, player1_deck = play_game(player0_start_deck, player1_start_deck, part2=True)
    print('Part 2:', score_game([player0_deck, player1_deck][winning_player]))
