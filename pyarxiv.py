#!/bin/env python

import urllib
import re


import time
def timedec(func):
    def wrapper(*arg,**kw):
        '''source: http://www.daniweb.com/code/snippet368.html'''
        t1 = time.time()
        res = func(*arg,**kw)
        t2 = time.time()
        print "%s took %fs"%(func.func_name, (t2-t1))
        return res
    return wrapper

@timedec
def getarticle_raw(aid):
  url = "http://export.arxiv.org/oai2?verb=GetRecord&identifier=oai:arXiv.org:%s&metadataPrefix=oai_dc"%(aid,)
  retry = True
  while retry:
    data = getdata(url)
    retrytime = re.search("Retry-After:[ ]?(?P<time>[0-9]*)",data)
    if retrytime:
      print "Retry-after signaled by export.arxiv.org.  Signal is: ",retrytime.groupdict()
      sleep(int(retrytime.groupdict()["time"]))
    else:
      retry = False
  return data

def getdata(url):
  return urllib.urlopen(url).read()

@timedec
def metadata(aid):
  data = getarticle_raw(aid)
  metadata = {}
  metadata["arxivid"]      = aid
  metadata["title"]        = oai_parse(data, "title")[0]
  metadata["abstract"]     = oai_parse(data, "description")[0]
  metadata["date"]         = oai_parse(data, "date")[0]
  metadata["topics"]       = oai_parse(data, "subject")
  metadata["arxiv_topics"] = oai_parse(data, "setSpec", prefix = "")
  metadata["authors"]      = oai_parse(data, "creator")
  metadata["author"]       = metadata["authors"][0]
  metadata["bibcode"]      = None
  return metadata

def oai_parse(data, feild, prefix="dc:"):
  result = re.findall("<%s%s>([^<]*?)</%s%s>"%((prefix,feild)*2), data)
  if result:
    return [clean(item) for item in result]
  else:
    return None
  
def clean(string):
  string = string.replace("\n"," ")
  return re.sub(r"[ ]{2,}","",string)

@timedec
def references(aid, bibcode=None):
  refs = [] 
  slacref = references_slac(aid)
  if slacref is not None:
    refs += slacref
  adsref, bibcode = references_ads(aid,bibcode=bibcode)
  if adsref is not None:
    refs += adsref
  # We use the list(set(x)) trick to delete replicate entries
  return list(set(refs)),{"bibcode":bibcode}

@timedec
def citations(aid, bibcode=None):
  cits = [] 
  slaccit = citations_slac(aid)
  if slaccit is not None:
    cits += slaccit
  adscit, bibcode = citations_ads(aid,bibcode=bibcode)
  if adscit is not None:
    cits += adscit
  # We use the list(set(x)) trick to delete replicate entries
  return list(set(cits)),{"bibcode":bibcode}

# Requires:
#   ads  - valid arXiv citation
#   mode - one of, "REFERENCE" or "CITATIONS"
def refs_ads(aid,mode,bibcode=None):
  # First we find the ADS bibcode for the article if it hasn't been given
  if bibcode is None:
    url = "http://adsabs.harvard.edu/cgi-bin/bib_query?arXiv:%s"%aid
    bibcode = re.search("""<input type="hidden" name="bibcode" value="([^"]*)">""",getdata(url)).groups()[0]
  # Now we find the list of items resulted by a MODE search which link to arxiv
  url = "http://adsabs.harvard.edu/cgi-bin/nph-ref_query?bibcode=%s&amp;refs=%s"%(bibcode, mode.upper())
  rawlinks = re.findall("""<a class="oa" href="([^"]*)"[^>]*>X</a>""", getdata(url))
  # Lastly, we loop through the above links and find the redirect in order to find the arXiv citation
  items = []
  for url in rawlinks:
    url = url.replace("&#38;","&")
    fd = urllib.urlopen(url)
    # At this point, fd.url points to "http://arXiv.org/abs/<aid>".  
    # "http://arXiv.org/abs/" is 21 characters long
    items.append(fd.url[21:])
  return items, bibcode

@timedec
def references_ads(aid, bibcode=None):
  return refs_ads(aid, "REFERENCE", bibcode)

@timedec
def citations_ads(aid, bibcode=None):
  return refs_ads(aid, "CITATIONS", bibcode)

def slac_query(aid, mode):
  url = "http://www.slac.stanford.edu/spires/find/hep/www?rawcmd=%s+%s&format=wwwrefslatex"%(mode,aid)
  return getdata(url)

@timedec
def references_slac(aid):
  data = slac_query(aid, "eprint")
  return re.findall("arXiv:([^ \.\]]*)", data)

@timedec
def citations_slac(aid):
  data = slac_query(aid, "c")
  return re.findall("arXiv:([^ \.\]]*)", data)

