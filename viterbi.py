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
			self.tree[state+1]['START'] = 1
			self.__viterbi_forward(seq,state+1)

		elif state < len(seq)-1:
			for v in self.t['tags'][1:-1]:
				vals = [{'prob':self.tree[state][u]*self.__get_transition_param(u,v)*self.__get_emission_param(seq,state+1,v),'tag' : u} for u in self.tree[state]]
				mx = max(vals,key=lambda x:x['prob'])
				self.tree[state+1][v] = mx['prob']

			self.__viterbi_forward(seq,state+1)

		else:
			vals = [{'prob' : self.tree[state][v]*self.__get_transition_param(v,'STOP'),'tag' : v} for v in self.tree[state]]
			mx = max(vals,key=lambda x:x['prob'])
			self.tree[state+1][mx['tag']] = mx['prob']

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
