
MORSE_CODE_DICT = { 'A': '.-', 'B': '-...',
                    'C': '-.-.', 'D': '-..', 'E': '.',
                    'F': '..-.', 'G': '--.', 'H': '....',
                    'I': '..', 'J': '.---', 'K': '-.-',
                    'L': '.-..', 'M': '--', 'N': '-.',
                    'O': '---', 'P': '.--.', 'Q': '--.-',
                    'R': '.-.', 'S': '...', 'T': '-',
                    'U': '..-', 'V': '...-', 'W': '.--',
                    'X': '-..-', 'Y': '-.--', 'Z': '--..',
                    '1': '.----', '2': '..---', '3': '...--',
                    '4': '....-', '5': '.....', '6': '-....',
                    '7': '--...', '8': '---..', '9': '----.',
                    '0': '-----', ', ': '--..--', '.': '.-.-.-',
                    '?': '..--..', '/': '-..-.', '-': '-....-',
                    '(': '-.--.', ')': '-.--.-'}


class MorseStringConverter:
    def __init__(self, string):
        self.orig_str = string
        self.invalid_chars = False

    def convert_to_morse_code(self):
        morse_str = ""
        for char in self.orig_str:
            # Make uppercase to work with dictionary lookup
            char = char.upper()
            # Build string out of Morse code values
            try:
                morse_str += MORSE_CODE_DICT[char]
            # Char does not have a value in Morse code. Append char as is.
            except KeyError:
                self.invalid_chars = True
                morse_str += char
            morse_str += ' '
        return morse_str.rstrip()

