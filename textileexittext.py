'''
Created on Nov 15, 2017

@author: Admin
'''

from PIL import Image, ImageDraw, ImageFont
import random, string, re
import os.path
import textwrap

PERFORMING = True

IMAGE_WIDTH= 600
IMAGE_HEIGHT=800
WHITE_BG=255

HORIZONTAL_CHARACTER_LIMIT = 12
NEWLINE_TOLERANCE = 8
LEFT_MARGIN = 10
VERTICAL_SPACE = 200
TOP_MARGIN = 10
FONT_SIZE = 108

RALEWAY_EB = "fonts/Raleway-ExtraBold.ttf"
JULIUS_REGULAR = "fonts/JuliusSansOne-Regular.ttf"
RALEWAY_MED = "fonts/Raleway-Medium.ttf"
GEO_REG = "fonts/Geo-Regular.ttf"
ROBOTO_MED = "fonts/Roboto-Medium.ttf"
SPECTRAL_SB = "fonts/SpectralSC-SemiBold.ttf"
TEKO_SB = "fonts/Teko-SemiBold.ttf"
FONT_LOCATION = GEO_REG

THREADOF_FILE = "corpus/threadof_metaphors.txt"
THEWEAVE_FILE = "corpus/theweave_metaphors.txt"
EMBROIDER_FILE = "corpus/embroider_metaphors.txt"
PINSANDNEEDLES_FILE = "corpus/pinsandneedles_metaphors.txt"
TEXTILE_FILE = "corpus/textile_metaphors.txt"
METAPHOR_FILES = [THREADOF_FILE, THEWEAVE_FILE, EMBROIDER_FILE, PINSANDNEEDLES_FILE, TEXTILE_FILE]

THEWEAVE_TEMPLATES = "corpus/theweave_templates.txt"
THREADOF_TEMPLATES = "corpus/threadof_templates.txt"
MISC_TEMPLATES = "corpus/assorted_templates.txt"
EMBROIDER_TEMPLATES = "corpus/embroidery_templates.txt"
TEXTILE_TEMPLATES = "corpus/textile_templates.txt"
TEMPLATE_FILES = {"weave": THEWEAVE_TEMPLATES, "thread": THREADOF_TEMPLATES, "embroider": EMBROIDER_TEMPLATES, "textile": TEXTILE_TEMPLATES,
                  "MISC": MISC_TEMPLATES}

IN_PHRASES = "corpus/in.txt"
WOULD_PHRASES = "corpus/would.txt"
IS_PHRASES = "corpus/is.txt"
PREPOSITION_PHRASES = "corpus/preposition.txt"
NOUN_PHRASES = "corpus/noun_phrase.txt"
VERB_PHRASES = "corpus/intransitive_verbs.txt"
SENTENCES = "corpus/available_sentences.txt"
ADJECTIVES = "corpus/available_sentences.txt"
LOCATIONS = "corpus/locations.txt"
PHRASE_FILES = {"IN": IN_PHRASES, "WOULD": WOULD_PHRASES, "IS": IS_PHRASES, 
                "PREPOSITION_PHRASE": PREPOSITION_PHRASES, "NOUN_PHRASE": NOUN_PHRASES, "VERB_PHRASE": VERB_PHRASES,
                "ADJECTIVE": ADJECTIVES, "LOCATION": LOCATIONS,
                "SENTENCE": SENTENCES}

OUTPUT_IMAGE_FILE = "exittext.bmp"

WORD_RE = re.compile("\w*")
TO_STRIP = string.punctuation + string.whitespace

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
fnt = ImageFont.truetype(os.path.join(__location__, FONT_LOCATION), FONT_SIZE)

INSIGNIFICANT_WORDS = set(["the","of","to", "and", "a", "in", "is", "it", "you", "that", "was", "for", "on", "are", "with", "as", "I", "his", "they", "be", "at", "one", "have", "this", "from", "or", "had", "by", "hot", "word", "but", "what", "some", "can", "out", "other", "were", "all", "there", "when", "up", "use", "your", "how", "said", "an", "each"])

all_possible_lines = []
for a_collection in METAPHOR_FILES:
    file_reader = open(os.path.join(__location__, a_collection),"r")
    all_possible_lines += file_reader.readlines()
    file_reader.close()

def pick_similar_line(line_in):
    random.shuffle(all_possible_lines)
    words_in = set(line_in.split()).difference(INSIGNIFICANT_WORDS)
    curr_best = -1
    best_line = ""
    for a_line in all_possible_lines:
        if len(words_in & set(a_line.split())) > curr_best:
            best_line = a_line.strip(TO_STRIP)
            curr_best = len(words_in & set(a_line.split()))
    return best_line

def txt_lineate(txt_in, character_limit=HORIZONTAL_CHARACTER_LIMIT, tolerance=NEWLINE_TOLERANCE):
    """ Inserts newlines into a string, to fit the image. 
    @param txt_in: text to lineate
    @param character_limit: number of max characters per line
    @param tolerance: defunct range over which to break large words
    """
    return "\n".join(textwrap.wrap(txt_in, character_limit))

