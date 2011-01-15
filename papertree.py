#!/bin/env python

import pyarxiv

class Article:
  def __init__(self, arxivid=None):
    if arxivid:
      self.setarxivid(arxivid)

  def setarxivid(self, arxivid):
    self.arxivid = arxivid
    self.fillfeilds()

  def fillfeilds(self):
    self.metadata = pyarxiv.metadata(self.arxivid)
    self.references, extrameta = pyarxiv.references(self.arxivid, self.metadata["bibcode"])
    self.metadata.update(extrameta)
    self.citations,extrameta = pyarxiv.citations(self.arxivid, self.metadata["bibcode"])
    self.metadata.update(extrameta)

  def __str__(self):
    return "arXiv article %s:\n\tmeta: %s\n\trefs: %s\n\tcits: %s"%(self.arxivid, self.metadata, self.references, self.citations)

def dfs(aid,agraph,pgraph,parent=None,max_depth=-1):
  article = Article(aid)
  print "\t"*(5-max_depth),"Found %s"%article.metadata["title"]

  # this quick hack doesn't support unicode so screw foreign 
  # authors :p... so we just "try" and reject entries giving 
  # errors
  try:
    pgraph.add_node(article.metadata["title"])
    agraph.add_node(article.metadata["author"])
    if parent:
      pgraph.add_edge(parent.metadata["title"], article.metadata["title"])
      agraph.add_edge(parent.metadata["author"], article.metadata["author"])
  
    if max_depth == 0:
      return
  
    for i in article.references:
      dfs(i, agraph, pgraph, parent=article, max_depth=max_depth-1)
  except:
    return

if __name__ == "__main__":
  import sys
  import pygraphviz as pgv
  agraph = pgv.AGraph(strict=False, directed=True)
  pgraph = pgv.AGraph(strict=False, directed=False)

  dfs(sys.argv[1], agraph, pgraph, max_depth=5)
  pgraph.write("papers.dot")
  pgraph.layout('dot')
  pgraph.draw("papers.png")
  agraph.write("authors.dot")
  agraph.layout('dot')
  agraph.draw("authors.png")
