class Viterbi:
	def __init__(self,t,e):
		self.t = t
		self.e = e
		self.tree = []

	#Please use this call to assign tags to the sequence
	def assign(self,seq):
		self.tree = [{} for i in range(len(seq)+1)]
		self.__viterbi_forward(seq,-1)
		out = self.__viterbi_backtrack(len(seq),seq)
		return out
		
	def __viterbi_forward(self,seq,state):
		if state == -1:
			self.tree[state+1]['START'] = 1
			self.__viterbi_forward(seq,state+1)

		elif state < len(seq):
			for v in self.t['tags'][1:-1]:
				vals = [{'prob':self.tree[state][u]*self.__get_transition_param(u,v)*self.__get_emission_param(seq,state,v),'tag' : u} for u in self.tree[state]]
				mx = max(vals,key=lambda x:x['prob'])
				self.tree[state+1][v] = mx['prob']

			self.__viterbi_forward(seq,state+1)

		else:
			vals = [{'prob' : self.tree[state][v]*self.__get_transition_param(v,'STOP'),'tag' : v} for v in self.tree[state]]
			mx = max(vals,key=lambda x:x['prob'])

	def __get_transition_param(self,u,v):
		return self.t['map'][v][u]
		# return self.t['map'][self.t['tags'].index(u)][self.t['tags'].index(v)]

	def __get_emission_param(self, seq, state, tag):
		word = list(seq[state].keys())[0]
		if word in self.e:
			if tag in self.e[word]:
				return self.e[word][tag]
			else:
				if tag == 'START' or tag == 'STOP':
					return 0
				return self.e["#UNK#"][tag]
		if tag == 'START' or tag == 'STOP':
			return 0
		return self.e["#UNK#"][tag]

	def __viterbi_backtrack(self,state,seq,y=None):
		if state == len(seq):
			vals = [{'prob' : self.tree[state][v]*self.__get_transition_param(v,'STOP'),'tag':v} for v in self.tree[state]]
			mx = max(vals,key=lambda x:x['prob'])
			return self.__viterbi_backtrack(state-1,seq,y=mx['tag']) + [mx['tag']]
		elif state > 0:
			vals = [{'prob' : self.tree[state][u]*self.__get_transition_param(u,y),'tag':u} for u in self.tree[state]]
			mx = max(vals,key=lambda x:x['prob'])
			return self.__viterbi_backtrack(state-1,seq,y=mx['tag']) + [mx['tag']]
		else:
			return []
