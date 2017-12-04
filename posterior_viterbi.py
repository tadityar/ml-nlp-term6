from forward_backward import FowardBackward

class PosteriorViterbi:
	def __init__(self,t,e):
		self.t = t
		self.e = e
		self.fb = FowardBackward(f,b)
		self.posterior = []

	def assign(self,seq):
		self.fb.assign(seq)
		states = self.fb.states

	def __compute_posterior(self,states):
		pass