''' An example of training a reinforcement learning agent on the environments in RLCard
'''
import os
import argparse

import torch

import rlcard
from rlcard.agents import RandomAgent
from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
    tournament3,
    reorganize,
    reorganize2,
    Logger,
    plot_curve,
)

from tqdm import tqdm
from tqdm.auto import trange

from rlcard.agents import DQNAgent, NFSPAgent
from copy import deepcopy

def get_opponent(env, args, device):

    if args.against_pretrained == "True":
        agent = DQNAgent(
            num_actions=env.num_actions,
            state_shape=env.state_shape[0],
            mlp_layers=[64,64],
            device=device,
            save_path=args.log_dir,
            save_every=args.save_every
        )

        dirs = os.listdir(args.load)
        path = args.load + "/" + dirs[-1] if len(dirs) > 0 else None

        agent = agent.from_checkpoint(checkpoint=torch.load(path))

        print("playing against pretrained: ", path, "\n\n")

        return agent

    else:
        return RandomAgent(num_actions=env.num_actions)
    
def train(args):


    info = [f'algorithm: {args.algorithm}', 
            f'num_episodes: {args.num_episodes}',
            f'evaluate_every (evaluation against randomplayer): {args.evaluate_every}',
            f'num_eval_games: {args.num_eval_games}',
            f'save_every (checkpoints): {args.save_every}',
            f'round_payoff: {args.round_payoff}',
            f'switch_every (opponent update): {args.switch_every}',
            f'log_dir: {args.log_dir}',
            f'load_checkpoint_path: {args.load_checkpoint_path}',
            f'seed: {args.seed}'
        ]

    with Logger(args.log_dir) as logger:
         logger.log_info(info)
         

    # Check whether gpu is available
    #device = get_device()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)  
    # Seed numpy, torch, random
    set_seed(args.seed)

    # conversione di steps in partite
    # in questo modo save every 100 significa che salvo ogni 100 partite e 2000 steps
    args.save_every = args.save_every*20

    #  Make the environment with seed
    env = rlcard.make(
        args.env,
        config={
            'seed': args.seed,
        }
    )

    # Initialize the agent and use random agents as opponents
 
        
        
    if args.algorithm == 'dqn':
            agent = DQNAgent(
                num_actions=env.num_actions,
                state_shape=env.state_shape[0],
                mlp_layers=[64,64],
                device=device,
                save_path=args.log_dir,
                save_every=args.save_every
            )
            
    elif args.algorithm == 'nfsp':
            
            agent = NFSPAgent(
                num_actions=env.num_actions,
                state_shape=env.state_shape[0],
                hidden_layers_sizes=[64,64],
                q_mlp_layers=[64,64],
                device=device,
                save_path=args.log_dir,
                save_every=args.save_every
            )
            
        
    if args.load_checkpoint_path != "":
            dirs = os.listdir(args.load_checkpoint_path)
            
            dirs = [d for d in dirs if d.startswith("checkpoint")]
            if dirs != []:
                
               dirs = sorted(dirs, key=lambda x: int(x.split("-")[1].split(".")[0]))
               path = args.load_checkpoint_path + "/" + dirs[-1] if len(dirs) > 0 else None
            
               agent = agent.from_checkpoint(checkpoint=torch.load(path))
               agent.save_every = args.save_every
               agent.save_path = args.log_dir

    agents = [agent]    

    opponent = get_opponent(env, args, device)

    if args.algorithm == 'nfsp':
        for _ in range(1, env.num_players):
            #agents.append(RandomAgent(num_actions=env.num_actions))
            agents.append(agent)
    else:
        for _ in range(1, env.num_players):
            agents.append(opponent)
        
    env.set_agents(agents)

    eval_agents = [agent,RandomAgent(num_actions=env.num_actions)]


    start_episode = agent.train_t / 20
    # Start training
    with Logger(args.log_dir) as logger:
        for episode in trange(args.num_episodes):
            if episode < start_episode:
                continue
            
            if args.algorithm == 'nfsp':
                agents[0].sample_episode_policy()

            # Generate data from the environment
            # payoffs: tuple (list of game payoffs, [player0's round_payoff, player1's round_payoff])
            trajectories, payoffs = env.run(is_training=True)

            # Reorganaize the data to be state, action, reward, next_state, done
            if args.round_payoff == "True":
                trajectories = reorganize2(trajectories, payoffs)
            else:
                if args.env == "briscola":
                    payoffs = payoffs[0]
                trajectories = reorganize(trajectories, payoffs)
            
            #print("new_trajectories[player = 0]: ", trajectories[0])
            #print("payoffs: ", payoffs[0], len(payoffs[0]))

            # Feed transitions into agent memory, and train the agent
            # Here, we assume that DQN always plays the first position
            for ts in trajectories[0]:
                agent.feed(ts)


