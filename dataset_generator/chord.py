class Chord():
    def __init__(
        self, 
        pitch, 
        accidental, 
        quality,
        interval_5th_accidental=None,
        th_type=None,
        extra_notes=None,
        sus_type=None,
        bass_slash_note=None
    ):
        self.pitch = pitch
        # TODO: Singular
        self.accidentals = accidental
        self.quality = quality
        self.interval_5th_accidental = interval_5th_accidental
        self.th_type = th_type
        self.extra_notes = extra_notes
        self.sus_type = sus_type
        self.bass_slash_note = bass_slash_note

    @staticmethod
    def is_valid_accidental(accidental: str):
        return accidental == "b" or accidental == "#"

    def add_interval_5th_accidental(self, value):
        if self.is_valid_accidental(value):
            self.interval_5th_accidental = value

    def add_pick_th_type(self, value):
        self.th_type = value

    def add_pick_sus_type(self, value):
        self.sus_type = value

    def add_extra_note(self, values):
        for i in values:
            self.extra_notes.append(i)

    def add_bass_slash_note(self, value):
        if value != self.pitch:
            self.bass_slash_note = value

    def __str__(self):
        string = self.pitch

        if self.bass_slash_note:
            string = "{0}/{1}".format(string, self.bass_slash_note)

        if self.is_valid_accidental(self.accidentals):
            string = "{0} {1}".format(string, self.accidentals)

        if self.quality:
            string = "{0} {1}".format(string, self.quality)

        if self.th_type:
            string = "{0} {1}".format(string, self.th_type)

        if self.is_valid_accidental(self.interval_5th_accidental):
            string = "{0} {1}5".format(string, self.interval_5th_accidental)

        if self.extra_notes:
            string = "{0} {1}".format(string, " ".join(self.extra_notes))

        if self.sus_type:
            string = "{0} {1}".format(string, self.sus_type)

        return string
