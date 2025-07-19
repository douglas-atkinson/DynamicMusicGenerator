class ScaleLibrary:
    """
    Provides multi-octave scales for different keys.
    """

    KEY_ROOT_NOTES_MAJOR = {
        'C Major': 60,
        'D Major': 62,
        'E Major': 64,
        'F Major': 65,
        'G Major': 67,
        'A Major': 69,
        'B Major': 71,
        'Bb Major': 70,
        'Eb Major': 63
    }

    MAJOR_SCALE_STEPS = [0, 2, 4, 5, 7, 9, 11, 12]

    _major_scales_cache = None

    @classmethod
    def _generate_scale_for_key(cls, root_note, octaves=[48, 60, 72]):
        """
        Generate a multi-octave major scale starting from the given root note.

        :param root_note: MIDI note number for the key's tonic (e.g. 60 for C)
        :param octaves: List of base notes for octaves
        :return: List of MIDI note number in the scale
        """
        full_scale = []
        for base in octaves:
            for step in cls.MAJOR_SCALE_STEPS:
                note = base + (root_note - 60) + step
                full_scale.append(note)
        return sorted(full_scale)

    @classmethod
    def major_scales(cls, octaves=[48, 60, 72]):
        """
        Returns a dictionary of major scales for all keys over multiple octaves.
        Lazily initializes only once
        :param octaves: List of base notes for octaves
        :return: Dictionary of major scales
        """
        if cls._major_scales_cache is None:
            major_scales = {}
            for key_name, root_note in cls.KEY_ROOT_NOTES_MAJOR.items():
                major_scales[key_name] = cls._generate_scale_for_key(root_note, octaves)
            cls._major_scales_cache = major_scales
        return cls._major_scales_cache