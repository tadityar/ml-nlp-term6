from copy import deepcopy

class Viterbi:
	def __init__(self, ep, tp):
		self.ep = ep
		self.tp = tp
		self.dp_table = []
		self.tags = tp['tags']

	def init_dp_table(self, sentence):
		self.dp_table.append([1,0,0,0,0,0,0,0,0])
		for word in sentence:
			self.dp_table.append([0,0,0,0,0,0,0,0,0])
		self.dp_table.append([0,0,0,0,0,0,0,0,0])

		self.__viterbi_forward(sentence, 1)
		# print(len(self.dp_table))
		# self.dp_table = []
	# REMEMBER TO CLEAR DP TABLE
	# careful of what layer is layer != word index
	# layer start at 1
	def __viterbi_forward(self, word_seq, layer):
		if layer < len(word_seq)+1:
			for tag in self.tags:
				val_for_tag = []
				for tag_p in self.tags:
					val_for_tag.append(self.get_transmission(tag_p, tag)*self.dp_table[layer-1][self.tags.index(tag_p)])
				word = list(word_seq[layer-1].keys())[0]
				# print(val_for_tag)
				self.dp_table[layer][self.tags.index(tag)] = max(val_for_tag)*self.get_emission(word, tag)
			self.__viterbi_forward(word_seq, layer+1)
		else:
			dp = deepcopy(self.dp_table)
			print(self.dp_table)
			self.dp_table = []
			return dp

	def get_emission(self, word, tag):
		for i in range(len(self.ep)):
			if word in self.ep[i]:
				if tag in self.ep[i][word]:
					return self.ep[i][word][tag]
				else:
					if tag == 'START' or tag == 'STOP':
						return 0
					return self.ep[0]["#UNK#"][tag]
		if tag == 'START' or tag == 'STOP':
			return 0
		return self.ep[0]["#UNK#"][tag]

	def get_transmission(self, initial, final):
		# return self.t[v][u]
		# print(self.tp['map'])
		# print(self.tags.index(initial))
		# print(self.tags.index(final))
		return self.tp['map'][self.tags.index(initial)][self.tags.index(final)]

	# def __get_emission_param(self,seq,state,v):
	# 	for i in range(len(self.e)):
	# 		for key in self.e[i]:
	# 			if key in list(seq[state].keys())[0]:
	# 				try:
	# 					return self.e[i][key][v]
	# 				except KeyError as er:
	# 					return self.e[0]["#UNK#"][v]
	# 	return self.e[0]["#UNK#"][v]
