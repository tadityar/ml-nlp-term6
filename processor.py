from collections import Counter
import copy
from fractions import Fraction
import operator


class Processor:

	def parse_train(filename):
		tags = []
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
		f = open(filename, 'r', encoding = 'UTF-8')
		res = {}
		found = False
		for line in f:
			line = line.split()
			if len(line) > 0:
				word = line[0].lower()
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

	def parse_sentiment(filename):
		sentiments = []
		f = open(filename, 'r', encoding = 'UTF-8')
		res = {}
		found = False
		for line in f:
			line = line.split()
			if len(line) > 0:
				word = line[0]
				sentiment = line[1].split('-')
				if len(sentiment) > 1:
					sentiment = sentiment[1]
				else:
					# tag O as neutral straight
					sentiment = 'neutral'
				sentiments.append(sentiment)
				if word in res:
					found = True
					if sentiment not in res[word]:
						res[word][sentiment] = 1
					else:
						res[word][sentiment] += 1
				if not found:
					res[word] = {sentiment: 1}
					for i in ['START', 'positive', 'negative', 'neutral', 'STOP']:
						if i not in res[word]:
							res[word][i] = 0
				found = False
		sentiment_count = Counter(sentiments)
		f.close()
		return res, sentiment_count

	def parse_tag(filename):
		tags = []
		f = open(filename, 'r', encoding = 'UTF-8')
		res = {}
		found = False
		for line in f:
			line = line.split()
			if len(line) > 0:
				word = line[0]
				tag = line[1].split('-')[0]
				tags.append(tag)
				if word in res:
					found = True
					if tag not in res[word]:
						res[word][tag] = 1
					else:
						res[word][tag] += 1
				if not found:
					res[word] = {tag: 1}
					for i in ['START', 'O', 'B', 'I', 'STOP']:
						if i not in res[word]:
							res[word][i] = 0
				found = False
		tag_count = Counter(tags)
		f.close()
		return res, tag_count


	# Give emission parameters for any model chosen
	def get_emission_params(wordsCount, modelCount):
		wordsCountP = copy.deepcopy(wordsCount)
		for word, models_dict in wordsCountP.items():
			for model, value in models_dict.items():
				if modelCount[model] != 0:
					wordsCountP[word][model] = Fraction(value, modelCount[model])
				else:
					wordsCountP[word][model] = Fraction(0, 1)
		return wordsCountP


	#Given a certain input of most frequent words and their tags, classifies the least N occuring words into a #UNK# unknown field
	#Counts the sum of all the tags of a word. If sum < n, the count of the indiv tags are added to #UNK#, else they are added to the output as a valid word.
	def process_unknown_words(f,n,tags):
		output = {}
		output.update({'#UNK#':{}})
		for tag in tags:
			output['#UNK#'][tag] = 0
		for word in f:
			if sum(f[word][tags] for tags in f[word]) > n:
				output.update({word:f[word]})
			else:
				for tags in output['#UNK#']:
					output['#UNK#'][tags] += f[word][tags]
		return output

	def get_transition_params(filename, tags, type):
		f = open(filename, 'r', encoding = 'UTF-8')
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
			# print (words)
			if len(words) > 0:
				if type == 'normal':
					tag = words[-1]
				elif type == 'tag':
					tag = words[-1].split('-')[0]
				elif type == 'sentiment':
					tagsplit = words[-1].split('-')
					if len(tagsplit) > 1:
						tag = tagsplit[-1]
					else:
						tag = 'neutral'
				if currentTag == 'START':
					tagCount[tags.index('START')] += 1
					tagTransitionCount[tag][currentTag] += 1
					tagCount[tags.index(tag)] += 1
					currentTag = tag
				else:
					tagTransitionCount[tag][currentTag] += 1
					tagCount[tags.index(tag)] += 1
					currentTag = tag
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


	#Given a certain testing data set inp and a model generated from process_unknown_words, classifies all words not found in the model as #UNK#
	def process_unknown_words_testing(inp,model):
		output = copy.deepcopy(inp)
		for i in range(len(output)):
			for j in range(len(output[i])):
				for key in output[i][j]:
					present = False
					if model.get(key):
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

	def swap_if_different(tag_out1, tag_out2, ep_sent):
		res = []
		for i in range(len(tag_out1)):
			res.append([])
			for j in range(len(tag_out1[i])):
				if (tag_out2[i][j] not in tag_out1[i][j]):
					if (tag_out2[i][j] != 'O'):
						res[i].append(ep_sent[tag_out2[i][j][0]])
					else:
						res[i].append(tag_out2[i][j] + '-' + tag_out1[i][j][2:])
				else:
					res[i].append(tag_out1[i][j])
		return res

	def combine_tag_sentiment(tag_out, sentiment_out):
		res = []
		for i in range(len(tag_out)):
			res.append([])
			for j in range(len(tag_out[i])):
				if (tag_out[i][j] != 'O'):
					res[i].append(tag_out[i][j] + '-' + sentiment_out[i][j])
				else:
					res[i].append(tag_out[i][j])
		return res

	def get_tag_sentiment_ratio(tag_count, tag_plus_sent_count):
		res = {}
		for i in tag_plus_sent_count.keys():
			if i[0] not in res:
				res[i[0]] = {}
			res[i[0]][i] = tag_plus_sent_count[i]/tag_count[i[0]]

		for k, v in res.items():
			res[k] = max(v.items(), key=operator.itemgetter(1))[0]
		return res

