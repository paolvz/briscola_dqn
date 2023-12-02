from rlcard.games.briscola.utils import init_italian_deck
import numpy as np

class BriscolaDealer:

    def __init__(self, np_random):
        ''' Initialize a Brisola dealer class
        '''
        self.np_random = np_random
        self.deck = init_italian_deck()
        self.shuffle()
        self.status = 'alive'
        self.score = 0

    def shuffle(self):
        ''' Shuffle the deck
        '''
        shuffle_deck = np.array(self.deck)
        self.np_random.shuffle(shuffle_deck)
        self.deck = list(shuffle_deck)

    def deal_card(self, player):
        ''' Distribute one card to the player

        Args:
            player_id (int): the target player's id
        '''
        #idx = self.np_random.choice(len(self.deck))
        card = self.deck[0]
        self.deck.pop(0)
        player.hand.append(card)
    
    def set_briscola(self):
        ''' Set the briscola card
        '''
        idx = self.np_random.choice(len(self.deck))
        card = self.deck[idx]
        self.deck.pop(idx)

        # place the briscola card at the bottom of the deck
        self.deck.append(card)

        return card