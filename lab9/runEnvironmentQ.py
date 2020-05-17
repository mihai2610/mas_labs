#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 13:01:41 2019

@author: rgarzon
"""
import random
import gym
import numpy as np
import itertools

from collections import defaultdict

env = gym.make('gym_blocksworld:BlocksWorld-v0')
env.seed(0)
env.reset()

numBlocks = 3
num_episodes = 10

done = False
ep_lengths = []
n = 0

alpha = 0.1
gamma = 0.6
epsilon = 0.1

all_epochs = []
all_penalties = []
q_table = defaultdict(lambda: np.zeros(env.numactio0ns))
all_possible_actions = [(bl1, bl2) for bl1, bl2 in itertools.permutations(range(numBlocks + 1), 2)]
all_possible_actions += [(bl, bl) for bl in range(numBlocks + 1)]


def get_action_id(action_value):
	return all_possible_actions.index(action_value)


def policy_function(state):
	state = str(state)
	if q_table.get(state) is None:
		q_table[state] = np.zeros(env.numactions)

	action_probabilities = np.ones(env.numactions, dtype=float) * epsilon / env.numactions

	best_action = np.argmax(q_table[state])
	action_probabilities[best_action] += (1.0 - epsilon)
	return action_probabilities


while n < num_episodes:
	steps = 1
	done = False
	obs = env.reset()
	current_state = str(obs[:3])
	goal_state = str(obs[3:])
	action = [random.randint(0, numBlocks), random.randint(0, numBlocks)]

	while not done:

		action_id = np.argmax(policy_function(current_state))  # Exploit learned values
		action = all_possible_actions[action_id]

		obs, reward, done, empty = env.step([action[0], action[1]])

		next_state = str(obs[:3])
		goal_state = obs[3:]

		if q_table.get(current_state) is None:
			q_table[current_state] = np.zeros(env.numactions)

		old_value = q_table[current_state][get_action_id(action)]
		next_max = np.max(q_table[current_state])

		new_value = old_value + alpha * (reward + gamma * next_max - old_value)
		print(new_value)
		q_table[current_state][get_action_id(action)] = new_value
		current_state = next_state
		print('Next action ' + str(action))
		print('Observation ' + str(obs))

		# env.render()
		steps += 1
		print(done)
	print('New episode')
	ep_lengths.append(steps)
	n += 1

	print('----------------')
	print('Number of blocks: ' + str(numBlocks))
	print('Number of episodes run: ' + str(num_episodes))
	print("Average episode length (steps) " + str(sum(ep_lengths) / float(len(ep_lengths))))
# input("Press Enter to continue...")
