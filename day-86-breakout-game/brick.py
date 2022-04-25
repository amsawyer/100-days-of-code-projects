from turtle import Turtle


class Brick(Turtle):

    def __init__(self, brick_color, position, point_val):
        super().__init__()
        self.shape("square")
        self.color(brick_color)
        self.point_value = point_val
        self.shapesize(stretch_wid=1, stretch_len=2.5)
        self.penup()
        self.goto(position)
