from collections import Counter
import copy
from viterbi import Viterbi
from forward_backward import ForwardBackward
from fractions import Fraction
from posterior_viterbi import PosteriorViterbi


'''
Part 2
'''
def parse_train(filename):
	tags = []
	pairs = []
	words = []
	f = open(filename, 'r', encoding = 'UTF-8')
	res = {}
	found = False
	for line in f:
		line = line.split()
		if len(line) > 0:
			word = line[0]
			tag = line[1]
			tags.append(tag)
			if word in res:
				found = True
				if tag not in res[word]:
					res[word][tag] = 1
				else:
					res[word][tag] += 1
			if not found:
				res[word] = {tag: 1}
				for i in ['START', 'O', 'B-positive', 'B-neutral', 'B-negative', 'I-positive', 'I-neutral', 'I-negative', 'STOP']:
					if i not in res[word]:
						res[word][i] = 0
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

# Give emission parameters
def get_emission_params(wordsCount, tagCount):
	wordsCountP = copy.deepcopy(wordsCount)
	for word, tags_dict in wordsCountP.items():
		for tag, value in tags_dict.items():
			if tagCount[tag] != 0:
				wordsCountP[word][tag] = Fraction(value, tagCount[tag])
			else:
				wordsCountP[word][tag] = Fraction(0, 1)
	return wordsCountP



#Given a certain input of most frequent words and their tags, classifies the least N occuring words into a #UNK# unknown field
#Counts the sum of all the tags of a word. If sum < n, the count of the indiv tags are added to #UNK#, else they are added to the output as a valid word.
def process_unknown_words(f,n):
	output = {}
	output.update({'#UNK#':{'O': 0, 'START': 0, 'B-positive': 0, 'B-neutral': 0, 'B-negative': 0, 'I-positive': 0, 'I-neutral': 0, 'I-negative': 0, 'STOP': 0}})
	for word in f:
		if sum(f[word][tags] for tags in f[word]) > n:
			output.update({word:f[word]})
		else:
			for tags in output['#UNK#']:
				output['#UNK#'][tags] += f[word][tags]
	return output

#######################################

#process_unknown_words_testing needs to be updated

#######################################

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
		highestVal = 0
		for tag in data[wordset]:
			value = data[wordset][tag]
			if value>highestVal:
				highestVal = value
				highestTag = tag
		wordAndTag.update({wordset:highestTag})
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
			noneDict = {line:"None"}
			sentence.append(noneDict)
	file.close()
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
		for dictionary in sentence:
			for key,value in dictionary.items():
				line = key+" "+ value + "\n"
				output = output + line
		output = output + "\n"
	return output
	
def output_file(data,fileName):
	file = open(fileName,"w", encoding = 'UTF-8')
	file.write(data)
	file.write('\n')
	file.close()
	
'''
Part 3
'''

def get_transition_params(filename):
	f = open(filename, 'r', encoding = 'UTF-8')
	tags = ['START', 'O', 'B-positive', 'B-neutral', 'B-negative', 'I-positive', 'I-neutral', 'I-negative', 'STOP']
	currentTag = 'START'
	tagCount = [0,0,0,0,0,0,0,0,0]
	tagTransitionCount = {}
	# initialise tagTransitionCount
	for i in tags:
		inner = {}
		for j in tags:
			inner[j] = 0
		tagTransitionCount[i] = inner

	# count transitions and tags
	for line in f:
		words = line.split()
		if len(words) > 0:
			if currentTag == 'START':
				tagCount[tags.index('START')] += 1
				tagTransitionCount[words[1]][currentTag] += 1
				tagCount[tags.index(words[1])] += 1
				currentTag = words[1]
			else:
				tagTransitionCount[words[1]][currentTag] += 1
				tagCount[tags.index(words[1])] += 1
				currentTag = words[1]
		else:
			tagTransitionCount['STOP'][currentTag] += 1
			tagCount[tags.index('STOP')] += 1
			currentTag = 'START'
			tagCount[tags.index('START')] += 1 

	# count transition params
	for final, val in tagTransitionCount.items():
		for initial, val_p in tagTransitionCount[final].items():
			tagTransitionCount[final][initial] = Fraction(val_p, tagCount[tags.index(initial)])

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

## <<< RESULTS FOR PART 2 >>>>
	
#training	
words_count, tag_count = parse_train(r'EN/train')
words_count = process_unknown_words(words_count,3)
ep = get_emission_params(words_count, tag_count)
# data = parser(r'EN/dev.in')
# data_p = process_unknown_words_testing(data,words_count)
# ep_p = emission_param_preprocess(ep)
# tagged_words = tagging_words(ep_p,data_p)

#testing vs actual output
# output_to_file = convert_back(tagged_words)
# output_file(output_to_file,r'EN/dev.p2.out')

## <<< RESULTS FOR PART 3 >>>

tp = get_transition_params(r'EN/train')

seq = parser(r'EN/dev.in')


# ### RUNNING VITERBI ###

v = PosteriorViterbi(tp,ep)
v_out = []

for s in seq:
	out = v.assign(s)
	v_out.append(out)
	print (out)
	# print (out)

v_seq = v_result_parse(v_out,seq)


output_to_file = convert_back(v_seq)
output_file(output_to_file,r'EN/dev.pv.out')
print ("done")



# ### RUNNING FORWARDBACKWARD ###
# v = ForwardBackward(tp,ep)
# v_out = []
# for s in seq:
# 	out = v.assign(s)
# 	v_out.append(out)
# v_seq = v_result_parse(v_out,seq)
# output_to_file = convert_back(v_seq)
# output_file(output_to_file,r'EN/dev.fb.out')
# print ("done")



# p = viterbi(seq,-1,tp,ep)
# print (p)

# o = viterbi_backtrack(tp,p,'STOP')
# print (o)
