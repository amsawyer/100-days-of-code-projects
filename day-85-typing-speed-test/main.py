import tkinter
from tkinter import *
import random
import math


### CONSTANTS ###
WORD_FILE = "/usr/share/dict/words"
WORDS = open(WORD_FILE).read().splitlines()
# only get words that are 8 or less chars and don't start with a capital letter (no proper nouns)
SHORT_WORDS = [word.lower() for word in WORDS if len(word) <= 8 and word[0] == word[0].lower()]
FONT_NAME = "Montserrat"
NUM_WORDS = 50
WIDTH = 700
HEIGHT = 200
# 1-minute test
TIMER_START = 60 # time from which to count down, in SECONDS
### GLOBAL VARS ###
timer_count = TIMER_START # initialize countdown to starting number of seconds
timer_started = False
timer = None
speed_test = None
space_bind = None
backspace_bind = None
start_timer_bind = None


def generate_random_words(num_words):
    """ Generate given number of random words for the typing speed test. """
    words = random.sample(SHORT_WORDS, num_words)
    return words


class TypingSpeedTest:
    def __init__(self, num_words):
        self.test_words = generate_random_words(num_words) # randomly system-generated test words
        self.input_text = "" # input typed in by the user
        self.correct_words = [] # list of words the user got correct
        self.word_pos = 0 # index of word we are currently on in test
        self.pos_in_word = 0 # index of char we are currently on within current word

    def next_word(self, event):
        """ Handle formatting for moving from one word to the next. """
        word = typing_input.get()
        correct_word = self.test_words[self.word_pos]
        self.input_text += word
        # clear input word from Entry
        typing_input.delete(0, tkinter.END)

        self.word_pos += 1
        self.pos_in_word = 0
        start_highlight = len(" ".join(self.test_words[:self.word_pos])) + 1
        end_highlight = start_highlight + len(self.test_words[self.word_pos])
        start_unhighlight = len(" ".join(self.test_words[:self.word_pos - 1]))
        # if user typed the word correctly
        if word.rstrip() == correct_word:
            words_text.tag_add('unhighlightwordcorrect', f'1.{start_unhighlight}', f'1.{start_highlight}')
        # else (user got the word wrong)
        else:
            words_text.tag_add('unhighlightwordwrong', f'1.{start_unhighlight}', f'1.{start_highlight}')

        # remove old tags from previous words so their color can be changed
        words_text.tag_remove('colorcorrect', '1.0', f'1.{start_highlight}')
        words_text.tag_remove('colorwrong', '1.0', f'1.{start_highlight}')
        # highlight next word in green
        words_text.tag_add('highlightword', f'1.{start_highlight}', f'1.{end_highlight}')

        # look 4 words ahead (auto-scroll down if needed)
        lookahead = end_highlight + len(" ".join(self.test_words[self.word_pos:self.word_pos+4]))
        words_text.see(f'1.{lookahead}')

    def backspace(self, event):
        """ Handle case where user presses backspace. Allow user to fix mistakes. """
        # back up position in word attribute by 1
        if self.pos_in_word > 0:
            self.pos_in_word -= 1
        start_color = len(" ".join(self.test_words[:self.word_pos])) + self.pos_in_word
        # if not first word, add 1 to index to account for space after previous word
        if self.word_pos > 0:
            start_color += 1
        end_color = start_color + 1
        # change back to original color
        words_text.tag_remove('colorwrong', f'1.{start_color}', f'1.{end_color}')
        words_text.tag_add('colorbackspace', f'1.{start_color}', f'1.{end_color}')

    def check_letter(self):
        """ Check if the latest character the user entered was correct. """
        # get latest character entered by the user
        try:
            last_char = typing_input.get()[-1]
        except IndexError:
            last_char = ""
        current_word = self.test_words[self.word_pos]
        start_color = len(" ".join(self.test_words[:self.word_pos])) + self.pos_in_word
        # if not first word, add 1 to index to account for space after previous word
        if self.word_pos > 0:
            start_color += 1
        end_color = start_color + 1
        try:
            words_text.tag_remove('colorbackspace', f'1.{start_color}', f'1.{end_color}')
            # color in white for correct character
            if last_char == current_word[self.pos_in_word]:
                words_text.tag_add('colorcorrect', f'1.{start_color}', f'1.{end_color}')
            # color in red for incorrect character
            else:
                words_text.tag_add('colorwrong', f'1.{start_color}', f'1.{end_color}')
            self.pos_in_word += 1
        # user has typed more characters than are in the word
        except IndexError:
            pass

    def check_accuracy(self):
        """ Check how many total words the user typed correctly. """
        input_words = self.input_text.split(" ")
        # clean up any empty string items in array
        input_words = [word for word in input_words if len(word) > 0]
        for pair in zip(self.test_words, input_words):
            if pair[0] == pair[1]:
                self.correct_words.append(pair[0])
        num_correct = len(self.correct_words)
        total_words = len(input_words)
        return num_correct, total_words

    def get_cpm(self):
        """ Get user's typing speed in characters per minute.
            Only count correct words."""
        minutes = TIMER_START / 60
        cpm = len("".join(self.correct_words)) / minutes
        return cpm

    def get_wpm(self):
        """ Get user's typing speed in words per minute.
            Only count correct words."""
        minutes = TIMER_START / 60
        wpm = len(self.correct_words) / minutes
        return wpm