def kwarg_substitute(base_str, **kwargs):
    """Updates a template-formatted string with listed replacemens. Probably less efficient than
    template.safe_substitute, however, it takes kwargs 
    @param base_str: the string to update, where $X is the variable X
    @param **kwargs: a list of variables and their substitutions
    Allows failure, like Template.safe_substitute
    """
    def substitute(s):
        if s in kwargs:
            return kwargs[s]
        else:
            return s.lower()
    return re.sub("\$([\w-]*)", lambda s: substitute(s.group(0)[1:].strip(TO_STRIP)), base_str)

def fill_template(base_str, madlibs_phrases={}, phrase_source_files = PHRASE_FILES):
    """ Replace variables with terms in a template-formatted ($VAR) string 
    @param base_str: The string in template format
    @param madlibs_phrases: a dict of priority string substitutions
    @param phrase_source_files: files with terms to substitute in"""
    discourse_vars = get_vars(base_str)
    kwargs = {}
    for a_var in discourse_vars:
        if a_var in madlibs_phrases:
            kwargs[a_var] = madlibs_phrases[a_var]
        elif a_var in phrase_source_files:
            kwargs[a_var] = fill_template(get_rand_response(PHRASE_FILES[a_var]))
        else:
            kwargs[a_var] = ""
    return kwarg_substitute(base_str, **kwargs)

def pick_pattern(trigger_str=""):
    """ Takes a string and returns an appropriate corpus filename """
    if trigger_str == "thread":
        return THREADOF_FILE
    else:
        return random.choice(list(TEMPLATE_FILES.values()))
    
def get_rand_response(from_file):
    """ Simply picks a random line from a given file. """
    file_reader = open(os.path.join(__location__, from_file),"r")
    possible_lines = file_reader.readlines()
    txt_response = str(random.choice(possible_lines)).rstrip(TO_STRIP)
    file_reader.close()
    return txt_response
    
def get_vars(a_template):
    """ Takes a template string and returns all the variables in it.
    @param a_template: a template formatted string """
    return re.findall("(?<=\$)[\w-]*",a_template)

class InputTemplate:
    def __init__(self, trigger, madlib_blanks, template_file = MISC_TEMPLATES):
        self.trigger = trigger
        self.madlib_blanks = madlib_blanks
        self.template_file = template_file
    
    def matches(self, some_str):
        return some_str.startswith(self.trigger)
    
    def get_response(self, some_str):
        discourse_vars = self.extract_vars(some_str)
        the_template = get_rand_response(self.template_file)
        return fill_template(the_template, discourse_vars)
    
    def extract_vars(self, some_str):
        vars_caught = {}
        working_str = some_str
        if self.matches(some_str):
            working_str = working_str[len(self.trigger):].strip(TO_STRIP)
            for i in range(0,len(self.madlib_blanks)):
                if i < len(self.madlib_blanks) - 1:
                    next_index = working_str.find(self.madlib_blanks[i+1][0])
                    if next_index != -1:
                        intermediate_stuff = working_str[:next_index]
                        if self.madlib_blanks[i][2]:
                            vars_caught[self.madlib_blanks[i][1]] = intermediate_stuff.strip(TO_STRIP)
                        else:
                            vars_caught[self.madlib_blanks[i][1]] = intermediate_stuff[len(self.madlib_blanks[i][0]):].strip(TO_STRIP)
                        working_str = working_str[next_index:].strip(TO_STRIP)
                else:
                    if self.madlib_blanks[i][2]:
                        vars_caught[self.madlib_blanks[i][1]] = working_str.strip(TO_STRIP)
                    else:
                        vars_caught[self.madlib_blanks[i][1]] = working_str[len(self.madlib_blanks[i][0].strip(TO_STRIP)):].strip(TO_STRIP)
        else:
            raise ValueError("String is not of the correct template")
        return vars_caught

boughs_template = InputTemplate("the apparition",[["these","NOUN_PHRASE",True],["in","PREPOSITION_PHRASE",True],["petals on","NO",True],[" a ","ADJECTIVE",False]])
how_you_template = InputTemplate("how",[["are", "NOUN_PHRASE",False]], THREADOF_TEMPLATES)
watch_template = InputTemplate("i want to",[["watch", "NOUN_PHRASE",False],["i do not", "NO", True]], THEWEAVE_TEMPLATES)
what_template = InputTemplate("what",[["is","NOUN_PHRASE",False]], THREADOF_TEMPLATES)
what_template = InputTemplate("what",[["are","NOUN_PHRASE",False]], EMBROIDER_TEMPLATES)
ALL_TEMPLATES = [boughs_template, how_you_template, watch_template]

def make_image(some_txt, output_file=OUTPUT_IMAGE_FILE):    
    """Saves an image with given text. """
    stitch_pattern = Image.new("1", (IMAGE_WIDTH,IMAGE_HEIGHT), WHITE_BG)
    d = ImageDraw.Draw(stitch_pattern)
    d.multiline_text((LEFT_MARGIN,TOP_MARGIN), txt_lineate(some_txt.upper()), font=fnt)
    if not PERFORMING:
        stitch_pattern.show()
    stitch_pattern.save(os.path.join(__location__, output_file))



def formulate_response(text_in):
    lower_text = text_in.lower()
    for a_template in ALL_TEMPLATES:
        if a_template.matches(lower_text):
            return a_template.get_response(lower_text)
    return pick_similar_line(text_in)

def stitch_image(text_in=""):
    """ Takes a string text_in as a query and outputs a file to output_file with the appropriate response """
    the_text = formulate_response(text_in)
    make_image(the_text)
