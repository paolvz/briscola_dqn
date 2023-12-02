class BriscolaCard:
    '''
    BriscolaCard stores the suit and rank of a single card

    Note:
        The suit variable in a standard card game should be one of [D, C, B, S] meaning [Denari, Coppe, Bastoni, Spade]
        Similarly the rank variable should be one of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    '''
    
    def __init__(self, suit, number):
        ''' Initialize the class of BriscolaCard

        Args:
            card_type (str): The type of card
            color (str): The color of card
            trait (str): The trait of card
        '''
        
        self.suit = suit
        self.number = number
        self.str = self.get_str()

        self.rank2score = {"1":11, "2":0, "3":10, "4":0, "5":0, "6":0, "7":0, "8":2, "9":3, "10":4}
        self.score = self.rank2score[self.number]

    def get_str(self):
        ''' Get the string representation of card

        Return:
            (str): The string of card's color and trait
        '''
        return self.suit + '-' + self.number

    @staticmethod
    def from_str(card_str):
        ''' Create a BriscolaCard object from a string representation

        Args:
            card_str (str): The string representation of the card, e.g., 'D-7'

        Returns:
            (BriscolaCard): The BriscolaCard object
        '''
        suit, number = card_str.split('-')
        return BriscolaCard(suit, number)
        
    
    def elegent_form(self):
        ''' Get an elegant form of a card string

        Args:
            card (string): A card string

        Returns:
            elegent_card (string): A nice form of the card
        '''
        suits = {'C': '🏺️', 'S': '🔪️', 'D': '🪙️', 'B': '🪵️'}
        return suits[self.suit] + self.number

    @staticmethod
    def print_cards(cards):
        ''' Nicely print a card or list of cards

        Args:
            cards (string or list): The card(s) to be printed
        '''
        if cards is None:
            cards = [None]
        if isinstance(cards, str):
            cards = [cards]

        lines = [[] for _ in range(9)]
        
        if isinstance(cards, BriscolaCard):
            elegent_card = cards.elegent_form()
            suit = elegent_card[0]
            number = elegent_card[1]
            if len(elegent_card) == 3:
                space = elegent_card[2]
            else:
                space = ' '

            lines[0].append('┌─────────┐')
            lines[1].append('│{}{}        │'.format(number, space))
            lines[2].append('│         │')
            lines[3].append('│         │')
            lines[4].append('│   {}    │'.format(suit))
            lines[5].append('│         │')
            lines[6].append('│         │')
            lines[7].append('│       {}{} │'.format(number, space))
            lines[8].append('└─────────┘')
        
       
        else:        
        
        
            for card in cards:
                if card is None:
                    lines[0].append('┌─────────┐')
                    lines[1].append('│░░░░░░░░░│')
                    lines[2].append('│░░░░░░░░░│')
                    lines[3].append('│░░░░░░░░░│')
                    lines[4].append('│░░░░░░░░░│')
                    lines[5].append('│░░░░░░░░░│')
                    lines[6].append('│░░░░░░░░░│')
                    lines[7].append('│░░░░░░░░░│')
                    lines[8].append('└─────────┘')
                else:
                    if isinstance(card, BriscolaCard):
                        elegent_card = card.elegent_form()
                    else:
                        card2=BriscolaCard.from_str(card)
                        elegent_card = card2.elegent_form()
                    suit = elegent_card[0]
                    number = elegent_card[1]
                    if len(elegent_card) == 3:
                        space = elegent_card[2]
                    else:
                        space = ' '

                    lines[0].append('┌─────────┐')
                    lines[1].append('│{}{}        │'.format(number, space))
                    lines[2].append('│         │')
                    lines[3].append('│         │')
                    lines[4].append('│   {}    │'.format(suit))
                    lines[5].append('│         │')
                    lines[6].append('│         │')
                    lines[7].append('│       {}{} │'.format(number, space))
                    lines[8].append('└─────────┘')
        for line in lines:
            print ('   '.join(line))
            
            
            
    @staticmethod
    def print_cards_string(cards):
        ''' Nicely print a card or list of cards

        Args:
            cards (string or list): The card(s) to be printed
        '''
        if cards is None:
            cards = [None]
        if isinstance(cards, str):
            cards = [cards]
        
        card_strings = [] 
        if isinstance(cards, BriscolaCard):
            elegent_card = cards.elegent_form()
            suit = elegent_card[0]
            number = elegent_card[1]
            if len(elegent_card) == 3:
                space = elegent_card[2]
            else:
                space = ' '   
            card_strings.append('{}{}{}'.format(number,space,suit))
            print('{}{}{}'.format(number,space,suit), end='')
        else:       
            for card in cards:
                if isinstance(card, BriscolaCard):
                    elegent_card = card.elegent_form()
                else:
                    card2=BriscolaCard.from_str(card)
                    elegent_card = card2.elegent_form()
                suit = elegent_card[0]
                number = elegent_card[1]
                if len(elegent_card) == 3:
                    space = elegent_card[2]
                else:
                    space = ' '
                card_strings.append('{}{}{}'.format(number,space,suit))
            print(', '.join(card_strings))

            


