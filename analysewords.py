#!/bin/env python
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
import nltk
import cPickle
import sys
import operator
try:
  import pytools
except:
  pytools = False

ignore_list = "and a the then we by be et al not of in to with for that on as which these our it an is than this are have at use".split()
strip_chars = r"""~@.,()[]{}`\/"'=1234567890% """

def getItemWordVector(bibitem, words):
  global ignore_list, strip_chars
  stem = nltk.stem.LancasterStemmer()

  wordLookup = dict(zip(words, range(len(words))))
  wordVector = [0,]*len(words)
  if bibitem.has_key("abstract") and bibitem.has_key("title"):
    text = nltk.wordpunct_tokenize(bibitem["abstract"] + " " + bibitem["title"])
    for word in [x[0] for x in nltk.pos_tag(text) if x[1] in ("NN")]:
      word = stem.stem(word.strip(strip_chars).lower())
      if len(word)>1 and word not in ignore_list:
        try:
          index = wordLookup[word]
          wordVector[index] += 1
        except KeyError:
          pass
  else:
    raise Exception("Not a valid BibTeX Entry")
  return wordVector

def getGlobalWordVector(bibitems, numkeep=0):
  global ignore_list, strip_chars
  stem = nltk.stem.LancasterStemmer()

  wordvector = {}
  if pytools: progress = pytools.ProgressBar("Analysing",len(bibitems))
  for item in bibitems:
    if item.has_key("abstract") and item.has_key("title"):
      text = nltk.wordpunct_tokenize(item["abstract"] + " " + item["title"])
      for word in [x[0] for x in nltk.pos_tag(text) if x[1] in ("NN")]:
        word = stem.stem(word.strip(strip_chars).lower())
        if len(word)>1 and word not in ignore_list:
          try:
            wordvector[word] += 1
          except KeyError:
            wordvector[word] = 1
    if pytools: progress.progress()
  if pytools: print ""
  sortedwordvector = sorted(wordvector.iteritems(), key=operator.itemgetter(1))
  return sortedwordvector[-numkeep:]

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Usage: ./%s input.bib output.dat [numkeep]"%sys.argv[0]
    exit(127)
  elif len(sys.argv) == 4:
    numkeep = int(sys.argv[3])
  else:
    numkeep = 0

  bib = btparse.load(sys.argv[1])
  globalWordVector = getGlobalWordVector(bib, numkeep=numkeep)

  cPickle.dump([x[0] for x in globalWordVector],open(sys.argv[2],"w+"))
  print "Top 50 words:"
  for word, count in globalWordVector[-50:]:
    print "%-15s %d"%(word,count)
