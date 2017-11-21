'''
Created on Oct 24, 2017

@author: Admin
'''
from PIL import Image, ImageDraw
import nltk
import random

def tag_sent(sent):
    return nltk.pos_tag(nltk.word_tokenize(sent))

class TextAtom:
    """ Just a pair of a syntactic category and a word. """
    
    def __init__(self, cat, wrd):
        self.cat = cat
        self.wrd = wrd
    
    def __str__(self):
        return self.wrd    

class Stitch:
    """ Has a name, and a list of text_atom """
        
    def __init__(self, text_atoms):
        self.text_atoms = text_atoms
        
    def __str__(self):
        return " ".join(list(map(lambda x: x.wrd, self.text_atoms)))
    
    def stitch_with(self, the_other):
        return Stitch(self.text_atoms + the_other.text_atoms[1:])

a_the = TextAtom("DT","the")
a_cross_hatching = TextAtom("NN","cross-hatching")
a_technique = TextAtom("NN","technique")
a_which = TextAtom("WDT","which")

a_automated = TextAtom("VBD", "automated")
a_manufacturing = TextAtom("NN","manufacturing")
a_processes = TextAtom("NNS","processes")

a_passes = TextAtom("VBZ", "passes")
a_into = TextAtom("IN","into")
a_silhouetting = TextAtom("VBG", "silhouetting")

a_lattices = TextAtom("VBZ", "lattices")
a_up = TextAtom("RP", "up")
a_dustmotes = TextAtom("NNS", "dustmotes")

a_goats = TextAtom("NNS", "goats")
a_loudly = TextAtom("RB", "loudly")
a_chew = TextAtom("VB", "chew")

a_inscriptions = TextAtom("NNS", "inscriptions")
a_are = TextAtom("VBG", "are")

a_into = TextAtom("RP", "into")
a_warehouse = TextAtom("NN", "warehouse")
a_roof = TextAtom("NN", "roof")

whatever_stitch = Stitch([a_the, a_cross_hatching, a_technique, a_which])
loop_stitch = Stitch([a_which, a_passes, a_into, a_silhouetting])
automation_stitch = Stitch([a_the, a_automated, a_manufacturing, a_processes, a_which])
mote_stitch = Stitch([a_which, a_lattices, a_dustmotes, a_up])
goats_stitch = Stitch([a_which, a_goats, a_loudly, a_chew, a_up])
inscriptions_stitch = Stitch([a_which, a_inscriptions, a_are, a_silhouetting])
roof_stitch = Stitch([a_up, a_into, a_the, a_warehouse, a_roof])


stitch_dict = [whatever_stitch, loop_stitch, automation_stitch, mote_stitch, goats_stitch, inscriptions_stitch, roof_stitch]

def quilt_together(stitches_known, starting_word, quilt_length):
    """ Takes a list of stitches and finds a way to combine them with single overlaps. """
    word_quilt = Stitch([starting_word])
    while len(word_quilt.text_atoms) < quilt_length:    
        possible_extensions = list(filter(lambda s: word_quilt.text_atoms[-1] == s.text_atoms[0], stitches_known))
        if len(possible_extensions) > 0:
            next_thing = random.choice(possible_extensions)
            word_quilt = word_quilt.stitch_with(next_thing)
            quilt_length -= len(next_thing.text_atoms)
        elif len(possible_extensions) <= 0:
            return word_quilt
    return word_quilt

def stitch_response(text_in):
    return quilt_together(stitch_dict, a_the, 12)

def sample_stitch():
    print(stitch_response("no"))

def stitch_image(text_in):
    stitch_pattern = Image.new("1", (512,512), 255)
    d = ImageDraw.Draw(stitch_pattern)
    d.text((10,10), str(stitch_response("no")))
    return stitch_pattern

