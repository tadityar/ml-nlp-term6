def viterbi(seq,state,t,e,pre_t=None):
	if state == -1:
		return viterbi(seq,state+1,t,e,'START')
	elif state < len(seq):
		return max([viterbi(seq,state+1,t,e,v)*get_transition_param(t,pre_t,v)*get_emission_param(e,seq,state,v) for v in t['tags']])
	else:
		out = get_transition_param(t,pre_t,'STOP')
		return out

def get_transition_param(t,u,v):
	tp = t['map'][t['tags'].index(u)][t['tags'].index(v)]
	return tp


def get_emission_param(e,seq,state,v):
	for i in range(len(e)):
		for key in e[i]:
			if key == list(seq[state].keys())[0]:
				try:
					param = e[i][key][v]
					return param
				except KeyError as e:
					return 0
	return 0
