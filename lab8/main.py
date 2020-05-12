import gym
import numpy as np
import matplotlib.pyplot as plt

MAX_ITERATIONS = 5 * pow(10, 4)
EPSILON_THRESHOLD = pow(10, -5)
DISCOUNT_FACTOR = 0.9


def get_best_actions(env, state, V):
	A = np.zeros(env.action_space.n)

	for a in range(env.action_space.n):
		for prob, next_state, reward, done in env.P[state][a]:
			A[a] += prob * DISCOUNT_FACTOR * V[next_state]
			A[a] += reward

	return A


def value_iteration(env, V):
	states_len = env.observation_space.n
	num_iter = 0
	V_new = V[:]

	x = []
	while True:
		delta = 0
		num_iter += 1

		for state in range(states_len):
			A = get_best_actions(env, state, V)
			best_action_value = np.max(A)
			delta = max(delta, pow(np.abs(best_action_value - V[state]), 2))
			V_new[state] = best_action_value

		x.append(delta)

		V = V_new[:]
		if delta < EPSILON_THRESHOLD or num_iter > MAX_ITERATIONS:
			break

	print("iterations: ", num_iter)

	policy = np.zeros([states_len])
	for state in range(states_len):
		A = get_best_actions(env, state, V_new)
		policy[state] = np.argmax(A)

	return policy, V_new, x


def gauss_seidel_vi(env, V):
	states_len = env.observation_space.n
	num_iter = 0
	x = []

	while True:
		delta = 0
		num_iter += 1

		for state in range(states_len):
			A = get_best_actions(env, state, V)
			best_action_value = np.max(A)
			delta = max(delta, pow(np.abs(best_action_value - V[state]), 2))
			V[state] = best_action_value

		x.append(delta)
		if delta < EPSILON_THRESHOLD or num_iter > MAX_ITERATIONS:
			break

	print("iterations: ", num_iter)

	policy = np.zeros([states_len])
	for state in range(states_len):
		A = get_best_actions(env, state, V)
		policy[state] = np.argmax(A)

	return policy, V, x


def prioritized_sweeping_vi(env, old_val):
	states_len = env.observation_space.n
	V = old_val
	H = np.zeros(states_len)

	x = []

	for k in range(1000):
		newV = V[:]
		s_k = np.argmax(H)

		newV[s_k] = max(get_best_actions(env, s_k, newV))

		H[s_k] = abs(V[s_k] - newV[s_k])
		V = newV[:]

		x.append(H[s_k])

	policy = np.zeros([states_len])
	for state in range(states_len):
		A = get_best_actions(env, state, V)
		policy[state] = np.argmax(A)

	return policy, V, x


def main(game_name):
	env = gym.make(game_name)
	states_len = env.observation_space.n
	_x = dict()
	for i_episode in range(50):
		_x[i_episode] = []
		value_iter = None
		value_iter_old = np.zeros(states_len)

		observation = env.reset()

		for t in range(1):
			env.render()
			print(observation)

			# action = env.action_space.sample()

			if value_iter is not None:
				value_iter_old = value_iter[:]

			policy, value_iter, x = gauss_seidel_vi(env, value_iter_old)
			if t == 0:
				_x[i_episode] = x

			observation, reward, done, info = env.step(int(policy[env.s]))

			if done:
				print("Episode finished after {} timesteps".format(t + 1))
				break
	env.close()
	values_x = np.zeros(len(_x[0]))
	for key in range(len(_x.keys())):
		for val in range(len(_x[0])):
			values_x[val] += _x[key][val]

	for el in range(len(values_x)):
		values_x[el] = values_x[el] / len(values_x)
	values_y = [i for i in range(len(values_x))]

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(values_y, values_x)
	plt.ylabel('Diff')
	plt.xlabel('Iterations')
	plt.show()


if __name__ == '__main__':
	frozen = 'FrozenLake-v0'
	frozen_large = 'FrozenLake8x8-v0'
	taxi = 'Taxi-v3'
	main(frozen_large)
