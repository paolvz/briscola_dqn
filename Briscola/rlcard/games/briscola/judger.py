
class BriscolaJudger:
    def __init__(self, np_random):
        ''' Initialize a Briscola judger class
        '''
        self.np_random = np_random
        self.rank2score = {"1":11, "2":0, "3":10, "4":0, "5":0, "6":0, "7":0, "8":2, "9":3, "10":4}

    def judge_round(self, round, players, briscola):
        ''' Judge the target player's status

        Args:
            player (int): target player's id

        Returns:
            status (str): the status of the target player
            score (int): the current score of the player
        '''
        turn_points = 0
        tmp_winner = 0
        
        # poiché il round è finito il current player è proprio
        # il giocatore che ha iniziato il turno
        start_player = round.current_player
    
        # iterate through cards
        for i, card in enumerate(round.played_cards):

            if i == 0:
                high_card = card
                tmp_winner = 0
            else:
                if card.suit == briscola.suit:
                    if high_card.suit == briscola.suit:
                        if card.score > high_card.score:
                            high_card = card
                            tmp_winner = i
                        else:
                            if card.score == high_card.score:
                                if card.number > high_card.number:
                                    high_card = card
                                    tmp_winner = i
                    else:
                        high_card = card
                        tmp_winner = i
                else:
                    if card.suit == high_card.suit:
                        if card.score > high_card.score:
                            high_card = card
                            tmp_winner = i
                        else:
                            if card.score == high_card.score:
                                if card.number > high_card.number:
                                    high_card = card
                                    tmp_winner = i
            turn_points += card.score

        winner = (start_player + tmp_winner) % round.num_players
        players[winner].incrementPoints(turn_points)
        #print("punti mano: ", turn_points, "al giocatore: ", winner, "\n")
        return winner, turn_points

    def judge_game(self, game):
        ''' Judge the winner of the game

        Args:
            game (class): target game class
        '''
        '''
                '''
        winner = max(game.players, key=lambda x:x.score)
        points = winner.score

        return winner, points

    def judge_score(self, cards):
        ''' Judge the score of a given cards set

        Args:
            cards (list): a list of cards

        Returns:
            score (int): the score of the given cards set
        '''
        score = 0
        for card in cards:
            card_score = self.rank2score[card.number]
            score += card_score

        return score
