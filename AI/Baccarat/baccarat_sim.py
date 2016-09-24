import sys
import os
import copy
import random


def bacc_score(rank):
    if rank == 'Jack' or rank == 'Queen' or rank == 'King':
        return 0
    else:
        return int(rank)

def build_deck():
    deck = []
    for suite in ['Clubs', 'Diamonds', 'Hearts', 'Spades']:
        for rank in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']:
            deck.append([rank, suite, bacc_score(rank)])
    return deck




def generate_deck(n=1):
    decks = build_deck() * n
    random.shuffle(decks)
    return decks
def take_card(decks,count):
    rank, suit, score = decks.pop()
    count.append([rank,suit])
    return score


def simulate_game(decks):
    card_count=[]
    player = [take_card(decks,card_count)]
    bank = [take_card(decks,card_count)]
    player.append(take_card(decks,card_count))
    bank.append(take_card(decks,card_count))

    player_score = sum(player) % 10
    bank_score = sum(bank) % 10
    if player_score >= 8 or bank_score >= 8:
        return end_game(player,bank,card_count)

    # player draws 3rd card
    if player_score <= 5:
        pcard = take_card(decks,card_count)
        player.append(pcard)
        # bank rules
        if pcard in (2,3) and bank_score <= 4:
            bank.append(take_card(decks,card_count))
        elif pcard in (4,5) and bank_score <= 5:
            bank.append(take_card(decks,card_count))
        elif pcard in (6,7) and bank_score <= 6:
            bank.append(take_card(decks,card_count))
        elif pcard == 8 and bank_score <= 2:
            bank.append(take_card(decks,card_count))
        elif pcard in (1,9,0) and bank_score <= 3:
            bank.append(take_card(decks,card_count))
    elif bank_score <= 5:
        bank.append(take_card(decks,card_count))
    return end_game(player,bank,card_count)


def end_game(player,bank,count):
    player_score = sum(player) % 10
    bank_score = sum(bank) % 10
    if player_score == bank_score:
        return "tie",count
    elif player_score > bank_score:
        return "player",count
    return "bank",count


def generate_games(n_games,n_decks=8,min_deck_size=10):
    results = [];
    for i in range(n_games):
        decks = generate_deck(n_decks)
        while len(decks) > min_deck_size:
            result = simulate_game(decks)
            results.append(result)
    return results


