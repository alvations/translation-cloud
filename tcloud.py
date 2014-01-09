#!/usr/bin/env python -*- coding: utf-8 -*-
import sys; reload(sys); sys.setdefaultencoding("utf-8")

import galechurch
import codecs, os
from collections import Counter, defaultdict
from itertools import chain

def sentence_matches(srcfile, trgfile, query, max=10000):
  for count, sentpair in enumerate(galechurch.align(sfile, tfile)):
    if query in sentpair.split('\t')[0].lower().split():
      yield sentpair

def count_freq(sentences, translations):
  return Counter(filter(None, list(chain(*[[j for j in translations \
                                   if j in i.split()] for i in sentences]))))
  
def corpus2translationcounts(src_corpus, trg_corpus, \
                             query_word, translations=None):
  matches = sentence_matches(src_corpus, trg_corpus, query_word)
  if translations==None:
    
  
  return count_freq(matches, translations)
  

sfile, tfile = 'galechurch/ntumc.eng', 'galechurch/ntumc.jpn'
source = u'food'
target = [u'フード', u'食物', u'食べ物', u'食料']
