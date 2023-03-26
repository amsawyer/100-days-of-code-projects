from tkinter import *
from tkinter.ttk import *

THEME_COLOR = "#502064"
PROGRESS_COLOR = "#FFBD35"
FONT = ("Arial", 18)
PLACEHOLDER_FONT = ("Arial", 18, "italic")
WIDTH = 800
HEIGHT = 400
PADX = 50
PADY = 40
TIMER_START = 5 # Timer counts down from 5 seconds
PLACEHOLDER_TEXT = 'Write anything...'
# deal with weirdness combining Progressbar and window.after
FULL_PROG_BAR = True


class WritingAppUI:

    def __init__(self):
        # Initialize UI class class attributes
        self.window = Tk()
        # set slightly more attractive tkinter theme
        s = Style()
        s.theme_use('clam')
        s.configure("colorful.Horizontal.TProgressbar", foreground=PROGRESS_COLOR, background=PROGRESS_COLOR)
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

        self.canvas = Canvas(width=WIDTH, height=HEIGHT,
                             borderwidth=0,
                             highlightthickness=0)
        # Text widget for user to type into
        self.text_editor = Text(self.window,
                                # 80 chars wide by 15 lines high
                                width=80, height=15,
                                padx=20, pady=20,
                                wrap=WORD)
        self.start_btn = Button(self.window,
                                text="Start Writing!",
                                command=self.start_writing)

        # Key binding on any key press
        self.timer_bind = self.window.bind("<Key>", self.reset_timer)
        # Progress bar to count down time remaining
        self.timer_bar = Progressbar(self.window,
                                     orient=HORIZONTAL,
                                     style="colorful.Horizontal.TProgressbar",
                                     length=WIDTH / 2,
                                     mode='determinate')
        # Configure Tkinter window
        self.window.title("Risky Writing App")
        self.window.config(padx=PADX, pady=PADY, bg=THEME_COLOR)

        # Canvas with welcome text
        self.welcome = self.canvas.create_text(
            WIDTH / 2, # x position
            HEIGHT / 2, # y position
            width=WIDTH - (PADX * 2),
            font=FONT,
            fill=THEME_COLOR,
            text="Welcome to the Risky Writing App! If you stop writing for more than "
                 "5 seconds, all you've written so far will disappear and your progress will be lost."
        )
        self.canvas.grid(row=0, column=0, pady=50)
        # Start button
        self.start_btn.grid(row=1, column=0)

        self.window.mainloop()

    def start_writing(self):
        """ Display the disappearing writing input box and start listening for keystrokes """
        # Clear off welcome screen
        self.canvas.destroy()
        self.start_btn.grid_forget()

        # Set up timer
        self.timer = None
        self.timer_bar.grid(row=0, column=1)
        # start progress bar at 100%
        self.timer_bar['value'] = 100

        self.text_editor.config(fg="gray", font=PLACEHOLDER_FONT)
        self.text_editor.insert('1.0', PLACEHOLDER_TEXT)
        self.text_editor.grid(row=1, column=0, columnspan=2, pady=50)
        self.text_editor.focus_set()

    def reset_timer(self, event):
        """ Reset timer back to 5 seconds (progress bar back to 100%) """
        global FULL_PROG_BAR

        # cancel previous timer if it is running
        if self.timer:
            self.window.after_cancel(self.timer)
            FULL_PROG_BAR = True
            # reset progress bar to 100%
            self.timer_bar['value'] = 100
        # clear out placeholder text
        else:
            self.text_editor.delete('1.0', f'1.{len(PLACEHOLDER_TEXT)}')
            self.text_editor.config(fg="black", font=FONT)
        # restart timer
        self.update_timer()

    def update_timer(self):
        """ Handle countdown - update timer every 1 second """
        global FULL_PROG_BAR

        if self.timer_bar['value'] > 0:
            # Wait 1 second (1000 ms) between runs
            self.timer = self.window.after(1000, self.update_timer)
            if not FULL_PROG_BAR:
                self.timer_bar['value'] -= (100 / TIMER_START)
            FULL_PROG_BAR = False
            # if time is running out, change progress bar color to red
            if self.timer_bar['value'] <= 40:
                self.timer_bar.config(style="red.Horizontal.TProgressbar")
        # time's up!
        if self.timer_bar['value'] == 0:
            self.self_destruct()

    def self_destruct(self):
        """ Clear any text that has been entered by the user and display Start Again button """
        self.text_editor.delete('1.0', 'end')
        self.start_btn.config(text="Start Again")
        self.start_btn.grid(row=2, column=0, columnspan=2)


writing_app = WritingAppUI()
