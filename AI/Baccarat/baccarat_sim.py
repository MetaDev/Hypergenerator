import sys
import os
import copy
import random
from collections import Counter
from collections import OrderedDict


def bacc_score(rank):
    if rank == 'Jack' or rank == 'Queen' or rank == 'King':
        return 0
    else:
        return int(rank)


suite_map = {
    0: 'Clubs',
    1: 'Diamonds',
    2: 'Hearts',
    3: 'Spades'
}
rank_map = {
    0: 'Ace',
    1: '2',
    2: '3',
    3: '4',
    4: '5',
    5: '6',
    6: '7',
    7: '8',
    8: '9',
    9: '10',
    10: 'Jack',
    11: 'Queen',
    12: 'King'

}


def build_deck():
    deck = []
    for suite in suite_map.keys():
        for rank in rank_map.keys():
            deck.append([rank, suite, bacc_score(rank)])
    return deck


def generate_deck(n=1):
    decks = build_deck() * n
    random.shuffle(decks)
    return decks


def take_card(decks, count):
    rank, suite, score = decks.pop()
    count.append(rank)
    return score


def simulate_game(decks):
    card_count = []
    player = [take_card(decks, card_count)]
    bank = [take_card(decks, card_count)]
    player.append(take_card(decks, card_count))
    bank.append(take_card(decks, card_count))

    player_score = sum(player) % 10
    bank_score = sum(bank) % 10
    if player_score >= 8 or bank_score >= 8:
        return end_game(player, bank), cards_to_occurrences(card_count)

    # player draws 3rd card
    if player_score <= 5:
        pcard = take_card(decks, card_count)
        player.append(pcard)
        # bank rules
        if pcard in (2, 3) and bank_score <= 4:
            bank.append(take_card(decks, card_count))
        elif pcard in (4, 5) and bank_score <= 5:
            bank.append(take_card(decks, card_count))
        elif pcard in (6, 7) and bank_score <= 6:
            bank.append(take_card(decks, card_count))
        elif pcard == 8 and bank_score <= 2:
            bank.append(take_card(decks, card_count))
        elif pcard in (1, 9, 0) and bank_score <= 3:
            bank.append(take_card(decks, card_count))
    elif bank_score <= 5:
        bank.append(take_card(decks, card_count))
    return end_game(player, bank), cards_to_occurrences(card_count)


win_map = {
    -1: "bank",
    0: "tie",
    1: "player"
}
#bet win payout
payout_map = {
    (-1,-1):0.95,
    (-1,1):-1,
    (-1,0): 0,
    (1,-1):-1,
    (1,1):1,
    (1,0):0,
    (0,-1):-1,
    (0,1):-1,
    (0,0):8
}
def end_game(player, bank):
    player_score = sum(player) % 10
    bank_score = sum(bank) % 10
    if player_score == bank_score:
        return 0
    elif player_score > bank_score:
        return 1
    return -1


def cards_to_occurrences(cards):
    return OrderedDict(sorted(Counter(cards).items(), key=lambda t: t[0]))


def generate_games(n_games, n_decks):
    results = [];
    for i in range(n_games):
        decks = generate_deck(n_decks)
        while len(decks) > 10:
            result = simulate_game(decks)
            results.append(result)
    return results
