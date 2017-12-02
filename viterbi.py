class Viterbi:
	def __init__(self,t,e):
		self.t = t
		self.e = e
		self.tree = []

	#Please use this call to assign tags to the sequence
	def assign(self,seq):
		self.tree = [{} for i in range(len(seq)+1)]
		return self.__viterbi_backtrack(self.__viterbi_forward(seq,-1)[:-1],'STOP',seq)
		
	def __viterbi_forward(self,seq,state,pre_t=None):
		if state == -1:
			return self.__viterbi_forward(seq,state+1,'START')
		elif state < len(seq):
			values = []
			for v in self.t['tags'][1:-1]:
				lst = self.__get_transition_param(pre_t,v)*self.__get_emission_param(seq,state,v)
				result = self.tree[state+1][v] if self.tree[state+1].get(v) else self.__viterbi_forward(seq,state+1,v)
				val = {'val' : result,'tag' : v, 'lst' : lst}
				self.tree[state][val['tag']] = val['val'] + [val['val'][-1]*val['lst']]
				values.append(val)				

			o = max(values,key=lambda x:x['val'][-1]*x['lst'])
			return o['val'] + [o['val'][-1]*o['lst']]
		else:
			self.tree[state][pre_t] = [self.__get_transition_param(pre_t,'STOP')]
			return [self.__get_transition_param(pre_t,'STOP')]

	def __get_transition_param(self,u,v):
		return self.t['map'][self.t['tags'].index(u)][self.t['tags'].index(v)]

	def __get_emission_param(self,seq,state,v):
		for i in range(len(self.e)):
			for key in self.e[i]:
				if key in list(seq[state].keys())[0]:
					try:
						return self.e[i][key][v]
					except KeyError as er:
						return self.e[0]["#UNK#"][v]
		return self.e[0]["#UNK#"][v]

	def __viterbi_backtrack(self,pi,post,seq):
		if len(pi) == 0:
			return []
		vals = [{'p':pi[-1]*self.__get_transition_param(v,post)*self.__get_emission_param(seq,len(seq)-1,v),'v':v} for v in self.t['tags'][1:-1]]
		o = max(vals,key=lambda x:x['p'])
		return self.__viterbi_backtrack(pi[:-1],o['v'],seq[:-1]) + [o['v']]
