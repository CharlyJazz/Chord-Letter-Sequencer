from chord_constructor_random import ChordConstructorRandom
from image_creator import ImageCreator
from chord import Chord

import argparse

def non_or_str(value):
    if value == None:
        return None
    return value

# https://www.pianochord.org/chord-symbols.html

# Cmajor = Chord("C", "#", "major", bass_slash_note="A")
# Cminor = Chord("C", "", "minor")
# Chalfdimismished = Chord("C", "", "half disminished")
# Cdisminished = Chord("C", "#", "disminished")
# Caugmented = Chord("C", "#", "augmented")
# Chord = Chord("C", "#", "minor", interval_5th_accidental="b", th_type="7", extra_notes=['9'], bass_slash_note="F")
# CSharpSus4 = Chord("A", "#", "minor", bass_slash_note="B#")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OCR using CNN+RNN+CTC')
    parser.add_argument('--path', type=non_or_str, help='path to the directory')
    parser.add_argument('--count', type=int, help="No. of images to create")
    args = parser.parse_args() 

    if args.count and args.path:
        for i in range(args.count):
            chord_instance = ChordConstructorRandom().chord_creation_flow()
            image_creator = ImageCreator(chord_instance, False)
            image_creator.create_image()
            # Lol
            label = str(image_creator.chord).replace("/", " slash ")
            image_creator.image.save(f"/{args.path}/{label}.png")
    else:
        image_creator = ImageCreator(ChordConstructorRandom().chord_creation_flow())
        image_creator.create_image()

# python3 dataset_generator/run.py --path /Users/charlyjazz/Charlyjazz/Chord-Letter-Sequencer/dataset --count 2
