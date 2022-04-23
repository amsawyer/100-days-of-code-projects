from morse_string import MorseStringConverter


def get_user_input():
    return input("What string would you like to convert to Morse code?:\n")


keep_going = True
while keep_going:
    start_str = get_user_input()

    morse_str_conv = MorseStringConverter(start_str)
    morse_str = morse_str_conv.convert_to_morse_code()

    if morse_str_conv.invalid_chars:
        print("Warning: Your string contains invalid characters"
              " that do not exist in Morse code.\nThey have been"
              " kept in the string as is.")

    print(f"Morse code:  {morse_str}")
    keep_going_answer = input("\nConvert another string? [Y/n]: ")
    if keep_going_answer.upper() == 'N':
        keep_going = False
