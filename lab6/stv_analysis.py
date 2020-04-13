from preflibtools import io
from preflibtools.generate_profiles import gen_mallows, gen_cand_map, gen_impartial_culture_strict
from typing import List, Dict, Tuple
import random
import operator
import collections

PHIS = [0.7, 0.8, 0.9, 1.0]
NUM_VOTERS = [100, 500, 1000]
NUM_CANDIDATES = [4, 6, 10, 15]


def generate_random_mixture(nvoters: int = 100, ncandidates: int = 6, num_refs: int = 3, phi: float = 1.0) \
		-> Tuple[Dict[int, str], List[Dict[int, int]], List[int]]:
	"""
	Function that will generate a `voting profile` where there are num_refs mixtures of a
	Mallows model, each with the same phi hyperparameter
	:param nvoters: number of voters
	:param ncandidates: number of candidates
	:param num_refs: number of Mallows Mixtures in the voting profile
	:param phi: hyper-parameter for each individual Mallows model
	:return: a tuple consisting of:
		the candidate map (map from candidate id to candidate name),
		a ranking list (list consisting of dictionaries that map from candidate id to order of preference)
		a ranking count (the number of times each vote order comes up in the ranking list,
		i.e. one or more voters may end up having the same preference over candidates)
	"""
	candidate_map = gen_cand_map(ncandidates)

	mix = []
	phis = []
	refs = []

	for i in range(num_refs):
		refm, refc = gen_impartial_culture_strict(1, candidate_map)
		refs.append(io.rankmap_to_order(refm[0]))
		phis.append(phi)
		mix.append(random.randint(1, 100))

	smix = sum(mix)
	mix = [float(m) / float(smix) for m in mix]

	rmaps, rmapscounts = gen_mallows(nvoters, candidate_map, mix, phis, refs)

	return candidate_map, rmaps, rmapscounts


def get_next_candidate(candidate: int, possible_candidates: List[int], next_candidates: Dict[int, Dict[int, int]]):
	if candidate not in next_candidates:
		return None

	candidates_ranks_desc = collections.OrderedDict(
		sorted(next_candidates[candidate].items(), key=lambda x: x[1], reverse=True))

	for possible_candidate in candidates_ranks_desc.keys():
		if possible_candidate in possible_candidates:
			return possible_candidate

	return None


def stv(nvoters: int,
		canidate_map: Dict[int, str],
		rankings: List[Dict[int, int]],
		ranking_counts: List,
		top_k: int,
		required_elected: int) -> List[int]:
	"""
	:param nvoters: number of voters
	:param canidate_map: the mapping of candidate IDs to candidate names
	:param rankings: the expressed full rankings of voters, specified as a list of mapping from candidate_id -> rank
	:param ranking_counts:
	:param top_k: the number of preferences taken into account [min: 2, max: (num_candidates - 1), aka full STV]
	:return: The list of elected candidate id-s
	"""
	# TODO: implement STV-k

	threshold = float(nvoters / (required_elected + 1)) + 1

	candidates_ranks: Dict[int, int] = dict.fromkeys(range(1, len(canidate_map.keys()) + 1), 0)
	next_candidates: Dict[int, Dict[int, int]] = dict()

	for voter in range(len(rankings)):
		voted_candidate = list(rankings[voter].keys())[0]
		candidates_ranks[voted_candidate] += ranking_counts[voter]

		for voter_decision in list(rankings[voter].keys())[1:top_k]:
			if voted_candidate not in next_candidates:
				next_candidates[voted_candidate] = {}
			if voter_decision not in next_candidates[voted_candidate]:
				next_candidates[voted_candidate][voter_decision] = 0

			next_candidates[voted_candidate][voter_decision] += rankings[voter][voter_decision] * ranking_counts[voter]
	# 	to ask  {+= rankings[voter][voter_decision] * ranking_counts[voter]}
	_elected_candidates = []

	for candidate in candidates_ranks.copy().keys():
		if candidates_ranks[candidate] > threshold:
			remaining_votes = candidates_ranks[candidate] - threshold
			next_candidate_key = get_next_candidate(candidate, list(candidates_ranks.keys()), next_candidates)
			if next_candidate_key is not None:
				candidates_ranks[next_candidate_key] += remaining_votes

			_elected_candidates.append(candidate)
			del candidates_ranks[candidate]
			del next_candidates[candidate]

	i = 0
	while len(_elected_candidates) < required_elected and i < 1000 and len(candidates_ranks.keys()) > 0:
		i += 1
		candidates_ranks = collections.OrderedDict(
			sorted(candidates_ranks.items(), key=lambda x: x[1], reverse=True))

		last_candidate_key = list(candidates_ranks.keys())[-1]
		next_candidate_key = get_next_candidate(last_candidate_key,
												list(candidates_ranks.keys()),
												next_candidates)

		if next_candidate_key is not None:
			candidates_ranks[next_candidate_key] += candidates_ranks[last_candidate_key]

		del candidates_ranks[last_candidate_key]

		for candidate in candidates_ranks.copy().keys():
			if candidates_ranks[candidate] > threshold:
				remaining_votes = candidates_ranks[candidate] - threshold
				next_candidate_key = get_next_candidate(candidate,
														list(candidates_ranks.keys()),
														next_candidates)
				if next_candidate_key is not None:
					candidates_ranks[next_candidate_key] += remaining_votes

				_elected_candidates.append(candidate)
				del candidates_ranks[candidate]
				del next_candidates[candidate]

	return _elected_candidates


if __name__ == "__main__":
	# i = 0
	# j = 0
	# p = 0
	num_refs = 4
	required_elected = 4

	for i in range(len(NUM_VOTERS)):
		print(" ++++++++++++++++++++++ num_voters = ", NUM_VOTERS[i], " ++++++++++++++++++++++++++++++++++++++++++")
		for j in range(len(NUM_CANDIDATES)):
			spaces = " " * j * 4
			print()
			print(spaces, "=================== num candiates = ", NUM_CANDIDATES[j], "======================")
			print()
			for p in range(len(PHIS)):
				print(spaces, "[  phi = ", PHIS[p], " ]")
				cmap, rmaps, rmapscounts = generate_random_mixture(nvoters=NUM_VOTERS[i],
																   ncandidates=NUM_CANDIDATES[j],
																   num_refs=num_refs, phi=PHIS[p])
				elected_candidates_by_all = stv(NUM_VOTERS[i], cmap, rmaps, rmapscounts, NUM_CANDIDATES[j], required_elected)
				print(spaces, "       elected considering all = ", NUM_CANDIDATES[j], " : ", elected_candidates_by_all)
				for top_k in range(2, NUM_CANDIDATES[j]):
					elected_candidates = stv(NUM_VOTERS[i], cmap, rmaps, rmapscounts, top_k, required_elected)
					intersection = [value for value in elected_candidates_by_all if value in elected_candidates]

					print(spaces, "		elected considering top_k = ", top_k, " : ", elected_candidates,
						  " => ", len(intersection), " coincidences : ", intersection)
				# print(cmap)
				# print(rmaps)
				# print(rmapscounts)
