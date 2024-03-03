from PIL import Image, ImageDraw, ImageFont
from chord import Chord
import random
import os

# import cv2

from numpy.random import choice
from numpy import array

# Major	C Cmaj CM	C, E, G
# Minor	Cm Cmin C-	C, Eb, G
# Diminished	Cdim Co	C, Eb, Gb
# Augmented	Caug C+ C+5	C, E, G#

# https://www.myfonts.com/fonts/tijs-krammer/chord-symbols/

def random_boolean():
    return bool(random.getrandbits(1))

class ImageCreator():
    def __init__(self, chord_instance: Chord, debug_mode=True):
        self.debug_mode = debug_mode
        self.chord = chord_instance
        self.root = os.path.dirname(os.path.realpath(__file__))
        self.fonts_path = [
            f"{self.root}/fonts/Cooljazz.ttf",
            f"{self.root}/fonts/arial.ttf"
        ]
        # Each key is the label value of the symbol and
        # we going to use severals symbol versions for the
        # same label value
        self.symbols = {
            "major": ["", "ma", "M", "Maj"], #"/Users/charlyjazz/Charlyjazz/Chord-Letter-Sequencer/dataset_generator/symbols/major_triangle.png"
            "minor": ["-", "m", "minor"],
            "sharp": ["#"],
            "bimol": ["b"],
            "half disminished": ['Ø'],
            "disminished": ["○", "dim"],
            "augmented": ['+', 'aug']
        }
        self.font_sizes = range(25, 35)

        # Creating Image State

        self.font_size = None
        self.font_size_for_symbols_to_top_and_small = None
        self.font_size_for_dash_minor_symbol = None # '-'
        self.font_family = None
        self.truetype = None
        self.image = None
        self.draw = None
        self.x_offset = 0.0
        self.symbols_to_top_and_small = random_boolean()

    # Create image of the chord to save
    def create_image(self):
        self.font_size = choice(self.font_sizes)
        # Ok You going to be big as self.font_size because the "-" symbol is tiny
        self.font_size_for_dash_minor_symbol = self.font_size
        # Ok You going to be more smaller than the general font_size
        self.font_size_for_symbols_to_top_and_small = choice(range(self.font_size - 15, self.font_size - 5))
        self.font_family = choice(self.fonts_path)
        self.truetype = ImageFont.truetype(self.font_family, self.font_size)
        self.image = Image.new('RGB', (200, 50), color=(255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

        # Array of functions to split concerns and condionality
        pipeline = self.pipeline_of_texts()

        for fn in pipeline:
            self.debug('x_offset', self.x_offset)
            fn()

        # Show image
        if self.debug_mode:
            self.open_cv_show_image()

    # Helper for print and debug
    def debug(self, label, value):
        if self.debug_mode:
            print(f' - - [DEBUG] - {label} - {value}')

    # Useful pipeline of functions to send offset x in each function and
    # Separate concerns and complex logic in each function
    def pipeline_of_texts(self):
        return [
            self.draw_pitch,
            self.draw_accidentals,
            self.draw_quality,
            self.draw_bass_slash_note,
            self.draw_th_type,
            self.draw_interval_5th_accidental,
            self.draw_add_notes,
            self.draw_sus_type
        ]

    # Draw Pitch in the image
    def draw_pitch(self):
        self.draw.text((self.x_offset,  self.font_size / 2), self.chord.pitch, font=self.truetype, fill=(0, 0, 0))
        self.x_offset = self.draw.textlength(self.chord.pitch, self.truetype)

    # Add Slash note if exist
    def draw_bass_slash_note(self):
        if self.chord.bass_slash_note:
            text = "/" + self.chord.bass_slash_note
            self.draw.text((self.x_offset,  self.font_size / 2), text, font=self.truetype, fill=(0, 0, 0))
            self.x_offset = self.draw.textlength('/A', self.truetype) + self.x_offset

    # Draw Accidentals with letters or symbols (random choice) #, b
    def draw_accidentals(self):
        if self.chord.is_valid_accidental(self.chord.accidentals):
            self.draw.text((self.x_offset, self.font_size / 2), self.chord.accidentals, font=self.truetype, fill=(0, 0, 0))
            self.x_offset = self.draw.textlength(self.chord.accidentals, self.truetype) + self.x_offset

    # Draw Quality with letters or symbols (random choice)
    # Quality word are minor, major, augmented, disminished and half disminished
    def draw_quality(self):
        # Dont draw quality if the chord is a sus4 or sus2
        if self.chord.sus_type:
            return

        # Chose a symbol or word to replace the quality word
        synonymous = choice(self.symbols[self.chord.quality])
        fontsizes = range(20, 30)
        fontsize = int(choice(fontsizes))
        
        if ".png" in synonymous:
            image_symbol = Image.open(synonymous)
            image_symbol.thumbnail((fontsize, fontsize))
            image_symbol = image_symbol.convert("RGB").copy()
            self.image.paste(image_symbol, (int(self.x_offset),  int(self.font_size / 2)))
            self.x_offset = self.x_offset + fontsize
        elif len(synonymous):
            # Case special to center the "-" symbol
            if synonymous == "-": 
                fontsize = self.font_size_for_dash_minor_symbol
                font = ImageFont.truetype(self.font_family, fontsize)
                y = int(self.font_size / 2) + 2
            else:
                # Case special when you want the symbols more to the top and smaller
                if self.symbols_to_top_and_small:
                    fontsize = self.font_size_for_symbols_to_top_and_small
                font = ImageFont.truetype(self.font_family, fontsize)
                y = self.font_size - fontsize
            self.draw.text((self.x_offset, y), synonymous, font=font, fill=(0, 0, 0))
            self.x_offset = self.draw.textlength(synonymous, font) + self.x_offset
        else:
            pass

    # Draw the th interval type (7, 9, 11, 13, 15)
    def draw_th_type(self):
        if self.chord.th_type:
            # Case special when you want the symbols more to the top and smaller
            if self.symbols_to_top_and_small:
                fontsize = self.font_size_for_symbols_to_top_and_small
                font = ImageFont.truetype(self.font_family, fontsize)
                y = self.font_size - fontsize
                self.draw.text((self.x_offset, y), self.chord.th_type, font=font, fill=(0, 0, 0))
                self.x_offset = self.draw.textlength(self.chord.th_type, font) + self.x_offset
            else:
                self.draw.text((self.x_offset, self.font_size / 2), self.chord.th_type, font=self.truetype, fill=(0, 0, 0))
                self.x_offset = self.draw.textlength(self.chord.th_type, self.truetype) + self.x_offset

    # Draw if the 5th is bemol or sharp
    def draw_interval_5th_accidental(self):
        if self.chord.interval_5th_accidental:
            string = f"{self.chord.interval_5th_accidental}5"
            # Case special when you want the symbols more to the top and smaller
            if self.symbols_to_top_and_small:
                fontsize = self.font_size_for_symbols_to_top_and_small
                font = ImageFont.truetype(self.font_family, fontsize)
                y = self.font_size - fontsize
                self.draw.text((self.x_offset, y), string, font=font, fill=(0, 0, 0))
                self.x_offset = self.draw.textlength(string, font) + self.x_offset
            else:
                self.draw.text((self.x_offset, self.font_size / 2), string, font=self.truetype, fill=(0, 0, 0))
                self.x_offset = self.draw.textlength(string, self.truetype) + self.x_offset

    # Draw the added notes
    def draw_add_notes(self):
        with_parenthesis = random_boolean()
        if len(self.chord.extra_notes):
            for i in self.chord.extra_notes:
                string = f"(add{i})" if with_parenthesis else f" add{i}"
                # Case special when you want the symbols more to the top and smaller
                if self.symbols_to_top_and_small:
                    fontsize = self.font_size_for_symbols_to_top_and_small
                    font = ImageFont.truetype(self.font_family, fontsize)
                    y = self.font_size - fontsize
                    self.draw.text((self.x_offset, y), string, font=font, fill=(0, 0, 0))
                    self.x_offset = self.draw.textlength(string, font) + self.x_offset
                else:
                    self.draw.text((self.x_offset, self.font_size / 2), string, font=self.truetype, fill=(0, 0, 0))
                    self.x_offset = self.draw.textlength(string, self.truetype) + self.x_offset

    # Draw the added notes
    def draw_sus_type(self):
        if self.chord.sus_type:
            string = self.chord.sus_type
            self.draw.text((self.x_offset, self.font_size / 2), string, font=self.truetype, fill=(0, 0, 0))
            self.x_offset = self.draw.textlength(string, self.truetype) + self.x_offset

    # Helper to render image
    def open_cv_show_image(self):
        if self.debug_mode:
            self.debug('Chord', self.chord)
            self.image.show()
            # cv_img = array(self.image)
            # cv_img = cv_img[:, :, ::-1].copy()
            # cv2.imshow(str(self.chord), cv_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
