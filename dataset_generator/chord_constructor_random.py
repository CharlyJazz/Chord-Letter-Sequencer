from chord import Chord

import random
import numpy as np

class ChordConstructorRandom():
    def __init__(self):
        self.notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.accidentals = ["#", "b", "♮"]
        self.qualities = ["major", "minor", "disminished",
                          "half disminished", "augmented"]
        self.th_types = ["6", "7", "9", "11", "13"]
        self.extra_notes = ["2", "4", "6", "7", "9", "11", "13"]
        self.sus_types = ["sus2", "sus4"]
        self.extra_note_accidentals = ["#", "b", ""]

    def pick_quality(self):
        return np.random.choice(self.qualities)

    def pick_pitch(self):
        return np.random.choice(self.notes)

    def pick_accidental(self):
        return np.random.choice(self.accidentals)

    def pick_th_type(self):
        return "{0}th".format(np.random.choice(self.th_types))

    def pick_sus_type(self):
        return np.random.choice(self.sus_types)

    def pick_notes(self):
        notes_list = np.unique(np.random.choice(
            self.extra_notes, size=np.random.randint(1, 3)))
        notes_list_final = []
        for i in notes_list:
            notes_list_final.append(
                "{0}{1}".format(
                    np.random.choice(self.extra_note_accidentals),
                    i
                )
            )

        return notes_list_final

    def pick_bass_slash_note(self):
        return "{0}".format(
            # np.random.choice(self.extra_note_accidentals),
            self.pick_pitch()
        )

    def chord_creation_flow(self):
        fundamental_pitch = self.pick_pitch()
        accidental = self.pick_accidental()
        quality = self.pick_quality()

        new_chord = Chord(
            fundamental_pitch,
            accidental,
            quality,
            extra_notes=[]
        )

        if quality == 'major' or quality == "minor":

            optional_interval_5th_accidental = self.add_or_not()
            optional_th_type = self.add_or_not()
            optional_sus_type = self.add_or_not()
            optional_add_notes = self.add_or_not()

            if optional_interval_5th_accidental:
                interval_5th_accidental = self.pick_accidental()

                new_chord.add_interval_5th_accidental(
                    interval_5th_accidental
                )

            if optional_th_type:
                th_type = self.pick_th_type()

                new_chord.add_pick_th_type(
                    th_type
                )

            if optional_sus_type and not optional_th_type and not optional_interval_5th_accidental:
                sus_type = self.pick_sus_type()

                new_chord.add_pick_sus_type(
                    sus_type
                )

            if optional_add_notes:
                new_chord.add_extra_note(self.pick_notes())

        elif self.add_or_not():
            new_chord.add_extra_note(self.pick_notes())

        if self.add_or_not():
            new_chord.add_bass_slash_note(self.pick_bass_slash_note())

        return new_chord

    def add_or_not(self):
        return bool(random.getrandbits(1))
