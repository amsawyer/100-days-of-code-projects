from turtle import Turtle

UP_DIR = 90
DOWN_DIR = 270
LEFT_DIR = 180
RIGHT_DIR = 0
MOVE_DISTANCE = 20


class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("lightblue")
        # Stretch to 10 times standard length
        self.shapesize(stretch_wid=1, stretch_len=10)
        self.penup()
        self.goto(position)
        self.halfsize = False

    def move_left(self):
        new_x = self.xcor() - MOVE_DISTANCE
        self.goto(new_x, self.ycor())

    def move_right(self):
        new_x = self.xcor() + MOVE_DISTANCE
        self.goto(new_x, self.ycor())

    def half_size(self):
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.halfsize = True

    def reset_paddle(self, position):
        self.goto(position)
