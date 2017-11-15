from collections import Counter

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

# print(parse_train('dev.out'))

def process_unknown(f,n):
	output = []
	output.append({"#UNK#" : []})
	for word in f:
		if sum([list(word.values())[0][key] for key in list(word.values())[0]]) > n:
			output.append(word)
		else:
			for key in list(word.values())[0]:
				if output[0].get(key):
					output[0][key] += list(word.values())[0][key]
				else:
					output[0][key] = list(word.values())[0][key]

	return output



data = [
	{"Trump" : {"A" : 200, "B" : 300, "C" : 400}},
	{"Hillary" : {"A" : 1, "B" : 1}},
	{"Matilda" : {"A" : 50, "B" : 60, "C" : 80}}
]

out = process_unknown(data,5)

print (out)