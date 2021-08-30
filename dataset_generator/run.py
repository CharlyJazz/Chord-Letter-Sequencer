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
CSharpMinor7 = Chord("C", "#", "minor", interval_5th_accidental="b", th_type="7", extra_notes=['6'])
# CSharpSus4 = Chord("A", "#", "minor", bass_slash_note="B#")


if __name__ == '__main__':
    # image_creator = ImageCreator(ChordConstructorRandom().chord_creation_flow())
    image_creator = ImageCreator(CSharpMinor7)
    image_creator.create_image()
