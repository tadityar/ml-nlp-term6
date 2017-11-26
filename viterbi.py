def viterbi(m):
	if len(m) == 1:
		return viterbi(m+1)
	else if len(m) <= n:
		return max([viterbi(m,u) for u in states])
	else:
		return max([m[u] for u in states])