class Viterbi:
	def __init__(self,t,e):
		self.t = t
		self.e = e
		self.tree = []

	#Please use this call to assign tags to the sequence
	def assign(self,seq):
		self.tree = [{} for i in range(len(seq)+1)]
		out = self.__viterbi_backtrack(self.__viterbi_forward(seq,-1)[:-1],'STOP',seq)
		return out
		
		# if state == -1:
		# 	return self.__viterbi_forward(seq,state+1,'START')
		# elif state < len(seq):
		# 	values = []
		# 	for v in self.t['tags'][1:-1]:
		# 		lst = self.__get_transition_param(pre_t,v)*self.__get_emission_param(seq,state,v)
		# 		result = self.tree[state+1][v] if self.tree[state+1].get(v) else self.__viterbi_forward(seq,state+1,v)
		# 		val = {'val' : result,'tag' : v, 'lst' : lst}
		# 		self.tree[state][val['tag']] = val['val'] + [val['val'][-1]*val['lst']]
		# 		values.append(val)				

		# 	o = max(values,key=lambda x:x['val'][-1]*x['lst'])
		# 	return o['val'] + [o['val'][-1]*o['lst']]
		# else:
		# 	self.tree[state][pre_t] = [self.__get_transition_param(pre_t,'STOP')]
		# 	return self.tree[state][pre]

		##### IMP 2 #####
		# if state == len(seq):
		# 	o = max([{'prob' : self.__viterbi_forward(seq,state-1,v), 'cur' : self.__get_transition_param(v,'STOP')} for v in self.t['tags'][1:-1]],key= lambda x:x['prob'][-1]*x['cur'])
		# 	return o['prob'] + [o['prob'][-1]*o['cur']]
		# elif state > 0:
		# 	o =  max([{'prob' : self.tree[state-1][u] if self.tree[state-1].get(u) else self.__viterbi_forward(seq,state-1,u),'cur' : self.__get_transition_param(u,pre_t)*self.__get_emission_param(seq,state,pre_t)} for u in self.t['tags'][1:-1]],key= lambda x:x['prob'])
		# 	self.tree[state][pre_t] = o['prob'] + [o['prob'][-1]*o['cur']]
		# 	return o['prob'] + [o['prob'][-1]*o['cur']]
		# else:
		# 	self.tree[state][pre_t] = [self.__get_transition_param('START',pre_t)*self.__get_emission_param(seq,state,pre_t)]
		# 	return self.tree[state][pre_t]

		###### IMP 3 #######
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

	def __viterbi_backtrack(self,pi,post,seq):
		if len(pi) == 0:
			return []
		vals = [{'p':pi[-1]*self.__get_transition_param(v,post)*self.__get_emission_param(seq,len(seq)-1,v),'v':v} for v in self.t['tags'][1:-1]]
		o = max(vals,key=lambda x:x['p'])
		return self.__viterbi_backtrack(pi[:-1],o['v'],seq[:-1]) + [o['v']]
