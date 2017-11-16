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

#Given a certain input of most frequent words and their tags, classifies the least N occuring words into a #UNK# unknown field
def process_unknown_words(f,n):
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

#Given a certain testing data set inp and a model generated from process_unknown_words, classifies all words not found in the model as #UNK#
def process_unknown_words_testing(inp,model):
	output = copy.deepcopy(inp)
	for i in range(len(output)):
		for j in range(len(output[i])):
			for key in output[i][j]:
				for word in model:
					if word.get(key):
						output[i][j] = {key : None}
					else:
						output[i][j] = {'#UNK#' : None}
	return output

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
	return entiredata

#new tagging_words that works with the new parser above

def tagging_words(wordAndTag,entiredata):
	sentenceCounter = 0
	wordCounter = 0
	for sentence in entiredata:
		for wordDict in sentence:
			for word in wordDict:
				if word in wordAndTag:
					tag = wordAndTag.get(word)
					entiredata[sentenceCounter][wordCounter][word] = tag
			wordCounter += 1        
		sentenceCounter += 1
	return entiredata

	
testing_data = parser(r'D:\ISTD 2017-2\01-ML\EN\EN\dev.in')

processed_data = process_unknown_words_testing(testing_data,[{"thes" : {"O" : 200}}])

print (processed_data)