import music_generator
from music_generator import KEY_SCALES_MAJOR
from scale_library import ScaleLibrary


def main():

    # KEY_SCALES_MAJOR = ScaleLibrary.major_scales()
    #
    # for key, scale in KEY_SCALES_MAJOR.items():
    #     print(f"{key}: {scale}")

    # ---------------------
    # TEST PARAMETERS
    # ---------------------

    key_name = "C Major"
    tempo = 120
    instrument_program = music_generator.INSTRUMENTS["Acoustic Grand Piano"]
    note_length_fraction = 1.0
    note_count = 64
    leap_probability = 0.2
    max_leap_size = 4
    contour = "arch"  # Options: 'arch', 'ascending', 'descending', 'random'

    # --------------------
    # GENERATE MELODY
    # --------------------

    filename = music_generator.generate_melody_rule_based(
        key_name=key_name,
        tempo=tempo,
        instrument_program=instrument_program,
        note_length_fraction=note_length_fraction,
        note_count=note_count,
        leap_probability=leap_probability,
        max_leap_size=max_leap_size,
        contour=contour,
    )

    print(f"Melody generated and saved as: {filename}")

if __name__ == "__main__":
    main()