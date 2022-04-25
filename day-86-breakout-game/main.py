from turtle import Screen
from paddle import Paddle
from ball import Ball
from brick import Brick
from scoreboard import Scoreboard
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PADDLE_X_POS = 0
PADDLE_Y_POS = (SCREEN_HEIGHT / 2 - 50) * -1
PADDLE_BALL_COLLISION_Y_POS = PADDLE_Y_POS + 30

U_EDGE = SCREEN_HEIGHT / 2 - 20
B_EDGE = U_EDGE * -1
R_EDGE = SCREEN_WIDTH / 2 - 20
L_EDGE = R_EDGE * -1

PADDLE_DISTANCE = 50
BRICK_DISTANCE = 40

MOVE_SPEED_RATIO = 0.9


def build_bricks():
    """ Build rows of bricks to break out of at the top. """
    bricks = []

    # 8 rows, each 14 bricks across
    rows = 8
    cols = 14
    colors = ["red", "red", "orange", "orange", "green", "green", "yellow", "yellow"]
    point_values = [7, 7, 5, 5, 3, 3, 1, 1]
    y_pos = SCREEN_HEIGHT / 2 * 0.7
    x_step = (SCREEN_WIDTH - 50) / (cols - 1)
    y_step = 30

    for i in range(rows):
        x_pos = SCREEN_WIDTH / 2 * -1 + 20
        y_pos -= y_step
        color = colors[i]
        point_value = point_values[i]
        for j in range(cols):
            bricks.append(Brick(color, (x_pos, y_pos), point_value))
            x_pos += x_step
    return bricks


screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("black")
screen.title("Breakout")
# Turn off animation when paddle is first created
screen.tracer(0)

paddle = Paddle((PADDLE_X_POS, PADDLE_Y_POS))
ball = Ball()
scoreboard = Scoreboard()

# Event listener + key bindings
screen.listen()
screen.onkey(paddle.move_left, "Left")
screen.onkey(paddle.move_right, "Right")

game_is_on = True


def play_round():
    """ Play round of Breakout (goes until player either loses all their lives or hits all the bricks). """
    global game_is_on

    hit_count = 0
    orange_hit = False
    red_hit = False

    ball.reset_ball()
    # build colorful bricks at the top
    all_bricks = build_bricks()

    while game_is_on:
        time.sleep(ball.move_speed)
        # Manually update screen to get updated animations
        screen.update()
        # Ball continuously moves
        ball.move()

        # Detect collision with left or right wall and bounce off
        if ball.x < L_EDGE or ball.x > R_EDGE:
            ball.x_bounce()

        # Detect collision with ceiling and bounce off
        if ball.y > U_EDGE:
            ball.y_bounce()
            # Check if this is the first ceiling hit. If so, shrink paddle to half size.
            if not paddle.halfsize:
                paddle.half_size()

        # Detect collision with paddle and bounce off paddle
        if ball.distance(paddle) < PADDLE_DISTANCE and ball.y < PADDLE_BALL_COLLISION_Y_POS:
            ball.y_bounce()

        # Detect when paddle misses the ball - Lose a life
        if ball.y < B_EDGE:
            ball.reset_ball()
            paddle.reset_paddle((PADDLE_X_POS, PADDLE_Y_POS))
            # Lose a life
            scoreboard.lose_life()
            # Check if game is over
            if scoreboard.lives == 0:
                scoreboard.game_over()
                ball.hideturtle()
                game_is_on = False

        # Detect collision with brick
        min_dist = SCREEN_HEIGHT
        for brick in all_bricks:
            if ball.distance(brick) < min_dist:
                closest_brick = brick
                min_dist = ball.distance(brick)
        # collision with brick!
        if min_dist < BRICK_DISTANCE:
            hit_count += 1
            # Brick that was hit disappears
            closest_brick.hideturtle()
            all_bricks.remove(closest_brick)

            # Add points to score
            scoreboard.add_points(closest_brick.point_value)

            x_dist = abs(closest_brick.pos()[0] - ball.pos()[0])
            y_dist = abs(closest_brick.pos()[1] - ball.pos()[1])
            # ball hit top or bottom of brick (normalized for rectangular shape of brick)
            if x_dist <= (y_dist * 3):
                ball.y_bounce()
            # else ball hit left or right side of brick
            else:
                ball.x_bounce()

            # check if all the bricks have disappeared
            if len(all_bricks) == 0:
                break

            # Check if we need to increase the ball speed
            #  - This happens on the 4th and 12th hits
            if hit_count == 4 or hit_count == 12:
                ball.move_speed *= MOVE_SPEED_RATIO
            #  - And the first times the orange and red rows are hit
            if not orange_hit and closest_brick.color == "orange":
                ball.move_speed *= MOVE_SPEED_RATIO
                orange_hit = True
            elif not red_hit and closest_brick.color == "red":
                ball.move_speed *= MOVE_SPEED_RATIO
                red_hit = True


# There are 2 rounds of the game
for _ in range(2):
    play_round()
    if game_is_on:
        scoreboard.game_over_win()
# Keep ball bouncing around
while game_is_on:
    time.sleep(ball.move_speed)
    # Manually update screen to get updated animations
    screen.update()
    # Ball continuously moves
    ball.move()

    # Detect collision with left or right wall and bounce off
    if ball.x < L_EDGE or ball.x > R_EDGE:
        ball.x_bounce()

    # Detect collision with floor or ceiling and bounce off
    if ball.y < B_EDGE or ball.y > U_EDGE:
        ball.y_bounce()

screen.exitonclick()
