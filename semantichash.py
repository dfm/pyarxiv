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
import cPickle
import sys
try:
  import pytools
except:
  pytools = False

if __name__ == "__main__":
  print "Getting global word list"
  bib = btparse.load(sys.argv[1])
  words = [x[0] for x in analysewords.getGlobalWordVector(bib, 256)]

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

  cPickle.dump((NNinput,NNinput_ref,bib),open("NNinput.dat","w+"))
