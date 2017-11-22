from collections import Counter
import copy

'''
Part 2
'''
def parse_train(filename):
	tags = []
	pairs = []
	words = []
	f = open(filename, 'r')
	res = []
	found = False
	for k in f:
		k = k.split()
		if len(k) > 0:
			k[0] = k[0].lower()
			tags.append(k[1])
			for i in res:
				if k[0] in i:
					found = True
					if k[1] not in i[k[0]]:
						i[k[0]][k[1]] = 1
					else:
						i[k[0]][k[1]] += 1
			if not found:
				res.append({k[0]: {k[1]: 1}})
			found = False
	tags_count = Counter(tags)
	return res, tags_count

# Give emission parameters
def get_emission_params(wordsCount, tagsCount):
	wordsCountP = copy.deepcopy(wordsCount)
	for l in wordsCountP:
		for k, v in l.items():
			for i, j in v.items():
				v[i] = j/tagsCount[i]
	return wordsCountP

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

def emission_param_preprocess(data):
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


#training	
words_count, tag_count = parse_train(r'D:\ISTD 2017-2\01-ML\EN\EN\train')
words_count = process_unknown_words(words_count,3)
ep = get_emission_params(words_count, tag_count)

# #testing
data = parser(r'D:\ISTD 2017-2\01-ML\EN\EN\dev.in')
data_p = process_unknown_words_testing(data,words_count)
ep_p = emission_param_preprocess(ep)
tagged_words = tagged_words(ep_p,data_p)

#testing vs actual output

'''
Part 3
'''

def get_transition_params(filename):
	f = open(filename, 'r')
	tags = ['START', 'O', 'B-positive', 'B-neutral', 'B-negative', 'I-positive', 'I-neutral', 'I-negative', 'STOP']
	currentTag = 'START'
	tagCount = [1,0,0,0,0,0,0,0,0]
	tagTransitionCount = []
	# initialise tagTransitionCount
	for i in tags:
		inner = []
		for j in tags:
			inner.append(0)
		tagTransitionCount.append(inner)

	# count transitions and tags
	for line in f:
		words = line.split()
		if len(words) > 0:
			tagTransitionCount[tags.index(currentTag)][tags.index(words[1])] += 1
			tagCount[tags.index(currentTag)] += 1
			currentTag = words[1]
		else:
			tagTransitionCount[tags.index(currentTag)][tags.index('STOP')] += 1
			tagCount[tags.index(currentTag)] += 1
			tagCount[-1] += 1
			currentTag = 'START'

	# count transition params
	for i in tagTransitionCount:
		for j in range(len(i)):
			i[j] = i[j]/tagCount[j]
	result = {'tags': tags, 'map': tagTransitionCount}
	return result
