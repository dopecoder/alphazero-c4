import Arena
from MCTS import MCTS
from connect4.Connect4Players import *
from connect4.Connect4Game import Connect4Game
from connect4.tensorflow.NNet import NNetWrapper as NNet


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

human_vs_cpu = False
step_vs_cpu = True
g = Connect4Game()

# all players
rp = RandomPlayer(g).play
gp = OneStepLookaheadConnect4Player(g).play
hp = HumanConnect4Player(g).play



# nnet players
n1 = NNet(g)
n1.load_checkpoint('./temp/','best.pth.tar')
args1 = dotdict({'numMCTSSims': 100, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

if human_vs_cpu:
    player2 = hp
elif step_vs_cpu:
    player2 = gp
else:
    n2 = NNet(g)
    n2.load_checkpoint('./temp/', 'checkpoint_10.pth.tar')
    args2 = dotdict({'numMCTSSims': 100, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display=Connect4Game.display)

print(arena.playGames(100, verbose=True))
