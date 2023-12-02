from rlcard.games.briscola.card import BriscolaCard
from tkinter import *
import random
from tkinter import messagebox
import queue  
from rlcard.agents.human_agents.interfaccia import main_app
#from examples.human.briscola_human import main_app
import os


class HumanAgent(object):
    ''' A human agent for Briscola. It can be used to play against trained models.
    '''

    def __init__(self, num_actions):
        ''' Initialize the human agent

        Args:
            num_actions (int): The size of the output action space
        '''
        self.use_raw = True
        self.num_actions = num_actions
        #self.app_instance = main_app
 
        
    def step(self, state):
        app_instance = main_app

        print(state['raw_obs'])
        _print_state(state['raw_obs'], state['action_record'])

        while app_instance.button_pressed is None:
            # Wait for a button press
            app_instance.root.update()  # Ensure the GUI remains responsive

        action = app_instance.button_pressed
        app_instance.button_pressed = None  # Reset button_pressed for the next interaction

        return state['raw_legal_actions'][action]
    
    
        

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation. The same as step here.

        Args:
            state (numpy.array): A numpy array that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the human agent
        '''
        return self.step(state), {}



def _print_state(state, action_record):
    ''' Print out the state of a given player

    Args:
        player (int): Player id
    '''
    app_instance = main_app
    _action_list = []
    for i in range(1, len(action_record) + 1):
        if action_record[-i][0] == state['current_player']:
            break
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print('>> Player', pair[0], 'chooses ', end='')            
    #    app_instance.custom_message_box("Player 1",f"Other player chooses card {pair[1]}")
        
        
        str(BriscolaCard.print_cards_string(pair[1]))

        print('')

    print('\n=============== The Briscola ===============')
    #display briscola card
    '''
    card=state['briscola']
    # Resize Card
    briscola_image = app_instance.resize_cards(f'/home/noemi/Scrivania/RL/rlcard/agents/human_agents/images/cards/{card}.png')
    # Output Card To Screen
    briscola_label=app_instance.briscola_label
    briscola_label.config(image=briscola_image)
    '''
    BriscolaCard.print_cards_string(state['briscola'])
    
    print('\n=============== Your Hand ===============')
    
    '''
    cards=state['hand']
    player_label_1=app_instance.player_label_1
    player_label_2=app_instance.player_label_2
    player_label_3=app_instance.player_label_3
    # Resize Card
    card_image1 = app_instance.resize_cards(f'/home/noemi/Scrivania/RL/rlcard/agents/human_agents/images/cards/{cards[0]}.png')
    # Output Card To Screen
    player_label_1.config(image=card_image1)
    
    if(len(state['hand']))<2:
        player_label_2.config(image='')
    else:
        # Resize Card
        card_image2 = app_instance.resize_cards(f'/home/noemi/Scrivania/RL/rlcard/agents/human_agents/images/cards/{cards[1]}.png')
        # Output Card To Screen
        player_label_2.config(image=card_image2)
    
    if(len(state['hand']))<3:
        player_label_3.config(image='')
    else:
        # Resize Card
        card_image3 = app_instance.resize_cards(f'/home/noemi/Scrivania/RL/rlcard/agents/human_agents/images/cards/{cards[2]}.png')
        # Output Card To Screen
        player_label_3.config(image=card_image3)
    '''
    
    BriscolaCard.print_cards(state['hand'])
    print('')
    
    
    print('=============== Table Cards ===============')
    
    '''
    cards=state['played_cards']
    
    table_label=app_instance.table_label
    if(len(state['played_cards']))==1:
        # Resize Card
        table_image = app_instance.resize_cards(f'/home/noemi/Scrivania/RL/rlcard/agents/human_agents/images/cards/{cards[0]}.png')
        # Output Card To Screen
        table_label.config(image=table_image)
    else:   
        table_label.config(image='')
    '''
    
    
    
    BriscolaCard.print_cards(state['played_cards'])
    print('')
    #print('========== Players Card Number ===========')
    #for i in range(state['num_players']):
    #    if i != state['current_player']:
    #        print('Player {} has {} cards.'.format(i, state['num_cards'][i]))
    
    
    print('======== Actions You Can Choose =========')
    for i, action in enumerate(state['legal_actions']):
        print(str(i) + ': ', end='')
        str(BriscolaCard.print_cards_string(action))
        #if i < len(state['legal_actions']) - 1:
        #    print(', ', end='')
    print('\n')

        
    #main_app.run()

def _print_action(action):
    ''' Print out an action in a nice form

    Args:
        action (str): A string action
    '''
    BriscolaCard.print_cards(action)
    
   
