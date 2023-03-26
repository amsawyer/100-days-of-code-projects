from turtle import Turtle


class Bullet(Turtle):
    def __init__(self, position, color):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.turtlesize(0.25)
        self.shapesize(stretch_wid=1, stretch_len=0.25)
        self.penup()
        self.x = position[0]
        self.y = position[1]
        self.goto((self.x, self.y))

    def move(self, move_dir, move_dist):
        self.y = self.ycor() + move_dist * move_dir
        self.goto((self.xcor(), self.y))
