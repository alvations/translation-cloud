#!/usr/bin/env python -*- coding: utf-8 -*-

import codecs, os, random
import sys; reload(sys); sys.setdefaultencoding("utf-8")
from collections import Counter, defaultdict
from itertools import chain
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from query_integral_image import query_integral_image as qii
import galechurch 

def sentence_matches(srcfile, trgfile, query, max=10000):
  """" Find sentences pairs that contain query"""
  for sentpair in galechurch.align(srcfile, trgfile):
    if query in sentpair.split('\t')[0].lower().split():
      yield sentpair

def count_freq(sentences, translations):
  """ Return src:trgs frequencies as Counter(). """
  return Counter(filter(None, list(chain(*[[j for j in translations \
                                   if j in i.split()] for i in sentences]))))
  
def corpus2translationcounts(src_corpus, trg_corpus, \
                             query_word, translations=None):
  """ Counts the frequencies of translation of the query word. """
  matches = sentence_matches(src_corpus, trg_corpus, query_word)
  return count_freq(matches, translations)

def draw_cloud(words, counts, width=1028, height=640, margin=10,
               font_path="TakaoMincho.ttf", firstcentre=True, printcount=True,
               ):
  """ Takes a sorted words and counts list and saves a the tcloud. """
  if printcount: # If users wants to print counts.
    words = [i+"("+str(j)+")" for i,j in zip(words, counts)]
  outputfilename = words[0]+".jpg"
  
  # Initialize proxy image values.
  fontsizes, positions= [], []
  integral =  np.zeros((height, width), dtype=np.uint32)
  img_grey = Image.new('L', (width, height))
  draw = ImageDraw.Draw(img_grey)
  
  # Calculates fontsizes and positions of words.
  for word, count in zip(words,counts):
    font_size =  int(count / float(sum(counts)) * 100) * height / 100
    if printcount:
      font_size = font_size * min(width, height) / max(width,height)
    
    while True:
      # Calculates appropriate fontsize of a word.
      font = ImageFont.truetype(font_path, font_size)
      # Calculates how much space the word will take.
      draw.setfont(font)
      box_size = draw.textsize(word)
      
      if firstcentre: # If you want the first item to be centered. 
        result = (height/4, width/4)
        firstcentre = False
      else: # Else use integral image to calculate the position.
        result = qii(integral, box_size[1] + margin, box_size[0] + margin)
      ##print font_size, result
      
      if result is not None or font_size <= 0:
        break
      font_size-=1
    
    if printcount and font_size < 50:
      font_size = 50 
      
    
    # Saves the positions.
    x, y = np.array(result) + margin // 2
    draw.text((y, x), word, fill="white")
    fontsizes.append(font_size) 
    positions.append((x, y))
    
    # Recompute integral image (so that the words don't overlap)
    img_array = np.asarray(img_grey)
    # Recompute bottom right
    partial_integral = np.cumsum(np.cumsum(img_array[x:, y:], axis=1),axis=0)
    # paste recomputed part into old image222
    # if x or y is zero it is a bit annoying
    if x > 0:
      if y > 0:
        partial_integral += (integral[x - 1, y:] - integral[x - 1, y - 1])
      else:
        partial_integral += integral[x - 1, y:]
    if y > 0:
      partial_integral += integral[x:, y - 1][:, np.newaxis]
    integral[x:, y:] = partial_integral
  
  # Redrawing the Image (i.e. the actual drawing of the image)
  img = Image.new("L", (width, height))
  draw = ImageDraw.Draw(img)
  everything = zip(words, fontsizes, positions)
  
  for word, font_size, position in everything:
    font = ImageFont.truetype(font_path, font_size)
    draw.setfont(font)
    #draw.text((position[1], position[0]), word,
    #        fill="hsl(%d" %  + ", 80%, 50%)")
    draw.text((position[1], position[0]), word, fill="white")

  inverted_img = ImageOps.invert(img)
  inverted_img.show()
##endfunc draw_cloud()


def main(corpusx, corpusy, query):
  if os.path.exists(query):
    with codecs.open(query, 'r', 'utf8') as fin:
      source, _, targets = fin.read().strip().partition(',')
      targets = targets.split(',')
      freq_input = corpus2translationcounts(corpusx, corpusy, source, targets)
      words, counts = map(list, zip(*[i for i in freq_input.most_common()]))
      words.insert(0,source)
      counts.insert(0,max(counts))
      draw_cloud(words, counts, firstcentre=True, printcount=False)

if __name__ == '__main__':
  import sys
  if len(sys.argv) not in range(3,6):
    sys.stderr.write('Usage: python %s src_corpus trg_corpus ' 
                     '(wordlist.txt | src_word)' % sys.argv[0])
    sys.exit(1)
  main(*sys.argv[1:])
