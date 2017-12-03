class ForwardBackward:

	def __init__(self,t,e):
		self.t = t
		self.e = e
		self.states = []

	def __create_params(self,seq):
		self.states = [{u : {'alpha' : None, 'beta' : None} for u in self.t['tags'][1:-1]} for j in range(len(seq))]

		for j in range(len(self.states)):
			for u in self.states[j]:
				if self.states[j][u]['alpha'] is None:
					self.states[j][u]['alpha'] = self.__alpha_calc(seq,j,u)
				if self.states[j][u]['beta'] is None:
					self.states[j][u]['beta'] = self.__beta_calc(seq,j,u)

		return self.states

	def __compute_max(self,seq,states):
		return [max([{'p': states[i][v]['alpha']*states[i][v]['beta'],'tag':v} for v in self.t['tags'][1:-1]],key=lambda x:x['p'])['tag'] for i in range(len(seq))]

	def assign(self,seq):
		return self.__compute_max(seq,self.__create_params(seq))

	def __alpha_calc(self,seq,j,u):
		if j == 0:
			return self.__get_transition_param('START',u)
		else:
			self.states[j][u]['alpha'] = sum([(self.states[j-1][v]['alpha'] if self.states[j-1][v]['alpha'] is not None else self.__alpha_calc(seq,j-1,v))*self.__get_transition_param(v,u)*self.__get_emission_param(seq,j-1,v) for v in self.t['tags'][1:-1]])
			return self.states[j][u]['alpha']

	def __beta_calc(self,seq,j,u):
		if j == len(seq)-1:
			return self.__get_transition_param(u,'STOP')*self.__get_emission_param(seq,j,u)
		else:
			self.states[j][u]['beta'] = sum([(self.states[j+1][v]['beta'] if self.states[j+1][v]['beta'] is not None else self.__beta_calc(seq,j+1,v))*self.__get_transition_param(u,v)*self.__get_emission_param(seq,j,u) for v in self.t['tags'][1:-1]]) 
			return self.states[j][u]['beta']

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