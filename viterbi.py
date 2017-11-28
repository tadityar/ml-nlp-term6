class Viterbi:
	def __init__(self,t,e):
		self.t = t
		self.e = e

	#Please use this call to assign tags to the sequence
	def assign(self,seq):
		return self.__viterbi_backtrack(self.__viterbi_forward(seq,-1),'STOP')

	def __viterbi_forward(self,seq,state,pre_t=None):
		if state == -1:
			return self.__viterbi_forward(seq,state+1,'START')
		elif state < len(seq):
			mx = max([{'r' : self.__viterbi_forward(seq,state+1,v),'l':self.__get_transition_param(pre_t,v)*self.__get_emission_param(seq,state,v)} for v in self.t['tags']],key=lambda x:x['r'][-1]*x['l'])	
			return mx['r'] + [mx['r'][-1]*mx['l']]
		else:
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
						return 0
		return 0

	def __viterbi_backtrack(self,pi,post):
		if len(pi) == 1:
			return []
		o = max([{'p':pi[-1]*self.__get_transition_param(v,post),'v':v} for v in self.t['tags']],key=lambda x:x['p'])
		return [o['v']] +self.__viterbi_backtrack(pi[:-1],o['v'])
