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

import btparse
import analysewords
import mdp
from CPRBMNode import CPRBMNode
import numpy as np

import cPickle
import sys
from os import path
try:
  import pytools
except:
  pytools = False

import pylab

def pretrain(rbms, NNinput, i=0, sample=None):
  if sample is None:
    def sample():
      return np.random.permutation(NNinput)[:int(NNinput.shape[0]/4)]

  learning = True
  lasterror = None
  c = 0
  while learning or c < 50:  #fine tuning on c? read through old notes on issue
    rbms[i].train(sample(), decay=0.01)
    if lasterror is not None:
      if lasterror - rbms[i]._train_err < 0:
        learning = False
    lasterror = rbms[i]._train_err
    print lasterror
    c += 1
  if i < len(rbms)-1:
    pretrain(rbms, NNinput, i+1, lambda : rbms[i].sample_h(sample())[1])



if __name__ == "__main__":
  #######CONFIG#########
  wvec_length = 512
  rbm_config = (512,256,128,64)
  ######################
  assert(wvec_length == rbm_config[0])

  if not path.isfile("NNinput.dat"):
    print "Getting global word list"
    bib = btparse.load(sys.argv[1])
    words = [x[0] for x in analysewords.getGlobalWordVector(bib, 512)]
  
    NNinput = []
    NNinput_ref = {}
    print "Getting individual word vectors"
    if pytools: progress = pytools.ProgressBar("Analysing",len(bib))
    for i, item in enumerate(bib):
      try:
        NNinput.append(analysewords.getItemWordVector(item, words))
        NNinput_ref[len(NNinput)-1] = i
      except:
        pass
      if pytools: progress.progress()
    if pytools: print ""
    NNinput = np.array(NNinput, dtype='float32')
  
    print "Saving NN input"
    cPickle.dump((NNinput,NNinput_ref,bib),open("NNinput.dat","w+"))
  else:
    print "Reloading previous NN input"
    NNinput, NNinput_ref, bib = cPickle.load(file("NNinput.dat"))

  print "Creating Restricted Boltzmann Machines"
  rbms = []
  for i in range(len(rbm_config)-1):
    if i == 0:
      nodetype = CPRBMNode
    else:
      nodetype = mdp.nodes.RBMNode
    rbms.append( nodetype(visible_dim = rbm_config[i  ], 
                           hidden_dim = rbm_config[i+1]))

  print "Starting pretraining"
  pretrain(rbms, NNinput)

