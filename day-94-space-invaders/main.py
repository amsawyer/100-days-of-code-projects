from turtle import Screen
from player import Player
from alienship import AlienShip
from barrier import Barrier
from scoreboard import Scoreboard
import time
import random

# Formatting/gameplay constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
PLAYER_X_POS_START = 0
PLAYER_Y_POS_START = SCREEN_HEIGHT * -0.375

U_EDGE = SCREEN_HEIGHT / 2 - 20
B_EDGE = U_EDGE * -1
R_EDGE = SCREEN_WIDTH / 2 - 80
L_EDGE = R_EDGE * -1

BARRIER_Y_START = SCREEN_HEIGHT * -0.1
BARRIER_DISTANCE_APART = SCREEN_HEIGHT * 0.225
BARRIER_COLLISION_DISTANCE = 10
SHIP_COLLISION_X_DIST = 32
SHIP_COLLISION_Y_DIST = 20

# Starting variable that determines frequency of randomly triggered alien bullets.
# Lower value == more alien bullets.
ALIEN_BULLET_FREQUENCY = 72
MOVE_SPEED = 0.1
alien_move_dir = 1
alien_ships_pos = 0
ALIENS_X_DIST = 50
ALIENS_Y_DIST = 32

PLAYER_BULLET_MOVE_DIST = 40
ALIEN_BULLET_MOVE_DIST = 5


def make_barrier(x):
    """ Build defensive barrier between player ship and alien ships.
        :return: List of Barrier objects comprising one barrier
    """
    barriers = []
    for i in range(10):
        y = BARRIER_Y_START
        col_height = 7
        if i in [1, 8]:
            col_height -= 1
        elif i in [0, 9]:
            col_height -= 2
        for _ in range(col_height):
            barriers.append(Barrier((x, y)))
            y += 10
        x += 10
    return barriers


def create_barriers():
    """ Build set of 4 defensive barriers in between the player and the alien ships.
        :return: List of Barrier objects comprising all 4 barriers
     """
    barrier_parts = []
    x_pos = SCREEN_WIDTH * -0.4
    for _ in range(4):
        barrier = make_barrier(x_pos)
        barrier_parts += barrier
        x_pos += 180
    return barrier_parts


def create_alien_ships():
    """ Create fleet of alien ships (3 rows and 8 columns of ships)
        :return:
          - List of AlienShip objects
          - int which is the number of alien ships in the fleet
    """
    alien_ships = []
    ships_count = 0
    # 3 rows of 8
    y_pos = SCREEN_HEIGHT * 0.25
    for _ in range(3):
        alien_row = []
        x_pos = SCREEN_WIDTH * -0.4
        for _ in range(8):
            alien_row.append(AlienShip((x_pos, y_pos)))
            x_pos += ALIENS_X_DIST
        y_pos += ALIENS_Y_DIST
        alien_ships.append(alien_row)
        ships_count += len(alien_row)
    return alien_ships, ships_count  # 3 row x 8 col 2-d array


def move_alien_ships(aliens, move_dir):
    """ Continuously move fleet of alien ships back and forth across top of screen.
        Flip the move direction when the ships near one edge or the other.
        :return: int representing move dir (-1 for left, 1 for right)
    """
    global alien_ships_pos
    alien_ships_pos += 1
    # check if move direction change is needed
    if alien_ships_pos >= 59:
        move_dir *= -1
        alien_ships_pos = 0
    for alien_row in aliens:
        for alien in alien_row:
            if alien is not None:
                alien.move(move_dir)
    return move_dir


def move_bullets(bullets, move_dir, move_dist):
    """ Move bullets across the screen.
        :return: List of Bullet objects
    """
    for bullet in bullets:
        if (move_dir == 1 and bullet.y < U_EDGE) or (move_dir == -1 and bullet.y > B_EDGE):
            bullet.move(move_dir, move_dist)  # player bullets move upwards
        else:  # clear bullet from screen and hide it
            bullet.clear()
            bullet.ht()
            bullets.remove(bullet)
    return bullets


def aliens_shoot(aliens):
    """ Make the alien ship fleet randomly shoot bullets at the player. """
    # Get bottom row of alien ships to shoot bullets from
    bottom_row = [None] * len(aliens[0])
    for alien_row in reversed(aliens):
        for i in range(len(alien_row)):
            if alien_row[i] is not None:
                bottom_row[i] = alien_row[i]
    rand_idx = random.randint(0, ALIEN_BULLET_FREQUENCY)
    # Randomly generate index to possibly shoot bullet from one of the alien ships in the bottom row
    rand_alien = None
    try:
        rand_alien = bottom_row[rand_idx]
    except IndexError:
        pass
    if rand_alien:
        rand_alien.shoot()
    for alien_row in aliens:
        for alien in alien_row:
            if alien is not None:
                # move_dir of -1 to move bullets downwards
                alien.bullets = move_bullets(alien.bullets, -1, ALIEN_BULLET_MOVE_DIST)


