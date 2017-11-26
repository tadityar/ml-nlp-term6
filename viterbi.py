def viterbi(seq,state,t,e,pre_t=None):
	if state == -1:
		return viterbi(seq,state+1,t,e,'START')
	elif state < len(seq):
		return max([viterbi(seq,state+1,t,e,v)*get_transition_param(t,pre_t,v)*get_emission_param(e,seq,state,v) for v in t['tags']])
	else:
		return get_transition_param(t,pre_t,'STOP')

def get_transition_param(t,u,v):
	return t['map'][t['tags'].index(u)][t['tags'].index(v)]

def get_emission_param(e,seq,state,v):
	for i in range(len(e)):
		for key in e[i]:
			if key in list(seq[state].keys())[0]:
				try:
					return e[i][key][v]
				except KeyError as e:
					return 0
	return 0