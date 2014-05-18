#-*- coding: utf-8 -*-

import sys; reload(sys); sys.setdefaultencoding("utf-8")

import random
from PIL import Image, ImageDraw, ImageFont
from query_integral_image import query_integral_image as qii
import numpy as np
from collections import Counter

query = 'food'
freq_input = Counter({u'\u30d5\u30fc\u30c9': 10, u'\u98df\u3079\u7269': 10, u'\u98df\u6599': 10})

words, counts = map(list, zip(*[i for i in freq_input.items()]))
words.insert(0,'food')
counts.insert(0,max(counts))

width, height = 1028, 640
#width, height = 500, 250
font_path = "TakaoMincho.ttf"
outputfilename = ".tc"
margin = 10

fontsizes, positions= [], []
integral =  np.zeros((height, width), dtype=np.uint32)
img_grey = Image.new('L', (width, height))
draw = ImageDraw.Draw(img_grey)

font_size = max(width,height)

first = True
prev = 0
for word, count in zip(words,counts):
  while True:
    #font_size = font_size*count/sum(counts)
    #font_size = min(font_size, int(100 * np.log(count + 100)))
    
    '''
    if first: first = False; prev = font_size
    elif font_size < 50: font_size = prev_size/2;
    else: font_size = font_size * 2
    '''
    
    #if font_size < 50: font_size = prev_size/2;
    #prev_size = font_size
    
    font = ImageFont.truetype(font_path, font_size)
    draw.setfont(font)
    box_size = draw.textsize(word)
    result = qii(integral, box_size[1] + margin, box_size[0] + margin)
    
    if result is not None or font_size == 0:
      break
    font_size -= 1
    
  if font_size == 0:
    break
  
  x, y = np.array(result) + margin // 2
  print x, y, font_size, word, count
  draw.text((y, x), word, fill="white")
  
  fontsizes.append(font_size); positions.append((x, y))
  
  # recompute integral image
  img_array = np.asarray(img_grey)
  # recompute bottom right
  # the order of the cumsum's is important for speed ?!
  partial_integral = np.cumsum(np.cumsum(img_array[x:, y:], axis=1),axis=0)
  # paste recomputed part into old image
  # if x or y is zero it is a bit annoying
  if x > 0:
    if y > 0:
      partial_integral += (integral[x - 1, y:] - integral[x - 1, y - 1])
    else:
      partial_integral += integral[x - 1, y:]
  if y > 0:
    partial_integral += integral[x:, y - 1][:, np.newaxis]
  integral[x:, y:] = partial_integral

img = Image.new("L", (width, height))
draw = ImageDraw.Draw(img)
everything = zip(words, fontsizes, positions)
for word, font_size, position in everything:
  font = ImageFont.truetype(font_path, font_size)
  draw.setfont(font)
  draw.text((position[1], position[0]), word,
          fill="hsl(%d" % random.randint(0, 255) + ", 80%, 50%)")

#img.show()
