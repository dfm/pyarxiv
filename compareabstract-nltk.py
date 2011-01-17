#!/usr/bin/env python
# encoding: utf-8
"""
compareabstract.py

Created by Dan F-M on 2011-01-16.
"""

# import bibparser
import btparse
import sys
import re

import Stemmer
import nltk

import numpy as np
np.random.seed()

ignore_list = "and a the then we by be et al not of in to with for that on as which these our it an is than this are have at use".split()
strip_chars = r"""~@.,()[]{}`\/"'=1234567890% """

def main():
  stem = Stemmer.Stemmer("english")
  # bib = bibparser.BibTex(sys.argv[1])
  bib = btparse.load(sys.argv[1])
  aid = 1#np.random.randint(len(bib))
  while ('abstract' in bib[aid].keys()) == False:
    aid = np.random.randint(len(bib))
  
  abstract = nltk.wordpunct_tokenize(bib[aid]['abstract'])
  q_vec0 = sorted([x[0] for x in nltk.pos_tag(abstract) if x[1] in ("NN")])
  
  q_vec = []
  q_val  = []
  for w in q_vec0:
    w = stem.stemWord(w.strip(strip_chars).lower())
    if len(w)>2 and w not in ignore_list and re.search('\\\\',w) == None:
      if (w in q_vec) == False:
        q_vec.append(w)
        q_val.append(1)
      else:
        q_val[-1] += 1
  
  q_val = np.array(q_val)/np.sqrt(np.dot(q_val,q_val))
  prob = np.zeros(len(bib))
  
  for ind,entry in enumerate(bib):
    if ind != aid and ('abstract' in bib[ind].keys()):
      abstract = nltk.wordpunct_tokenize(bib[ind]['abstract'])
      r_vec = sorted([x[0] for x in nltk.pos_tag(abstract) if x[1] in ("NN")])
      r_val = np.zeros(len(q_val))
      for w in r_vec:
        #w = stem.stemWord(w.strip(strip_chars).lower())
        w = w.strip(strip_chars).lower()
        if w in q_vec:
          r_val[q_vec.index(w)] += 1
      mod = np.dot(r_val,r_val)
      if mod > 0:
        prob[ind] = np.dot(r_val/np.sqrt(mod),q_val)
  
  # sort based on probability (best first)
  inds_sort = np.argsort(prob)[::-1]
  
  print 'Similar papers to:\n\t%s\n\t\tby: %s\n'%(bib[aid]['title'],bib[aid]['author'])
  for i in range(10):
    best = inds_sort[i]
    print '%3d.\t%s\n\t\tby: %s\n\t\tid = %3d, prob = %f\n'%(i+1,bib[best]['title'],bib[best]['author'],best,prob[best])

if __name__ == '__main__':
  main()

