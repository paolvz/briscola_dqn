
class BriscolaPlayer:

    def __init__(self, player_id, np_random):
        ''' Initialize a Briscola player class

        Args:
            player_id (int): id for the player
        '''
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []
        self.prese = []
        self.score = 0

    def get_player_id(self):
        ''' Return player's id
        '''
        return self.player_id
    
    def play_card(self, card):
        ''' Play a card
        '''

        self.hand.remove(card)
        return
    
    def incrementPoints(self, points):
        self.score += points



""""
    def get_state(self, public_cards, all_chips, legal_actions):
        
        #Encode the state for the player
#
        #Args:
        #    public_cards (list): A list of public cards that seen by all the players
#
        #Returns:
        #    (dict): The state of the player
        
        return {
            'hand': [c.get_index() for c in self.hand],
            'public_cards': [c.get_index() for c in public_cards],
            'legal_actions': legal_actions
        }

"""