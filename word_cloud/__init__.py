#!/usr/bin/env python -*- coding: utf-8 -*-

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

try:
    from query_integral_image import query_integral_image as qii
except:
    from util import pythonizing_cython
    pythonizing_cython('query_integral_image')
    from query_integral_image import query_integral_image as qii

def draw_cloud(words, counts, width=1028, height=640, margin=100, 
               font_path='TakaoMincho.ttf', 
               outfilename = "cloud.png",
               ranks_only=False):
    
    # Initialize proxy image values.
    font_sizes, positions= [], []
    integral =  np.zeros((height, width), dtype=np.uint32)
    img_grey = Image.new("L", (width, height))
    draw = ImageDraw.Draw(img_grey)
    
    # intitiallize font size "large enough"
    font_size = height
    
    # start drawing grey image
    for word, count in zip(words,counts):
        # alternative way to set the font size
        if not ranks_only:
            font_size = min(font_size, int(100 * np.log(count + 100)))
        while True:
            # try to find a position
            font = ImageFont.truetype(font_path, font_size)
            
            draw.setfont(font)
            # get size of resulting text
            box_size = draw.textsize(word)
            
            result = qii(integral, box_size[1] + margin,
                                          box_size[0] + margin)
            
            if result is not None or font_size == 0:
                break
            # if we didn't find a place, make font smaller
            font_size -= 1

        if font_size == 0:
            # we were unable to draw any more
            break

        x, y = np.array(result) + margin // 2
        # actually draw the text
        draw.text((y, x), word, fill="white")
        positions.append((x, y))
        font_sizes.append(font_size)
        # recompute integral image
        img_array = np.asarray(img_grey)
        # recompute bottom right
        # the order of the cumsum's is important for speed ?!
        partial_integral = np.cumsum(np.cumsum(img_array[x:, y:], axis=1),
                                     axis=0)
        # paste recomputed part into old image
        # if x or y is zero it is a bit annoying
        if x > 0:
            if y > 0:
                partial_integral += (integral[x - 1, y:]
                                     - integral[x - 1, y - 1])
            else:
                partial_integral += integral[x - 1, y:]
        if y > 0:
            partial_integral += integral[x:, y - 1][:, np.newaxis]

        integral[x:, y:] = partial_integral

    # Redrawing the Image (i.e. the actual drawing of the image)
    img = Image.new("L", (width, height))
    draw = ImageDraw.Draw(img)
    everything = zip(words, font_sizes, positions)
    
    for word, font_size, position in everything:
        font = ImageFont.truetype(font_path, font_size)
        draw.setfont(font)
        
        draw.text((position[1], position[0]), word, fill="white")

    inverted_img = ImageOps.invert(img)
    
    if outfilename:
        inverted_img.save(outfilename)
    else:
        inverted_img.show()
    
