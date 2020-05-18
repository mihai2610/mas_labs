from environment import *
from random import choice
import itertools
from collections import defaultdict
import numpy as np

alpha = 0.1
gamma = 0.6
epsilon = 0.1


def sars():
	TEST_SUITE = "tests/0a/"

	EXT = ".txt"
	SI = "si"
	SF = "sf"

	start_stream = open(TEST_SUITE + SI + EXT)
	end_stream = open(TEST_SUITE + SF + EXT)

	env = DynamicEnvironment(BlocksWorld(input_stream=start_stream), BlocksWorld(input_stream=end_stream), dynamics=.0)

	available_actions = [NoAction(), Unstack(Block("A"), Block("B")), PutDown(Block("A")), PickUp(Block("B")),
						 Stack(Block("B"), Block("C"))]
	q_table = dict()

	def policy_function(state):
		num_actions = len(available_actions)
		state = str(state)
		if q_table.get(state) is None:
			q_table[state] = np.zeros(num_actions)

		action_probabilities = np.ones(num_actions, dtype=float) * epsilon / num_actions

		best_action = np.argmax(q_table[state])
		action_probabilities[best_action] += (1.0 - epsilon)
		return action_probabilities

	env.reset()
	old_state = env.get_world_state()
	action_id = np.argmax(policy_function(old_state))
	act = available_actions[action_id]

	for i in range(100):
		print("=============== STEP %i ===============" % i)
		state, reward, done = env.step(act)

		action_id = np.argmax(policy_function(old_state))
		new_act = available_actions[action_id]

		if q_table.get(old_state) is None:
			q_table[old_state] = np.zeros(len(available_actions))

		if q_table.get(state) is None:
			q_table[state] = np.zeros(len(available_actions))

		old_value = q_table[old_state][available_actions.index(act)]
		next_max = np.max(q_table[state])

		new_value = old_value + alpha * (reward + gamma * next_max - old_value)

		q_table[old_state][available_actions.index(act)] = new_value
		old_state = state
		act = new_act

		print("## Chosen action: " + str(act))
		print("## State\n")
		print(state)

		print(env)

		print("\n")
		print("Reward: " + str(reward))

		print("\n")
		print("done: " + str(done))

		if done:
			break


def learning_q():
	TEST_SUITE = "tests/0a/"

	EXT = ".txt"
	SI = "si"
	SF = "sf"

	start_stream = open(TEST_SUITE + SI + EXT)
	end_stream = open(TEST_SUITE + SF + EXT)

	env = DynamicEnvironment(BlocksWorld(input_stream=start_stream), BlocksWorld(input_stream=end_stream), dynamics=.0)

	available_actions = [NoAction(), Unstack(Block("A"), Block("B")), PutDown(Block("A")), PickUp(Block("B")),
						 Stack(Block("B"), Block("C"))]
	q_table = dict()

	def policy_function(state):
		num_actions = len(available_actions)
		state = str(state)
		if q_table.get(state) is None:
			q_table[state] = np.zeros(num_actions)

		action_probabilities = np.ones(num_actions, dtype=float) * epsilon / num_actions

		best_action = np.argmax(q_table[state])
		action_probabilities[best_action] += (1.0 - epsilon)
		return action_probabilities

	env.reset()
	current_state = env.get_world_state()
	act = choice(available_actions)
	for i in range(100):
		print("=============== STEP %i ===============" % i)
		action_id = np.argmax(policy_function(current_state))
		act = available_actions[action_id]
		state, reward, done = env.step(act)

		if q_table.get(current_state) is None:
			q_table[current_state] = np.zeros(env.numactions)

		old_value = q_table[current_state][available_actions.index(act)]
		next_max = np.max(q_table[current_state])

		new_value = old_value + alpha * (reward + gamma * next_max - old_value)

		q_table[current_state][available_actions.index(act)] = new_value
		current_state = state

		print("## Chosen action: " + str(act))
		print("## State\n")
		print(state)

		print(env)

		print("\n")
		print("Reward: " + str(reward))

		print("\n")
		print("done: " + str(done))

		if done:
			break


def main():
	TEST_SUITE = "tests/0a/"

	EXT = ".txt"
	SI = "si"
	SF = "sf"

	start_stream = open(TEST_SUITE + SI + EXT)
	end_stream = open(TEST_SUITE + SF + EXT)

	env = DynamicEnvironment(BlocksWorld(input_stream=start_stream), BlocksWorld(input_stream=end_stream), dynamics=.0)

	available_actions = [NoAction(), Unstack(Block("A"), Block("B")), PutDown(Block("A")), PickUp(Block("B")),
						 Stack(Block("B"), Block("C"))]

	for i in range(100):
		print("=============== STEP %i ===============" % i)

		act = choice(available_actions)
		state, reward, done = env.step(act)

		index = available_actions.index(act)

		print("## Chosen action: " + str(act))
		print("## State\n")
		print(state)

		print(env)

		print("\n")
		print("Reward: " + str(reward))

		print("\n")
		print("done: " + str(done))

		if done:
			break


if __name__ == "__main__":
	learning_q()
