from collections import Counter

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
					for i in ['positive', 'negative', 'neutral']:
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
			# print (words)
			if len(words) > 0:
				if currentTag == 'START':
					tagCount[tags.index('START')] += 1
					tagTransitionCount[words[-1]][currentTag] += 1
					tagCount[tags.index(words[-1])] += 1
					currentTag = words[-1]
				else:
					tagTransitionCount[words[-1]][currentTag] += 1
					tagCount[tags.index(words[-1])] += 1
					currentTag = words[-1]
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
