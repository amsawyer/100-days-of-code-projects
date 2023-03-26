from turtle import Turtle

FONT = ("Courier", 20, "normal")
LIVES_X_POS = -280
SCORE_X_POS = 270
Y_POS = -360


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.lives = 3
        self.score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(LIVES_X_POS, Y_POS)
        self.write(f"Lives: {self.lives}", align="center", font=FONT)
        self.goto(SCORE_X_POS, Y_POS)
        self.write(f"Score: {self.score}", align="center", font=FONT)

    def add_points(self, points):
        self.score += points
        self.update_scoreboard()

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Courier", 75))

    def game_over_win(self):
        self.goto(0, 0)
        self.write("YOU WIN!", align="center", font=("Courier", 75))
