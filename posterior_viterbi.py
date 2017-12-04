from forward_backward import ForwardBackward

class PosteriorViterbi:
	def __init__(self,t,e):
		self.t = t
		self.e = e
		self.fb = ForwardBackward(t,e)
		self.posterior = []

	def assign(self,seq):
		self.tree = [{} for i in range(len(seq)+1)]
		self.fb.assign(seq)
		states = self.fb.states

		self.__compute_posterior(states)
		self.__viterbi_forward(seq,-1)
		return self.__viterbi_backtrack(len(seq),seq)

	def __compute_posterior(self,states):
		p_o_m = sum([states[-1][v]['alpha']*self.__get_transition_param(v,'STOP') for v in states[-1]])

		self.posterior = [{v: (states[i][v]['alpha']*states[i][v]['beta'])/p_o_m for v in states[i]} for i in range(len(states))]

	def __viterbi_forward(self,seq,state):
		if state == -1:
			self.tree[state+1]['START'] = 1
			self.__viterbi_forward(seq,state+1)
		elif state < len(seq):
			for v in self.t['tags'][1:-1]:
				vals = [self.tree[state][u]*self.__is_viable_path(u,v)*self.posterior[state][v] for u in self.tree[state]]
				self.tree[state+1][v] = max(vals)

			self.__viterbi_forward(seq,state+1)
		else:
			vals = [self.tree[state][v]*self.__is_viable_path(v,'STOP') for v in self.tree[state]]
			mx = max(vals)

	def __viterbi_backtrack(self,state,seq,y=None):
		if state == len(seq):
			vals = [{'prob' : self.tree[state][v]*self.__is_viable_path(v,'STOP'),'tag':v} for v in self.tree[state]]
			mx = max(vals,key=lambda x:x['prob'])
			return self.__viterbi_backtrack(state-1,seq,y=mx['tag']) + [mx['tag']]
		elif state > 0:
			vals = [{'prob' : self.tree[state][u]*self.__is_viable_path(u,y),'tag':u} for u in self.tree[state]]
			mx = max(vals,key=lambda x:x['prob'])
			return self.__viterbi_backtrack(state-1,seq,y=mx['tag']) + [mx['tag']]
		else:
			return []

	def __get_transition_param(self,u,v):
		return self.t['map'][v][u]
		# return self.t['map'][self.t['tags'].index(u)][self.t['tags'].index(v)]

	def __is_viable_path(self,u,v):
		return 0 if self.t['map'][v][u] == 0 else 1

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