def get_timer_text():
    """ Get correctly formatted display text for the timer based on current value of global var timer_count. """
    count_min = math.floor(timer_count / 60)
    count_sec = timer_count % 60
    if count_sec <= 9:
        count_sec = f"0{count_sec}"
    return count_min, count_sec


def keypress(event):
    """ On any keypress, start the timer and check whether the character entered was correct. """
    global timer_started
    if not timer_started:
        timer_started = True
        countdown()
    speed_test.check_letter()


def countdown():
    """ Handle the timer second-by-second countdown. """
    global timer
    global timer_count

    count_min, count_sec = get_timer_text()
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if timer_count > 0:
        # Wait 1 second (1000 ms) between runs
        timer = window.after(1000, countdown)
        timer_count -= 1
    else:
        times_up()


def times_up():
    """ Time's up - the test is complete. Get score and give user the option to try again. """
    # unbind keystroke bindings so test will no longer appear to function
    window.unbind("<space>", space_bind)
    window.unbind("<BackSpace>", backspace_bind)
    window.unbind("<Key>", start_timer_bind)

    num_correct, total = speed_test.check_accuracy()
    # characters per minute
    cpm = speed_test.get_cpm()
    # words per minute
    wpm = speed_test.get_wpm()
    canvas.itemconfig(welcome_text,
                      text=f"Time's up! You typed {num_correct}/{total} words correctly.\n"
                           f"Your typing speed is {cpm} CPM and {wpm} WPM (excluding incorrect words).",
                      fill="magenta",
                      font=("Arial", 16))
    typing_input.grid_forget()
    try_again_btn.grid(row=4, column=0)


def setup_test_ui():
    """ Display the typing speed test UI for a new test. """
    global speed_test
    global timer_count
    global timer_started
    global space_bind
    global backspace_bind
    global start_timer_bind

    # Clear words and other UI elements left over from previous speed test
    words_text.delete("1.0", 'end')
    try_again_btn.grid_forget()
    typing_input.delete(0, tkinter.END)

    # Initialize new speed test with random words
    speed_test = TypingSpeedTest(NUM_WORDS)

    # Reset timer to start time
    timer_count = TIMER_START
    timer_start_text = get_timer_text()
    # Display welcome/instructional message
    canvas.itemconfig(timer_text,
                      text=f"{timer_start_text[0]}:{timer_start_text[1]}")
    canvas.itemconfig(welcome_text,
                      text="Test your typing speed! Type as many words as you can in 1 minute.\n"
                           "Press space after each word you type.",
                      fill="green")
    speed_test_words = " ".join(speed_test.test_words)
    # Insert randomly generated test words at line 1, position 0
    words_text.insert("1.0",
                      speed_test_words)
    # Get index of first space (i.e. end of first word)
    space_idx = len(speed_test.test_words[0])
    # Highlight first word to start
    words_text.tag_add('highlightword', '1.0', f'1.{space_idx}')
    words_text.grid(row=2)
    typing_input.grid(row=4, column=0, rowspan=2, columnspan=3)
    # Start with focus in input box (like it has already been clicked into)
    typing_input.focus_set()

    timer_started = False
    space_bind = window.bind("<space>", speed_test.next_word)
    backspace_bind = window.bind("<BackSpace>", speed_test.backspace)
    start_timer_bind = window.bind("<Key>", keypress)


# Initial UI setup
window = Tk()
window.title("Typing Speed Test")
window.config(padx=50, pady=50)

canvas = Canvas(width=WIDTH, height=HEIGHT)
logo_img = PhotoImage(file="images/logo.gif")
canvas.create_image(WIDTH / 2, HEIGHT / 2, image=logo_img)
canvas.grid(row=0, column=0, columnspan=3)

# Set up timer
timer_text = canvas.create_text(600, 20,
                                fill="black",
                                font=("Courier", 30))
# Set up text/widgets/button
welcome_text = canvas.create_text(
    WIDTH / 2, HEIGHT * 0.85,
    fill="green",
    font=("Arial", 20))
words_text = Text(window,
                  width=34, height=3,
                  font=("Courier", 35),
                  wrap=WORD)
# Text widget tags for formatting
words_text.tag_configure('highlightword',
                         background='green')
words_text.tag_configure('unhighlightwordcorrect',
                         background='white',
                         foreground='blue')
words_text.tag_configure('unhighlightwordwrong',
                         background='white',
                         foreground='maroon')
words_text.tag_configure('colorcorrect',
                         foreground='white')
words_text.tag_configure('colorwrong',
                         foreground='red')
words_text.tag_configure('colorbackspace',
                         foreground='black')

typing_input = Entry(width=20,
                     font=("Arial", 30))
try_again_btn = Button(window,
                       text="Try Again",
                       command=setup_test_ui,
                       highlightbackground="blue")
setup_test_ui()


window.mainloop()
