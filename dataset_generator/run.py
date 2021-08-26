from chord_constructor_random import ChordConstructorRandom
from image_creator import ImageCreator
from chord import Chord

# https://www.pianochord.org/chord-symbols.html

# Cases: Triangle Symbol, M letter, Maj word
Cmajor = Chord("C", "#", "major", bass_slash_note="A")
Cminor = Chord("C", "", "minor")
Chalfdimismished = Chord("C", "", "half disminished")
Cdisminished = Chord("C", "#", "disminished")
Caugmented = Chord("C", "#", "augmented")

if __name__ == '__main__':
    image_creator = ImageCreator(ChordConstructorRandom().chord_creation_flow())
    image_creator.create_image()
