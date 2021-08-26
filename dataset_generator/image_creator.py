from PIL import Image, ImageDraw, ImageFont
from chord import Chord

# import cv2

from numpy.random import choice
from numpy import array

# Major	C Cmaj CM	C, E, G
# Minor	Cm Cmin C-	C, Eb, G
# Diminished	Cdim Co	C, Eb, Gb
# Augmented	Caug C+ C+5	C, E, G#

class ImageCreator():
    def __init__(self, chord_instance: Chord):
        self.chord = chord_instance
        self.fonts_path = [
            "/Users/charlyjazz/Charlyjazz/Chord-Letter-Sequencer/dataset_generator/fonts/Cooljazz.ttf",
            # "/Users/charlyjazz/Charlyjazz/Chord-Letter-Sequencer/dataset_generator/fonts/arial.ttf"
        ]
        # Each key is the label value of the symbol and
        # we going to use severals symbol versions for the
        # same label value
        self.symbols = {
            "major": ["", "ma", "M", "Maj", ], #"/Users/charlyjazz/Charlyjazz/Chord-Letter-Sequencer/dataset_generator/symbols/major_triangle.png"
            "minor": ["-", "m", "min", "mi"],
            "sharp": ["#"],
            "bimol": ["b"],
            "half disminished": ['Ø'],
            "disminished": ["○", "dim"],
            "augmented": ['+', 'aug']
        }
        self.font_sizes = [35]

        # Creating Image State

        self.chord_string_length = None
        self.font_size = None
        self.font_family = None
        self.truetype = None
        self.image = None
        self.draw = None
        self.x_offset = 0.0

    # This method need measure the real chord length because
    # word like disminished will be replace with a symbol then len(str)
    # is wrong because if the image wil be a symbol with the length
    # of a single character
    def len_chord(self, string):
        return len(string)

    # Create image of the chord to save
    def create_image(self):
        self.chord_string_length = self.len_chord(str(self.chord))
        self.font_size = choice(self.font_sizes)
        self.font_family = choice(self.fonts_path)
        self.truetype = ImageFont.truetype(self.font_family, self.font_size)
        self.image = Image.new('RGB', (int((self.font_size / 1.5) * self.chord_string_length), 100), color=(255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

        # Array of functions to split concerns and condionality
        pipeline = self.pipeline_of_texts()

        for fn in pipeline:
            self.debug('x_offset', self.x_offset)
            fn()

        # Show image
        self.open_cv_show_image()

    def debug(self, label, value):
        print(f' - - [DEBUG] - {label} - {value}')

    # Useful pipeline of functions to send offset x in each function and
    # Separate concerns and and complex logic in each function
    def pipeline_of_texts(self):
        return [
            self.draw_pitch,
            self.draw_accidentals,
            self.draw_bass_slash_note,
            self.draw_quality
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
        # Chose a symbol or word to replace the quality word
        synonymous = choice(self.symbols[self.chord.quality])
        fontsizes = range(13, 18)
        fontsize = int(choice(fontsizes))
        if ".png" in synonymous:
            image_symbol = Image.open(synonymous)
            image_symbol.thumbnail((fontsize, fontsize))
            image_symbol = image_symbol.convert("RGB").copy()
            self.image.paste(image_symbol, (int(self.x_offset),  int(self.font_size / 2)))
            # Revisar esto
            self.x_offset = self.x_offset + fontsize
        elif len(synonymous):
            font = ImageFont.truetype(self.font_family, fontsize)
            y = self.font_size - fontsize # Responsivity
            self.draw.text((self.x_offset, y), synonymous, font=font, fill=(0, 0, 0))
            self.x_offset = self.draw.textlength(synonymous, font) + self.x_offset
        else:
            pass

    def open_cv_show_image(self):
        self.debug('Chord', self.chord)
        self.image.show()
        # cv_img = array(self.image)
        # cv_img = cv_img[:, :, ::-1].copy()
        # cv2.imshow(str(self.chord), cv_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
