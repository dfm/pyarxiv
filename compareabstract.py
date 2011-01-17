#!/usr/bin/env python
# encoding: utf-8
"""
compareabstract.py

Created by Dan F-M on 2011-01-16.
"""

import bibparser
import sys
import re

import Stemmer

import numpy as np
np.random.seed()

ignore_list = ['and','a','the','then','we','by','be','et','al','not']
strip_chars = '.,(){}`\''

def main():
  stem = Stemmer.Stemmer("english")
  bib = bibparser.BibTex(sys.argv[1])
  aid = 1 #np.random.randint(len(bib.bib))
  while ('Abstract' in bib.bib[aid].keys()) == False:
    aid = np.random.randint(len(bib.bib))
  
  q_vec0 = sorted(bib.bib[aid]['Abstract'].split())
  
  q_vec = []
  q_val  = []
  for w in q_vec0:
    w = stem.stemWord(w.strip(strip_chars).lower())
    if (w in ignore_list) == False \
        and re.search('\\\\',w) == None:
      if (w in q_vec) == False:
        q_vec.append(w)
        q_val.append(1)
      else:
        q_val[-1] += 1
  
  q_val = np.array(q_val)/np.sqrt(np.dot(q_val,q_val))
  prob = np.zeros(len(bib.bib))
  
  for ind,entry in enumerate(bib.bib):
    if ind != aid and ('Abstract' in bib.bib[ind].keys()):
      r_vec = sorted(bib.bib[ind]['Abstract'].split())
      r_val = np.zeros(len(q_val))
      for w in r_vec:
        w = stem.stemWord(w.strip(strip_chars).lower())
        if w in q_vec:
          r_val[q_vec.index(w)] += 1
      mod = np.dot(r_val,r_val)
      if mod > 0:
        prob[ind] = np.dot(r_val/np.sqrt(mod),q_val)
  
  # sort based on probability (best first)
  inds_sort = np.argsort(prob)[::-1]
  
  print 'Similar papers to:\n\t%s\n\t\tby: %s\n'%(bib.bib[aid]['Title'],bib.bib[aid]['Author'])
  for i in range(10):
    best = inds_sort[i]
    print '%3d.\t%s\n\t\tby: %s\n\t\tid = %3d, prob = %f\n'%(i+1,bib.bib[best]['Title'],bib.bib[best]['Author'],best,prob[best])

if __name__ == '__main__':
  main()

