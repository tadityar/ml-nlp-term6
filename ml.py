from collections import Counter
import copy

def parse_train(filename):
	tags = []
	pairs = []
	words = []
	f = open(filename, 'r')
	res = {}
	for k in f:
		k = k.split()
		if len(k) > 0:
			k[0] = k[0].lower()
			tags.append(k[1])
			if k[0] not in res:
				res[k[0]] = {}
				res[k[0]][k[1]] = 1
			else:
				if k[1] not in res[k[0]]:
					res[k[0]][k[1]] = 1
				else:
					res[k[0]][k[1]] += 1
	tags_count = Counter(tags)
	return res, tags_count

def get_emission_params(words_count, tags_count):
	words_count_p = copy.deepcopy(words_count)
	for k, v in words_count_p.items():
		for i, j in v.items():
			v[i] = j/tags_count[i]
	return words_count_p
