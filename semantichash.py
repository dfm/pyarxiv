#!/bin/env python
# encoding: utf-8

import bibparser
import analysewords
import cPickle
import sys
try:
  import pytools
except:
  pytools = False

if __name__ == "__main__":
  print "Getting global word list"
  bib = bibparser.BibTex(sys.argv[1]).bib
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
