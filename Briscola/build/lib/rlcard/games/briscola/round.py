from rlcard.games.briscola.card import BriscolaCard
from rlcard.games.briscola.utils import cards2list
import numpy as np

class BriscolaRound:

    def __init__(self, dealer, num_players, np_random, round_number=0):
        ''' Initialize the round class

        Args:
            dealer (object): the object of UnoDealer
            num_players (int): the number of players in game
        '''
        self.np_random = np_random
        self.dealer = dealer
        #self.current_player = np.random.randint(num_players)
        self.current_player = 0
        self.num_players = num_players
        self.played_cards = []
        self.round_number = round_number
        self.is_over = False
        self.winner = None


    def proceed_round(self, players, action):
        ''' Call other Classes' functions to keep one round running

        Args:
            player (object): object of UnoPlayer
            action (str): string of legal action
        '''        
        player = players[self.current_player]
        card_info = action.split('-')
        suit = card_info[0]
        number = card_info[1]
        
        # remove card corresponding to the input action
        remove_index = None
        for index, card in enumerate(player.hand):
            if suit == card.suit and number == card.number:
                remove_index = index
                break
        
        #print("giocatore = ", self.current_player, "\n")
        #print("mano giocatore = ", [card.str for card in player.hand], "\n")
        #print("azione = ", action)
        #print("indice da rimuovere = ", remove_index, "\n")
        card = player.hand.pop(remove_index)
        
                
        self.played_cards.append(card)
        self.current_player = (self.current_player + 1) % self.num_players
        
        # se le carte sul tavolo sono quante i giocatori, il turno è finito
        if len(self.played_cards) == self.num_players:
            self.is_over= True

    
    def get_legal_actions(self, players, player_id):
        
        player = players[player_id]
        
        legal_actions = [card.str for card in player.hand]

        return legal_actions
    
    def get_state(self, players, player_id):
        ''' Get player's state

        Args:
            players (list): The list of BriscolaPlayer
            player_id (int): The id of the player
        '''
        state = {}
        player = players[player_id]
        state['hand'] = cards2list(player.hand)
        #state['hand'] = player.hand

        # carte sul tavolo
        state['played_cards'] = cards2list(self.played_cards)
        state['legal_actions'] = self.get_legal_actions(players, player_id)

        state['current_player'] = self.current_player
                
        return state
    
