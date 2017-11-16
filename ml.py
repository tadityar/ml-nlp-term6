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

def generate_tagged_words(data):
	wordAndTag = {}
	for wordset in data:
		for word in wordset:
			for tag in wordset[word]:
				highestVal = 0
				if wordset[word][tag]>highestVal:
					highestVal = wordset[word][tag]
					highestTag = tag
			print (word,highestTag,highestVal)
			wordAndTag.update({word:highestTag})
	return wordAndTag

def tagging_words(wordAndTag,filename):
	taggedData = []
	file = open(filename,'r')
	for word in file:
		wordWONL = word.rstrip()
		if wordWONL in wordAndTag:
			tag = wordAndTag.get(wordWONL)
			taggedWord = {wordWONL:tag}
			taggedData.append(taggedWord)
		else:
			print (wordWONL)
	return taggedData
	
#parser creates [[{word:None},{word:None}],[{word:None},{word:None}]], separating sentences. 
#parser requires that you end with 2 newlines at the end of the file. (same as the dev.in)
def parser (filename):
	file = open(filename,'r')
	entiredata = []
	sentence = []

	for line in file:
		if line == "\n":
			entiredata.append(sentence)
			sentence = []
		else:
			line = line.rstrip()
			noneDict = {line:"None"}
			sentence.append(noneDict)
	return (entiredata)