#            if args.algorithm == "dqn" and episode % args.switch_every == 0 and episode > 0:
#                
#                old_agent = DQNAgent(
#                    num_actions=env.num_actions,
#                    state_shape=env.state_shape[0],
#                    mlp_layers=[64,64],
#                    device=device,
#                    save_path=args.log_dir,
#                    save_every=args.save_every
#                )
#
#                dirs = os.listdir(args.load_checkpoint_path)
#            
#                dirs = [d for d in dirs if d.startswith("checkpoint")]
#                if dirs != []:
#
#                    dirs = sorted(dirs, key=lambda x: int(x.split("-")[1].split(".")[0]))
#                    path = args.load_checkpoint_path + "/" + dirs[-1] if len(dirs) > 0 else None
#
#                    old_agent = old_agent.from_checkpoint(checkpoint=torch.load(path))
#                    old_agent.save_every = args.save_every
#                    old_agent.save_path = args.log_dir
#
#                    agents = [agent,old_agent]
#                    env.set_agents(agents)
#                    print("Switched to play old version of agent, from checkpoint: ", path, "\n\n")
#
#

            # Evaluate the performance. Play with random agents.
            if episode % args.evaluate_every == 0:                


                trained_reward = tournament3(env, args.num_eval_games)
 
                env.set_agents(eval_agents)                
                random_reward = tournament3(env, args.num_eval_games)
                env.set_agents(agents)
 
                
                logger.log_performance_tris(episode, random_reward, trained_reward)
                #logger.log_performance_bis(episode, trained_reward)

        # Get the paths
        csv_path, fig_path = logger.csv_path, logger.fig_path

    # Plot the learning curve
    plot_curve(csv_path, fig_path, args.algorithm)

    # Save model
    save_path = os.path.join(args.log_dir, 'model.pth')
    torch.save(agent, save_path)
    print('Model saved in', save_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("DQN/NFSP example in RLCard")
    parser.add_argument(
        '--env',
        type=str,
        default='briscola',
        choices=[
            'blackjack',
            'leduc-holdem',
            'limit-holdem',
            'doudizhu',
            'mahjong',
            'no-limit-holdem',
            'uno',
            'gin-rummy',
            'bridge',
            'briscola',
        ],
    )
    parser.add_argument(
        '--algorithm',
        type=str,
        default='dqn',
        choices=[
            'dqn',
            'nfsp',
        ],
    )
    parser.add_argument(
        '--cuda',
        type=str,
        default='cpu',
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
    )
    parser.add_argument(
        '--num_episodes',
        type=int,
        default=1000000,
    )
    parser.add_argument(
        '--num_eval_games',
        type=int,
        default=500,
    )
    parser.add_argument(
        '--evaluate_every',
        type=int,
        default=5000,
    )
    parser.add_argument(
        '--log_dir',
        type=str,
        default='experiments/briscola/',
    )
    
    parser.add_argument(
        "--load_checkpoint_path",
        type=str,
        default="experiments/briscola/",
    )
    
    parser.add_argument(
        "--save_every",
        type=int,
        default=25000
    )
    
    parser.add_argument(
         "--round_payoff",
            type=str,
            default="True",
    )

    parser.add_argument(
        "--switch_every",
        type=int,
        default=50000,
    )
    parser.add_argument(
        "--against_pretrained",
        type=str,
        default="True",
    )
    parser.add_argument(
        "--load",
        type=str,
        default="./experiments/model"
    )

    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda

    # create directory if not exists
    if not os.path.exists(args.log_dir):
        os.makedirs(args.log_dir)

    args.load_checkpoint_path = args.log_dir

    train(args)

