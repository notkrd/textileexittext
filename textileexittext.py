'''
Created on Nov 15, 2017

@author: Admin
'''

from PIL import Image, ImageDraw, ImageFont
import random, string, re
import os.path
import textwrap

IMAGE_WIDTH=750
IMAGE_HEIGHT=1000
WHITE_BG=255

HORIZONTAL_CHARACTER_LIMIT = 15
NEWLINE_TOLERANCE = 8
LEFT_MARGIN = 20
VERTICAL_SPACE = 200
TOP_MARGIN = 20
FONT_SIZE = 86

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

IN_PHRASES = "in.txt"
WOULD_PHRASES = "would.txt"
IS_PHRASES = "is.txt"
PREPOSITION_PHRASES = "preposition.txt"
NOUN_PHRASES = "noun_phrase.txt"
VERB_PHRASES = "intransitive_verbs.txt"
SENTENCES = "available_sentences.txt"
PHRASE_FILES = {"IN": IN_PHRASES, "WOULD": WOULD_PHRASES, "IS": IS_PHRASES, 
                "PREPOSITION_PHRASE": PREPOSITION_PHRASES, "NOUN_PHRASE": NOUN_PHRASES, "VERB_PHRASE": VERB_PHRASES,
                "SENTENCE": SENTENCES}

OUTPUT_IMAGE_FILE = "exittext.bmp"

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
fnt = ImageFont.truetype(os.path.join(__location__, FONT_LOCATION), FONT_SIZE)

def txt_lineate(txt_in, character_limit=HORIZONTAL_CHARACTER_LIMIT, tolerance=NEWLINE_TOLERANCE):
    """ Inserts newlines into a string, prioritizing whitespace within NEWLINE_TOLERANCE of every HORIZONTAL_CHARACTER_LIMIT characters. 
    @param txt_in: text to lineate
    @param character_limit: number of max characters per line
    @param tolerance: defunct range over which to break large words
    """
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

def kwarg_substitute(base_str, **kwargs):
    """Updates a template-formatted string with listed replacemens. Probably less efficient than
    template.safe_substitute, however, it takes kwargs 
    @param base_str: the string to update, where $X is the variable X
    @param **kwargs: a list of variables and their substitutions
    Allows failure, like Template.safe_substitute
    """
    return re.sub("\$[\w-]*",lambda s: kwargs[s.group(0)[1:]], base_str)

def fill_template(base_str):
    discourse_vars = get_vars(base_str)
    kwargs = {}
    for a_var in discourse_vars:
        if a_var in PHRASE_FILES:
            kwargs[a_var] = get_rand_response(PHRASE_FILES[a_var])
        else:
            kwargs[a_var] = ""
    return kwarg_substitute(base_str, **kwargs)

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
    return txt_response
    
def get_vars(a_template):
    """ Takes a template string and returns all the variables in it.
    @param a_template: a template formatted string """
    return re.findall("(?<=\$)[\w-]*",a_template)

def stitch_image(text_in="", output_file=OUTPUT_IMAGE_FILE):
    """ Takes a string text_in as a query and outputs a file to output_file with the appropriate response """
    stitch_pattern = Image.new("1", (IMAGE_WIDTH,IMAGE_HEIGHT), WHITE_BG)
    d = ImageDraw.Draw(stitch_pattern)
    the_text = txt_lineate(get_rand_response(pick_pattern(text_in)))
#    textile_metaphr = get_rand_response(THEWEAVE_FILE)
#    embroider_metaphr = get_rand_response(EMBROIDER_FILE)
    d.multiline_text((LEFT_MARGIN,TOP_MARGIN), the_text, font=fnt)
#    d.multiline_text((LEFT_MARGIN,TOP_MARGIN + VERTICAL_SPACE), textile_metaphr, font=fnt)
#    d.multiline_text((LEFT_MARGIN,TOP_MARGIN + 2*VERTICAL_SPACE), embroider_metaphr, font=fnt)
    stitch_pattern.show()
    stitch_pattern.save(os.path.join(__location__, output_file))