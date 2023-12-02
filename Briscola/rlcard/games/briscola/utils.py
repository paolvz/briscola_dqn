import os
import json
import numpy as np
from collections import OrderedDict

import rlcard

from rlcard.games.briscola.card import BriscolaCard as Card

# Read required docs
ROOT_PATH = rlcard.__path__[0]

# a map of abstract action to its index and a list of abstract action
with open(os.path.join(ROOT_PATH, 'games/briscola/jsondata/action_space.json'), 'r') as file:
    ACTION_SPACE = json.load(file, object_pairs_hook=OrderedDict)
    ACTION_LIST = list(ACTION_SPACE.keys())

# a map of color to its index
COLOR_MAP = {'D': 0, 'S': 1, 'B': 2, 'C': 3}

# a map of trait to its index
TRAIT_MAP = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
             '8': 8, '9': 9, '10':10}

def init_italian_deck():
    ''' Initialize a standard deck of 40 cards

    Returns:
        (list): A list of Card object
    '''
    suit_list = ['D', 'C', 'S', 'B']
    rank_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    res = [Card(suit, rank) for suit in suit_list for rank in rank_list]
    return res


def cards2list(cards):
    ''' Get the corresponding string representation of cards

    Args:
        cards (list): list of UnoCards objects

    Returns:
        (string): string representation of cards
    '''
    cards_list = []
    for card in cards:
        cards_list.append(card.get_str())
    return cards_list

def hand2dict(hand):
    ''' Get the corresponding dict representation of hand

    Args:
        hand (list): list of string of hand's card

    Returns:
        (dict): dict of hand
    '''
    hand_dict = {}
    for card in hand:
        if card not in hand_dict:
            hand_dict[card] = 1

    return hand_dict

def encode_cards(plane, hand):
    ''' Encode hand and represerve it into plane

    Args:
        plane (array): 3*4*15 numpy array
        hand (list): list of string of hand's card

    Returns:
        (array): 4*10 numpy array
    '''
    hand = hand2dict(hand)
    for card, _ in hand.items():
        card_info = card.split('-')
        suit = COLOR_MAP[card_info[0]]
        number = TRAIT_MAP[card_info[1]]

        plane[suit][number-1] = 1

    return plane

def encode_target(plane, target):
    ''' Encode target and represerve it into plane

    Args:
        plane (array): 1*4*15 numpy array
        target(str): string of target card

    Returns:
        (array): 1*4*15 numpy array
    '''
    target_info = target.split('-')
    color = COLOR_MAP[target_info[0]]
    trait = TRAIT_MAP[target_info[1]]
    plane[color][trait] = 1
    return plane
