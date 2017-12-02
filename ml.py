from collections import Counter
import copy
from viterbi import Viterbi
from forward_backward import ForwardBackward

'''
Part 2
'''
def parse_train(filename):
	tags = []
	pairs = []
	words = []
	f = open(filename, 'r', encoding = 'UTF-8')
	res = []
	found = False
	for k in f:
		k = k.split()
		if len(k) > 0:
			k[0] = k[0]
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
	f.close()
	return res, tags_count

def parse_train_lower(filename):
	tags = []
	pairs = []
	words = []
	f = open(filename, 'r', encoding = 'UTF-8')
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
	f.close()
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
	output.append({"#UNK#" : {}})
	for word in f:
		if sum([list(word.values())[0][key] for key in list(word.values())[0]]) > n:
			output.append(word)
		else:
			for key in list(word.values())[0]:
				if output[0].get(key):
					output[0]["#UNK#"][key] += list(word.values())[0][key]
				else:
					output[0]["#UNK#"][key] = list(word.values())[0][key]

	return output

#Given a certain testing data set inp and a model generated from process_unknown_words, classifies all words not found in the model as #UNK#
def process_unknown_words_testing(inp,model):
	output = copy.deepcopy(inp)
	for i in range(len(output)):
		for j in range(len(output[i])):
			for key in output[i][j]:
				present = False
				for word in model:
					if word.get(key):
						present = key
				output[i][j] = {present : None} if present else {'#UNK#' : None}
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
			# print (word,highestTag,highestVal)
			wordAndTag.update({word:highestTag})
	return wordAndTag

	
#parser creates [[{word:None},{word:None}],[{word:None},{word:None}]], separating sentences. 
#parser requires that you end with 2 newlines at the end of the file. (same as the dev.in)
def parser (filename):
	file = open(filename,'r', encoding = 'UTF-8')
	entiredata = []
	sentence = []

	for line in file:
		if line == "\n":
			entiredata.append(sentence)
			sentence = []
		else:
			line = line.rstrip()
			noneDict = {line.lower():"None"}
			sentence.append(noneDict)
	f.close()
	return entiredata

#new tagging_words that works with the new parser above
#this needs to be reworked, to check if the word in  is inside wordAndTag and then 
def tagging_words(wordAndTag,entiredata):
	sentenceCounter = 0
	for sentence in entiredata:
		wordCounter = 0
		for wordDict in sentence:
			for word in wordDict:
				if word in wordAndTag:
					tag = wordAndTag.get(word)
					entiredata[sentenceCounter][wordCounter][word] = tag
				else:
					entiredata[sentenceCounter][wordCounter][word] = "None"
			wordCounter += 1
			# print ("wordCounter")
			# print (wordCounter)
		sentenceCounter += 1
		# print ("sentence")
		# print (sentenceCounter)
	return entiredata

def convert_back(p_data):
	line = ""
	output = ""
	for sentence in p_data:
		output = output + "\n"
		for dictionary in sentence:
			for key,value in dictionary.items():
				line = key+" "+ value + "\n"
				output = output + line
	return output
	
def output_file(data,fileName):
    file = open(fileName,"a", encoding = 'UTF-8')
    file.write(data)
    file.close()
	
	
#training	
words_count, tag_count = parse_train(r'EN\train')
words_count = process_unknown_words(words_count,3)
ep = get_emission_params(words_count, tag_count)

# #testing
data = parser(r'EN\dev.in')
data_p = process_unknown_words_testing(data,words_count)
ep_p = emission_param_preprocess(ep)
tagged_words = tagging_words(ep_p,data_p)

#testing vs actual output
# output_to_file = convert_back(tagged_words)
# output_file(output_to_file,r'EN\dev.p2.out')


'''
Part 3
'''

def get_transition_params(filename):
	f = open(filename, 'r', encoding = 'UTF-8')
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
	f.close()
	return result

##Writing a function to assign the viterbi output back to the seq
## that was passed in. v_out = [[tag,tag],[]] seq = [[{},{}],[{},{}]]
def v_result_parse(v_out,seq):
	sentenceCounter = 0
	for sentence in seq:
		wordCounter = 0
		for wordDict in sentence:
			for key in wordDict:
				wordDict[key] = v_out[sentenceCounter][wordCounter]
			wordCounter += 1
		sentenceCounter += 1
	return (seq)

tp = get_transition_params(r'EN\train')

seq = parser(r'EN\dev.in')


### RUNNING VITERBI ###
# v = Viterbi(tp,ep)
# v_out = []

# for s in seq:
# 	out = v.assign(s)
# 	print (out)
# 	# print (out)
# 	v_out.append(out)
# 	# print (v_out)
# v_seq = v_result_parse(v_out,seq)
# # print (v_seq)

# output_to_file = convert_back(v_seq)
# output_file(output_to_file,r'EN\dev.v.out')
# print ("done")

# ### RUNNING FORWARDBACKWARD ###
v = ForwardBackward(tp,ep)
v_out = []
for s in seq:
	out = v.assign(s)
	v_out.append(out)
v_seq = v_result_parse(v_out,seq)
output_to_file = convert_back(v_seq)
output_file(output_to_file,r'EN\dev.fb.out')
print ("done")



# p = viterbi(seq,-1,tp,ep)
# print (p)

# o = viterbi_backtrack(tp,p,'STOP')
# print (o)