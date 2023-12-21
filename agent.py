import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot
import config as cf


class Agent:

    def __init__(self):
        # initializing the Agent class
        pass

    def get_state(self, game):
        # defining different potential states
        pass

    def remember(self, state, action, reward, next_state, done):
        # the memory we want to remember the moves. we'll use queue data 
        # structure so when reached to the max it will remove from the begining 
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        # will get the action based on the state
        pass

def train():
    # the main function where later it will used the model to get trained
    pass

if __name__ == '__main__':
    train()