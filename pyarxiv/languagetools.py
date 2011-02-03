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
# languagetools.py
# 
# Created by Dan F-M on 2011-02-02.
#

import nltk
import re
import numpy as np

# an arbitrary list of words we don't like!
ignore_list = """and a the then we by be et al not of in to with for 
that on as which these our it an is than this are have at use cite""".split()
strip_chars = r"""~@.,()[]{}`\/"'=1234567890% """

def get_nouns(string,relative=True):
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
  if relative:
    return nouns, freq/np.sum(freq)
  return nouns, freq
