from tkinter import *
import random
from tkinter import messagebox
import rlcard
from rlcard import models
from rlcard.agents.human_agents.briscola_human_agent import HumanAgent, _print_action
from rlcard.agents.human_agents.interfaccia import main_app
import os
import threading
import argparse

def play(args):
    app_instance = main_app


    ''' A toy example of playing against rule-based bot on Briscola
    '''

    # Make environment
    env = rlcard.make('briscola', config={'seed': args.seed})

    from rlcard.agents import DQNAgent, NFSPAgent

    import torch

    load_checkpoint_path  = args.checkpoint_path

    if load_checkpoint_path != "":
        dqn_agent = DQNAgent.from_checkpoint(checkpoint=torch.load(load_checkpoint_path))
        #nfsp_agent = NFSPAgent.from_checkpoint(checkpoint=torch.load(load_checkpoint_path))

    else:
        dqn_agent = models.load('briscola-rule-v1').agents[0]


    human_agent_1 = HumanAgent(env.num_actions)

    # dqn_agent = models.load('briscola-rule-v1').agents[0]
    env.set_agents([
        human_agent_1,
        #human_agent_2,
        dqn_agent,
        #nfsp_agent,
    ])

    print(">> briscola rule model V1")
    print(">> Start a new game")

    trajectories = [[] for _ in range(env.num_players)]
    state, player_id = env.reset()

    # Loop to play the game
    trajectories[player_id].append(state)

    #show briscola
    state1 = state['raw_obs']
    card=state1['briscola']
    # Resize Card
    briscola_image = app_instance.resize_cards(f'rlcard/agents/human_agents/images/cards/{card}.png')
    # Output Card To Screen
    briscola_label=app_instance.briscola_label
    briscola_label.config(image=briscola_image)

    #show hand
    cards=state1['hand']
    player_label_1=app_instance.player_label_1
    player_label_2=app_instance.player_label_2
    player_label_3=app_instance.player_label_3
    # Resize Card
    card_image1 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{cards[0]}.png')
    # Output Card To Screen
    player_label_1.config(image=card_image1)  
    if(len(state1['hand']))<2:
        player_label_2.config(image='')
    else:
        # Resize Card
        card_image2 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{cards[1]}.png')
        # Output Card To Screen
        player_label_2.config(image=card_image2)  
    if(len(state1['hand']))<3:
        player_label_3.config(image='')
    else:
        # Resize Card
        card_image3 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{cards[2]}.png')
        # Output Card To Screen
        player_label_3.config(image=card_image3)
        
    #show table cards
    cards=state1['played_cards']
    table_label=app_instance.table_label
    if(len(state1['played_cards']))==1:
        # Resize Card
        table_image = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{cards[0]}.png')
        # Output Card To Screen
        table_label.config(image=table_image)
    else:   
        table_label.config(image='')


    opponent_state=env.get_state(1)
    state1=opponent_state['raw_obs']
                
    #show hand
    if args.opp_hand_visible == "True":
        opponents_cards=state1['hand']
        opponent_label_1=app_instance.opponent_label_1
        opponent_label_2=app_instance.opponent_label_2
        opponent_label_3=app_instance.opponent_label_3
                
        # Resize Card
        if(len(state1['hand']))>0:
            #print(str(cards[0]))
            opponent_card_image1 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{opponents_cards[0]}.png')
        # Output Card To Screen
        opponent_label_1.config(image=opponent_card_image1)  
        if(len(state1['hand']))<2:
            opponent_label_2.config(image='')
        else:
            # Resize Card
            #print(str(cards[1]))
            opponent_card_image2 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{opponents_cards[1]}.png')
            # Output Card To Screen
            opponent_label_2.config(image=opponent_card_image2)  
        if(len(state1['hand']))<3:
            opponent_label_3.config(image='')
        else:
            # Resize Card
            #print(str(cards[2]))
            opponent_card_image3 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{opponents_cards[2]}.png')
            # Output Card To Screen
            opponent_label_3.config(image=opponent_card_image3)    
    else:
        app_instance.opponent_frame.destroy()

    prev_player_id= 0
    
    #print(env.get_remaining_cards())

        
    #show initial gui conditions
    while not env.is_over():
    
        remaining_cards=env.game.get_remaining_cards()
        app_instance.root.title(f'Deck cards left: {remaining_cards}')
        # Agent plays
        action, _ = env.agents[player_id].eval_step(state)
            
        if(action!= None):
        
        
        
        
            
            # Environment steps
            next_state, next_player_id = env.step(action, env.agents[player_id].use_raw)
            # Save action
            trajectories[player_id].append(action)

        
            card=state['action_record'][-1][1]
            if(player_id==0):
                #show table cards
                table_label=app_instance.table_label
                app_instance.table_image = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{card}.png')
                table_label.config(image=app_instance.table_image)
            else:  
                if(prev_player_id==0):
                    if((app_instance.table_label2.cget("image") == '') or (app_instance.table_label.cget("image") == '')):
                        #show table cards
                        table_label2=app_instance.table_label2
                        app_instance.table_image2 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{card}.png')
                        table_label2.config(image=app_instance.table_image2)
            
            
            #mostra action sul tavolo, mostra due carte del giocatore (state['hand']-action) per un po di tempo, poi aggiorna allo stato successivo
            
            def update_state(next_state, opp_hand_visible):

                app_instance.card0_button.config(state="normal")
                app_instance.card1_button.config(state="normal")
                app_instance.card2_button.config(state="normal")

                next_state1=next_state['raw_obs']
                #show briscola
                card = next_state1['briscola']
                # Resize Card
                app_instance.briscola_image = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{card}.png')
                # Output Card To Screen
                briscola_label=app_instance.briscola_label
                briscola_label.config(image=app_instance.briscola_image)
                #app_instance.root.update_idletasks()

                #show hand
                cards=next_state1['hand']
                player_label_1=app_instance.player_label_1
                player_label_2=app_instance.player_label_2
                player_label_3=app_instance.player_label_3
                # Resize Card
                if(len(cards))>0:
                    app_instance.player_image1 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{cards[0]}.png')
                    # Output Card To Screen
                    player_label_1.config(image=app_instance.player_image1) 
                    #app_instance.root.update_idletasks() 
                    if(len(next_state1['hand']))<2:
                        player_label_2.config(image='')
                        app_instance.card1_button.config(state="disabled")

                        #app_instance.root.update_idletasks()
                    else:
                        # Resize Card
                        app_instance.player_image2 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{cards[1]}.png')
                        # Output Card To Screen
                        player_label_2.config(image=app_instance.player_image2) 
                        #app_instance.root.update_idletasks() 
                    if(len(next_state1['hand']))<3:
                        player_label_3.config(image='')
                        app_instance.card2_button.config(state="disabled")

                        #app_instance.root.update()
                    else:
                        # Resize Card
                        app_instance.player_image3 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{cards[2]}.png')
                        # Output Card To Screen
                        player_label_3.config(image=app_instance.player_image3)
                        #app_instance.root.update_idletasks()
                else:
                    player_label_1.config(image='')
                    app_instance.card0_button.config(state="disabled")
                
                #show table cards
                cards=next_state1['played_cards']
                table_label=app_instance.table_label
                if(len(next_state1['played_cards']))==1:
                    # Resize Card
                    app_instance.table_image2 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{cards[0]}.png')
                    # Output Card To Screen
                    app_instance.table_label2.config(image=app_instance.table_image2)
                    table_label.config(image='')
                else:   
                    table_label.config(image='')
                    app_instance.table_label2.config(image='')
            
                
                opponent_state=env.get_state(1)
                state1=opponent_state['raw_obs']
                
                #show hand
                if opp_hand_visible == "True":
                    opponents_cards=state1['hand']
                    opponent_label_1=app_instance.opponent_label_1
                    opponent_label_2=app_instance.opponent_label_2
                    opponent_label_3=app_instance.opponent_label_3
                
                    # Resize Card
                    if(len(state1['hand']))>0:
                        app_instance.opponent_image1 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{opponents_cards[0]}.png')
                    # Output Card To Screen
                    opponent_label_1.config(image=app_instance.opponent_image1)  
                    if(len(state1['hand']))<2:
                        opponent_label_2.config(image='')
                    else:
                        # Resize Card
                        app_instance.opponent_image2 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{opponents_cards[1]}.png')
                        # Output Card To Screen
                        opponent_label_2.config(image=app_instance.opponent_image2)  
                    if(len(state1['hand']))<3:
                        opponent_label_3.config(image='')
                    else:
                        # Resize Card
                        app_instance.opponent_image3 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{opponents_cards[2]}.png')
                        # Output Card To Screen
                        opponent_label_3.config(image=app_instance.opponent_image3)
                else:
                    app_instance.opponent_frame.destroy()

            
            app_instance.card0_button.config(state="disabled")
            app_instance.card1_button.config(state="disabled")
            app_instance.card2_button.config(state="disabled")

            #app_instance.root.bind("<Return>", lambda event: on_enter_press(event, next_state))    
            app_instance.root.after(2000, lambda: update_state(next_state, args.opp_hand_visible))
        
                
            
            #update previous player
            prev_player_id=player_id   
            # Set the state and player
            state = next_state
            player_id = next_player_id

            # Save state.
            if not env.game.is_over():
                trajectories[player_id].append(state)

        #     Add a final state to all the players
        #    for player_id in range(self.num_players):
        #        state = self.get_state(player_id)
        #        trajectories[player_id].append(state)

        #    # Payoffs
        #    payoffs = self.get_payoffs()

        #    return trajectories, payoffs
        

    for player_id in range(env.num_players):
        state = env.get_state(player_id)
        trajectories[player_id].append(state)
    
    
    
    # If the human does not take the final action, we need to
    # print other players' actions
    final_state = trajectories[0][-1]
    action_record = final_state['action_record']
    state = final_state['raw_obs']
    _action_list = []
        
    print(action_record)
    #show table cards
    table_label=app_instance.table_label
    app_instance.table_image = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{action_record[-1][1]}.png')
    table_label.config(image=app_instance.table_image)

    #if((app_instance.table_label2.cget("image") == '') or (app_instance.table_label.cget("image") == '')):
    #show table cards
    table_label2=app_instance.table_label2
    app_instance.table_image2 = app_instance.resize_cards(f'./rlcard/agents/human_agents/images/cards/{action_record[-2][1]}.png')
    table_label2.config(image=app_instance.table_image2)
            
    import numpy as np
    payoffs = env.get_payoffs()

    #print("\n\npayoffs post conversion: ", _payoffs)

    print('===============     Result     ===============')
                    
    print(payoffs[0])
    points = payoffs[0][0]*60+60     

    points = env.game.players[0].score

    def win(points):
        app_instance.custom_message_box("Game over",f"You win! You scored {points} points")
        
    def lose(points):
        app_instance.custom_message_box("Game over",f"You lose! You scored {points} points")
        
    if points > 60:
        app_instance.root.after(3000, lambda: win(points))
        print('You win!, you scored: ',points, " points")
    else:
        app_instance.root.after(3000, lambda: lose(points))
        print('You lose!, you scored: ', points, " points")




    app_instance.run()

#root.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("DQN/NFSP example in RLCard")
    
    parser.add_argument(
         "--checkpoint_path",
            type=str,
            default=""
    )

    parser.add_argument(
         "--opp_hand_visible",
            type=str,
            default="False",
            choices=["True", "False"]
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=0,
        help='Random seed'
    )

    args = parser.parse_args()

    play(args)  
