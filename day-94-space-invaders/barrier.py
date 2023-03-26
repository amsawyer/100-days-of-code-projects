from turtle import Turtle


class Barrier(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("gray")
        self.turtlesize(0.5)
        self.penup()
        self.goto(position)
