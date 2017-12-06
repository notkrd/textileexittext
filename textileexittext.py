'''
Created on Nov 15, 2017

@author: Admin
'''

from PIL import Image, ImageDraw, ImageFont
import random, string, re
import os.path
import textwrap

IMAGE_WIDTH=1024
IMAGE_HEIGHT=768
WHITE_BG=255

HORIZONTAL_CHARACTER_LIMIT = 25
NEWLINE_TOLERANCE = 8
LEFT_MARGIN = 40
VERTICAL_SPACE = 200
TOP_MARGIN = 100
FONT_SIZE = 72

FONT_LOCATION = 'Raleway-ExtraBold.ttf'
THREADOF_FILE = "threadof_metaphors.txt"
THEWEAVE_FILE = 'theweave_metaphors.txt'
EMBROIDER_FILE = 'embroider_metaphors.txt'
PINSANDNEEDLES_FILE = "pinsandneedles_metaphors.txt"
TEXTILE_FILE = "textile_metaphors.txt"
METAPHOR_FILES = [THREADOF_FILE, THEWEAVE_FILE, EMBROIDER_FILE, PINSANDNEEDLES_FILE, TEXTILE_FILE]
THEWEAVE_TEMPLATES = "theweave_templates.txt"
THREADOF_TEMPLATES = "threadof_templates.txt"
TEMPLATE_FILES = [THEWEAVE_TEMPLATES, THREADOF_TEMPLATES]
OUTPUT_IMAGE_FILE = "exittext.bmp"

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
fnt = ImageFont.truetype(os.path.join(__location__, FONT_LOCATION), FONT_SIZE)

def txt_lineate(txt_in, character_limit=HORIZONTAL_CHARACTER_LIMIT, tolerance=NEWLINE_TOLERANCE):
    """ Inserts newlines into a string, prioritizing whitespace within NEWLINE_TOLERANCE of every HORIZONTAL_CHARACTER_LIMIT characters. """
    """txt_out = txt_in
    for i in range(1, 1 + len(txt_in) // character_limit):
        for j in range(i * (character_limit + 1) - 1, i * (character_limit + 1) - 1 + tolerance):
            if j >= len(txt_out):
                return txt_out
            if j == i * (character_limit + 1) - 1 + tolerance:
                newline_index = j+1
                break
            if txt_out[j] == " ":
                newline_index = j+1
                break
        txt_out = txt_out[:newline_index] + "\n" + txt_out[newline_index:]
    return txt_out"""
    return "\n".join(textwrap.wrap(txt_in, character_limit))

def pick_pattern(trigger_str=""):
    """ Takes a string and returns an appropriate corpus filename """
    if trigger_str == "thread":
        return THREADOF_FILE
    return random.choice([THREADOF_FILE, TEXTILE_FILE, EMBROIDER_FILE, PINSANDNEEDLES_FILE, THEWEAVE_FILE])
    
def get_rand_response(from_file):
    """ Simply picks a random line from a given file. """
    metaphors_str = open(os.path.join(__location__, from_file),"r")
    possible_lines = [x for x in metaphors_str.readlines() if x != ""]
    txt_response = str(random.choice(possible_lines)).rstrip(string.punctuation+string.whitespace)
    txt_response = txt_lineate(txt_response)
    return txt_response
    
def get_vars(a_template):
    """ Takes a template string and returns all the variables in it """
    return re.findall("(?<=\$)[\w-]*",a_template)

def stitch_image(text_in="", output_file=OUTPUT_IMAGE_FILE):
    """ Takes a string text_in as a query and outputs a file to output_file with the appropriate response """
    stitch_pattern = Image.new("1", (IMAGE_WIDTH,IMAGE_HEIGHT), WHITE_BG)
    d = ImageDraw.Draw(stitch_pattern)
    the_text = get_rand_response(pick_pattern(text_in))
#    textile_metaphr = get_rand_response(THEWEAVE_FILE)
#    embroider_metaphr = get_rand_response(EMBROIDER_FILE)
    d.multiline_text((LEFT_MARGIN,TOP_MARGIN), the_text, font=fnt)
#    d.multiline_text((LEFT_MARGIN,TOP_MARGIN + VERTICAL_SPACE), textile_metaphr, font=fnt)
#    d.multiline_text((LEFT_MARGIN,TOP_MARGIN + 2*VERTICAL_SPACE), embroider_metaphr, font=fnt)
    stitch_pattern.show()
    stitch_pattern.save(os.path.join(__location__, output_file))