def detect_barrier_collision(bullets, barriers):
    """ Detect a collision of a bullet with a barrier. Both the barrier part and bullet disappear.
        :return:
          - List of Bullet objects after checking for collisions
          - List of Barrier objects after checking for collisions
    """
    for bullet in bullets:
        for barrier in barriers:
            if bullet.distance(barrier) < BARRIER_COLLISION_DISTANCE:
                # Piece of barrier that was hit and bullet both disappear
                if bullet in bullets:
                    bullet.hideturtle()
                    bullets.remove(bullet)
                barrier.hideturtle()
                barriers.remove(barrier)
    return bullets, barriers


def detect_ship_collision(bullets, ship):
    """ Detect a collision of a bullet with a ship. Bullet disappears. If alien ship, the ship disappears.
        :return:
          - List of Bullet objects after checking for collisions
          - Boolean indicating whether a collision occurred or not
    """
    collision = False
    for bullet in bullets:
        x_dist = abs(bullet.x - ship.x)
        y_dist = abs(bullet.y - ship.y)
        if x_dist < SHIP_COLLISION_X_DIST and y_dist < SHIP_COLLISION_Y_DIST:
            # Ship that was hit and bullet both disappear
            bullet.hideturtle()
            if bullet in bullets:
                bullets.remove(bullet)
            ship.hideturtle()
            collision = True
            break
    return bullets, collision


def clear_bullets(player_bullets, aliens):
    """ Clear bullets from screen when player loses a life. """
    for bullet in player_bullets:
        bullet.hideturtle()
    for alien_row in aliens:
        for alien in alien_row:
            if alien is not None:
                for bullet in alien.bullets:
                    bullet.hideturtle()


screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("black")
screen.title("Space Invaders")
# Turn off animation when elements are first created on screen
screen.tracer(0)

player = Player((PLAYER_X_POS_START, PLAYER_Y_POS_START))
scoreboard = Scoreboard()

# Event listener + key bindings
screen.listen()
screen.onkey(player.move_left, "Left")
screen.onkey(player.move_right, "Right")
screen.onkey(player.shoot, "space")

game_is_on = True

all_barriers = create_barriers()
aliens, alien_ships_count = create_alien_ships()
# list of bullets whose parent alien ship was destroyed
orphan_bullets = []
screen.update()


while game_is_on:
    time.sleep(MOVE_SPEED)
    # Manually update screen to get updated animations
    screen.update()
    # Alien ships continuously move back and forth
    alien_move_dir = move_alien_ships(aliens, alien_move_dir)
    # Move player bullets upwards across screen
    player.bullets = move_bullets(player.bullets,
                                  1,  # move_dir of 1 to move bullets upwards
                                  PLAYER_BULLET_MOVE_DIST)
    # Randomly shoot bullets from alien ships
    aliens_shoot(aliens)
    orphan_bullets = move_bullets(orphan_bullets, -1, ALIEN_BULLET_MOVE_DIST)

    # Detect bullet collisions with barriers
    player.bullets, all_barriers = detect_barrier_collision(player.bullets, all_barriers)
    for alien_row in aliens:
        for alien in alien_row:
            if alien is not None:
                alien.bullets, all_barriers = detect_barrier_collision(alien.bullets, all_barriers)
    orphan_bullets, all_barriers = detect_barrier_collision(orphan_bullets, all_barriers)

    # Detect bullet collision with alien ship
    count = 0
    for alien_row in aliens:
        for i in range(len(alien_row)):
            if alien_row[i] is not None:
                player.bullets, was_collision = detect_ship_collision(player.bullets, alien_row[i])
                # Alien ship destroyed!
                if was_collision:
                    # Save the alien ship's bullets so they don't just get stuck and hold still
                    orphan_bullets += alien_row[i].bullets
                    alien_row[i] = None
                    alien_ships_count -= 1
                    # increase score
                    scoreboard.add_points(20)
                    # Make alien bullets slightly more frequent
                    ALIEN_BULLET_FREQUENCY = int(ALIEN_BULLET_FREQUENCY * 0.98)
        count += 1
    # Check if player has won by destroying all the alien ships
    if alien_ships_count == 0:
        scoreboard.game_over_win()

    # Detect bullet collision with player ship
    was_collision = orphan_was_collision = False
    for alien_row in aliens:
        for alien in alien_row:
            if alien is not None:
                alien.bullets, was_collision = detect_ship_collision(alien.bullets, player)
                if was_collision:
                    break
        if was_collision:
            break
    orphan_bullets, orphan_was_collision = detect_ship_collision(orphan_bullets, player)
    # Check if player ship was hit
    if was_collision or orphan_was_collision:
        scoreboard.lose_life()
        clear_bullets(player.bullets, aliens)
        # Check if player is out of lives
        if scoreboard.lives == 0:
            scoreboard.game_over()
            player.hideturtle()
            game_is_on = False
        player.reset_pos((PLAYER_X_POS_START, PLAYER_Y_POS_START))


screen.exitonclick()
