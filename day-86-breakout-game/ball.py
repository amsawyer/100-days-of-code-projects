from turtle import Turtle

STARTING_X_POS = 0
STARTING_Y_POS = -50
MOVE_DISTANCE = 10
L_EDGE = -380
R_EDGE = L_EDGE * -1
STARTING_MOVE_SPEED = 0.1


class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("gray")
        self.penup()
        self.x = STARTING_X_POS
        self.y = STARTING_Y_POS
        self.goto((self.x, self.y))
        self.x_move = MOVE_DISTANCE
        self.y_move = MOVE_DISTANCE
        # Amount of time (in seconds) to sleep between each move
        self.move_speed = STARTING_MOVE_SPEED

    def move(self):
        self.x = self.xcor() + self.x_move
        self.y = self.ycor() + self.y_move
        self.goto((self.x, self.y))

    def x_bounce(self):
        self.x_move *= -1

    def y_bounce(self):
        self.y_move *= -1

    def reset_ball(self):
        self.x = STARTING_X_POS
        self.y = STARTING_Y_POS
        self.goto((self.x, self.y))
        self.move_speed = STARTING_MOVE_SPEED
        self.x_bounce()
