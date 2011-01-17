#!/bin/env python

import bibparser
from Stemmer import Stemmer
import nltk
import cPickle
import sys
import operator
try:
  import pytools
except:
  pytools = False

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Usage: ./%s [input.bib] [output.dat]"%sys.argv[0]
    exit(127)

  ignore_list = "and a the then we by be et al not of in to with for that on as which these our it an is than this are have at use".split()
  strip_chars = r"""~@.,()[]{}`\/"'=1234567890% """

  bib = bibparser.BibTex(sys.argv[1])
  stem = Stemmer("english")

  wordvector = {}
  if pytools: progress = pytools.ProgressBar("Analysing",len(bib.bib))
  for item in bib.bib:
    if item.has_key("Abstract") and item.has_key("Title"):
      text = nltk.wordpunct_tokenize(item["Abstract"] + " " + item["Title"])
      for word in [x[0] for x in nltk.pos_tag(text) if x[1] in ("NN")]:
        word = stem.stemWord(word.strip(strip_chars).lower())
        if len(word)>1 and word not in ignore_list:
          try:
            wordvector[word] += 1
          except KeyError:
            wordvector[word] = 1
    if pytools: progress.progress()
  sortedwordvector = sorted(wordvector.iteritems(), key=operator.itemgetter(1))

  cPickle.dump(sortedwordvector,open(sys.argv[2],"w+"))
  print "Top 50 words:"
  for word, count in sortedwordvector[-50:]:
    print "%-15s %d"%(word,count)
