#!/usr/bin/env python
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
# parse.py
# 
# Created by Dan F-M on 2011-02-02.
#

"""
This script parses the abstracts and titles in a bibtex document and 
returns all the nouns and their relative frequencies
"""

import sys
import pickle
import re
import numpy as np

import btparse
import nltk

try:
  import pytools
except:
  pytools = False


# bib = btparse.load(sys.argv[1])

# an arbitrary list of words we don't like!
ignore_list = """and a the then we by be et al not of in to with for 
that on as which these our it an is than this are have at use cite""".split()
strip_chars = r"""~@.,()[]{}`\/"'=1234567890% """

class BibTexLibrary:
  def __init__(self,path):
    """'path' can point to either a pickle file or a .bib file"""
    try:
      # we'll see if it's a pickle file?
      self.nouns,self.freq = pickle.load(open(path,'rb'))
    except:
      self.bib = btparse.load(path)
      
      # tokenize the library
      self.nouns = []
      self.freq  = []
      if pytools:
        progress = pytools.ProgressBar("Analysing",len(self.bib))
        progress.draw()
      else:
        print 'Tokenizing library... this may take some time...'
      for ind,entry in enumerate(self.bib):
        if ('abstract' in self.bib[ind].keys()) and ('title' in self.bib[ind].keys()):
          tokens,freq = self.get_nouns(self.bib[ind]['abstract']+" "+self.bib[ind]['title'])
          for i,w in enumerate(tokens):
            try:
              self.freq[self.nouns.index(w)] += freq[i]
            except:
              self.nouns.append(w)
              self.freq.append(freq[i])
        
        if pytools: progress.progress()
        else: print '%.1f \%'%(float(ind)/len(self.bib))
      
      
  def save(self,path):
    """save to a file"""
    pickle.dump((self.nouns,self.freq),open(path,'wb'),-1)
  
  def get_nouns(self,string):
    """
    Return a sorted list of the nouns in 'string' and their relative frequency
    """
    
    # tokenize the word
    raw_tokens = nltk.wordpunct_tokenize(string)
    
    # clean it up!
    stem = nltk.stem.LancasterStemmer()
    cleanword = lambda w : stem.stem(w.strip(strip_chars).lower())
    
    # sort and return only the nouns
    tokens = sorted([cleanword(x[0]) for x in nltk.pos_tag(raw_tokens) if x[1][:2] in ("NN")])
    
    # count the frequencies of each word
    nouns = []
    freq  = []
    for w in tokens:
      if len(w)>2 and w not in ignore_list and re.search('\\\\',w) == None:
        if (w in nouns) == False:
          nouns.append(w)
          freq.append(1)
        else:
          # we assume that since we have a sorted list of words,
          # the last one that we added is the same as this one.
          freq[-1] += 1
    freq = np.array(freq,dtype=float)
    return nouns, freq/np.sum(freq)


