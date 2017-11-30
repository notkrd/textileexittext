'''
Created on Nov 15, 2017

@author: Admin
'''

from PIL import Image, ImageDraw, ImageFont
import nltk
import random
import os.path

HORIZONTAL_CHARACTER_LIMIT = 40
NEWLINE_TOLERANCE = 12
LEFT_MARGIN = 40
VERTICAL_SPACE = 200
TOP_MARGIN = 100
FONT_SIZE = 48
FONT_FACE = 'VT323-Regular.ttf'
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
fnt = ImageFont.truetype(os.path.join(__location__, FONT_FACE), FONT_SIZE)

def txt_lineate(txt_in):
    txt_out = txt_in
    for i in range(1, 1 + len(txt_in) // HORIZONTAL_CHARACTER_LIMIT):
        for j in range(i * (HORIZONTAL_CHARACTER_LIMIT + 1) - 1, i * (HORIZONTAL_CHARACTER_LIMIT + 1) - 1 + NEWLINE_TOLERANCE):
            if j >= len(txt_out):
                return txt_out
            if j == i * (HORIZONTAL_CHARACTER_LIMIT + 1) - 1 + NEWLINE_TOLERANCE:
                newline_index = j+1
                break
            if txt_out[j] == " ":
                newline_index = j+1
                break
        txt_out = txt_out[:newline_index] + "\n" + txt_out[newline_index:]
    return txt_out
    
def get_rand_response(from_file):
    threadof_metaphors = open(os.path.join(__location__, from_file),"r")
    possible_lines = threadof_metaphors.readlines()
    txt_response = str(random.choice(possible_lines)).rstrip()
    txt_response = txt_lineate(txt_response)
    return txt_response
    

def stitch_image(text_in):
    stitch_pattern = Image.new("1", (1094,768), 255)
    d = ImageDraw.Draw(stitch_pattern)
    thread_metaphr = get_rand_response('threadof_metaphors.txt')
    textile_metaphr = get_rand_response('theweave_metaphors.txt')
    embroider_metaphr = get_rand_response('embroider_metaphors.txt')
    d.multiline_text((LEFT_MARGIN,TOP_MARGIN), thread_metaphr, font=fnt)
    d.multiline_text((LEFT_MARGIN,TOP_MARGIN + VERTICAL_SPACE), textile_metaphr, font=fnt)
    d.multiline_text((LEFT_MARGIN,TOP_MARGIN + 2*VERTICAL_SPACE), embroider_metaphr, font=fnt)
    stitch_pattern.show()