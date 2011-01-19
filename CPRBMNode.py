#!/bin/env python

from mdp.nodes import RBMNode
from math import factorial

from numpy import vectorize, zeros, newaxis
from mdp.utils import mult
from mdp import numx, numx_rand

exp        = numx.exp
log        = numx.log
random     = numx_rand.random
vfactorial = vectorize(lambda x: factorial(x))

class CPRBMNode(RBMNode):
  """
  Constrained poisson RBM.  Uses a poisson distribution for modeling visible word counts
  and the standard conditional Bernoulli distribution for modeling hidden features.  As such,
    P(v=n|h) = Ps(
  """

  _Ps = lambda self, n, l : exp(-l) * (l**n) / vfactorial(n)

  def _train(self, v, n_updates=1, epsilon=0.1, decay=0., momentum=0., verbose=False):
    """
    Overloading the train function here is simply a hack in order to put the visible
    data into the class properties, self.v.
    We do this in order to gain access to this variable in _sample_v(h) without changing
    the input parameters.  In this way, we are able to keep backwards compatibility with
    RBMNode
    """
    self.v = v
    super(CPRBMNode, self)._train(v, n_updates, epsilon, decay, momentum, verbose)
  
  def _sample_v(self, h):
    # returns  P(v=n|h,W,b) and a sample from it

    # un-normalized poisson rate, l
    l = exp(self.bv + mult(h, self.w.T))
    # now we normalize it wrt length of wordvector and partition function
    l = l * self.v.sum(axis=1)[:,newaxis] / l.sum(axis=1)[:,newaxis]       

    probs = self._Ps(self.v, l)
    v = (probs > random(probs.shape)).astype(self.dtype)
    return probs, v

  def _energy(self, v, h):
    return (-mult(v, self.bv) - mult(h, self.bh) +
             (-mult(v, self.w)*h + log(factorial(v))).sum(axis=1))
