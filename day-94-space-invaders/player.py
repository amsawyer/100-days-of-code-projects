from turtle import Turtle
from bullet import Bullet

MOVE_DISTANCE = 20
COLOR = "magenta"


class Player(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color(COLOR)
        # Stretch to 3 times standard length
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.penup()
        self.x = position[0]
        self.y = position[1]
        self.goto(position)
        self.bullets = []

    def move_left(self):
        self.x = self.xcor() - MOVE_DISTANCE
        self.goto(self.x, self.ycor())

    def move_right(self):
        self.x = self.xcor() + MOVE_DISTANCE
        self.goto(self.x, self.ycor())

    def shoot(self):
        self.bullets.append(Bullet((self.x, self.y + 20), COLOR))

    def reset_pos(self, position):
        self.goto(position)
        self.showturtle()
