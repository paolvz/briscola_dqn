from copy import deepcopy
import numpy as np

from rlcard.games.briscola import Dealer
from rlcard.games.briscola import Player
from rlcard.games.briscola import Judger
from rlcard.games.briscola import Round

from rlcard.games.briscola.utils import cards2list


class BriscolaGame:

    def __init__(self, allow_step_back=False, num_players=2):
        ''' Initialize the class Brisola Game
        '''
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()

        if(num_players != 2 and num_players != 4):
            raise ValueError('Only 2 or 4 players are supported')
            
        self.num_players = num_players
        
        self.briscola = None

        #self.played_cards = []
        self.winners = []
             
        self.rank2score = {"1":11, "2":0, "3":10, "4":0, "5":0, "6":0, "7":0, "8":2, "9":3, "10":4}
        
        
        self.allow_step_back = allow_step_back

    def init_game(self):
        ''' Initialilze the game

        Returns:
            state (dict): the first state of the game
            player_id (int): current player's id
        '''
        
        # Initialize a dealer that can deal cards
        self.dealer = Dealer(self.np_random)
        
        self.briscola = self.dealer.set_briscola()

        #print("BRISCOLA: ", self.briscola.suit)

        # Initialize two/four players to play the game
        self.players = []
        for i in range(self.num_players):
            self.players.append(Player(i, self.np_random))

        self.judger = Judger(self.np_random)


        #modificato
        self.round_payoffs=[[] for player in self.players]
        #fine modificato
        
        
        # Deal 3 cards to each player to prepare for the game
        for i in range(3):
            for j in range(self.num_players):
                self.dealer.deal_card(self.players[j])


        # Initialize a Round
        self.round = Round(self.dealer, self.num_players, self.np_random)

        # Save the hisory for stepping back to the last state.
        self.history = []


        player_id = self.round.current_player
        state = self.get_state(player_id)
        
        
        return state, player_id
    
    def step(self, action):
        ''' Get the next state

        Args:
            action (str): A specific action

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        '''
        #self.played_cards = self.played_cards + self.round.played_cards


        if self.allow_step_back:
            # First snapshot the current state
            his_dealer = deepcopy(self.dealer)
            his_round = deepcopy(self.round)
            his_players = deepcopy(self.players)
            self.history.append((his_dealer, his_players, his_round))


        # se è finito un turno ma non la partita, inizializzo un nuovo turno
        self.round.proceed_round(self.players, action)
        
        if not self.round.is_over:
            player_id = self.round.current_player
            state = self.get_state(player_id)
        else:
            winner, points = self.judger.judge_round(self.round, self.players, self.briscola)   
            round_payoff : float = points/22  
            self.round_payoffs[winner].append(round_payoff)
            self.round_payoffs[1-winner].append(-round_payoff)
            
            state, player_id = self.set_new_round(winner)
        
        return state, player_id
    
    def step_back(self):
        ''' Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        if not self.history:
            return False
        self.dealer, self.players, self.round = self.history.pop()
        return True

    def set_new_round(self, winner):
        ''' Set a new round
        '''
        # winner of previous round starts the new round
        # winner, _ = self.judger.judge_round(self.round, self.players, self.briscola)
        self.players[winner].prese = self.players[winner].prese + self.round.played_cards

        self.winners.append(winner)

        if self.round.round_number == 40/self.num_players-1:
            return self.get_state(winner), winner
        
        # initialize a new round
        self.round.round_number = self.round.round_number + 1
        self.round.is_over = False
        self.round.current_player = winner
        self.round.played_cards = []

        # deal one card each, starting from the winner
        # così il winner persca per primo (serve solo all'ultimo round, la briscola finale va all'ultimo)
        if(not self.dealer.deck==[]):    
            if self.num_players == 2:
                for i in [winner, 1-winner]:
                    self.dealer.deal_card(self.players[i])
            else: 
                for i in [winner, (winner+1)%4,(winner+2)%4,(winner+3)%4]:
                    self.dealer.deal_card(self.players[i])


        state = self.get_state(winner)
        
        return state, winner

    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        state = self.round.get_state(self.players, player_id)
        state['briscola'] = self.briscola.str
        state['game_played_cards'] = [cards2list(player.prese) for player in self.players]
        state['num_players'] = self.num_players
        
        return state

    def get_payoffs(self):
        ''' Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        
        # payoffs punteggio finale 
        # payoffs = [(player.score-60) for player in self.players]
        
        # payoffs come da ultimo turno
        payoffs = [self.round_payoffs[0][-1],self.round_payoffs[1][-1]]

        # +-1
        # payoffs = 
        
        # round payoffs
        round_payoffs = self.round_payoffs


        return payoffs, round_payoffs
        #return payoffs
        #return round_payoffs, []
        
    #modificato   
    def get_round_payoffs(self):
        ''' Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
       
        return self.round_payoffs
    #fine modificato  
        
        
        

    def get_legal_actions(self):
        ''' Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        '''

        return self.round.get_legal_actions(self.players, self.round.current_player)

    def get_num_players(self):
        ''' Return the number of players in Limit Texas Hold'em

        Returns:
            (int): The number of players in the game
        '''
        return self.num_players

   # @staticmethod
    def get_num_actions(self):
        ''' Return the number of applicable actions

        Returns:
            (int): The number of actions. number of actions = cards in the hand of the player
        '''
        return 40 #self.players[self.round.current_player].hand.length()

    def get_player_id(self):
        ''' Return the current player's id

        Returns:
            (int): current player's id
        '''
        return self.round.current_player

    def is_over(self):
        ''' Check if the game is over

        Returns:
            (boolean): True if the game is over
        '''
        if(len(self.dealer.deck)==0 and self.round.is_over):
            return True
        
        return  False
        
    def get_remaining_cards(self):
        return len(self.dealer.deck)
