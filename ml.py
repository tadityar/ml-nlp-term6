from collections import Counter

def parse_train(filename):
	tags = []
	words = []
	f = open(filename, 'r')
	for line in f:
		line = line.split()
		if len(line) > 0:
			words.append(line[0])
			tags.append(line[1])
	tags = set(tags)
	word_count = Counter(words)
	print(tags)
	# print(word_count)

parse_train('train')
