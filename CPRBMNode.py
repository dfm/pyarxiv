#!/bin/env python
# encoding: utf-8
#
# Copyright 2011 Daniel Foreman-Mackey and Michael Gorelick
# 
# This is part of pyarxiv.
# 
# pyarxiv is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
# 
# pyarxiv is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pyarxiv.  If not, see <http://www.gnu.org/licenses/>.
#

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
    P(v_i=n|h) = Ps(v, exp(bv_i + Sum_j(h_j*w_ij)) * N/Z)
    N = Sum_i(v_i)
    Z = Sum_k(exp(bv_k + Sum_j(h_j*w_kj))

  with resulting energy,
    E(v,h) = -Sum_i(bv_i*v_i) + Sum_i(log(v_i!)) - Sum_j(bh_j*h_j) - Sum_ij(v_i*h_j*w_ij)
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
