import time
import pyautogui
import webbrowser
from PIL import Image, ImageOps
import numpy as np
import mss.tools

"""

NOTE: You must be offline for this to work!

"""

GOOGLE_URL = "https://google.com"
CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
DAY_MODE = True  # game starts in day mode

webbrowser.get(CHROME_PATH).open(GOOGLE_URL)
time.sleep(1)


# Start game
def start_game():
    """ Start the game by opening Chrome, locating and clicking the dino, and pressing space.
        :return: Tuple of x,y coordinates representing dino's starting position.
    """
    try:
        x, y = pyautogui.locateCenterOnScreen('images/dino.png', confidence=0.8)
    # Detect if user is not offline so dino game can't be accessed
    except TypeError:
        raise SystemExit("Error: Make sure you are offline.")
    # For some reason on my Mac I needed to divide these values by 2
    # to get it to work correctly
    start_dino_x = x / 2
    start_dino_y = y / 2
    pyautogui.moveTo(start_dino_x, start_dino_y)
    time.sleep(0.5)
    pyautogui.click()  # clicks on dino to put the game window into focus
    time.sleep(0.5)
    pyautogui.press('space')  # starts game
    # Dino moves 20 to the right once game starts
    start_dino_x += 20
    return start_dino_x, start_dino_y


def get_screengrab_top_color(x, width):
    """ Take a screengrab of the area in front of the dino to check for obstacles.
        :return: Tuple consisting of:
                   - int representing top grayscale color in the image
                   - int representing count of pixels of top_color
    """
    global img_area

    # region of which to grab screenshot
    region = {'top': dino_y - 15, 'left': x, 'width': width, 'height': 30}
    sct_img = sct.grab(region)  # capture screenshot of given region
    image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw")
    image = ImageOps.grayscale(image)  # PIL image object, mode L
    # capture and save the screenshot image area
    img_area = image.size[0] * image.size[1]
    a = np.array(image.getcolors())
    # get maximum pixel count, which will indicate most common color in the image
    top_color_count = np.amax(a.T[0])
    for i in a:
        if i[0] == top_color_count:
            # get most common color (the color with the max pixel count)
            top_color = i[1]
            break
    return top_color, top_color_count


keep_playing = True
dino_x, dino_y = start_game()
time.sleep(2)
# Note: This value is for regular (faster) version of the game.
# For the slow version of the game, a lower value of ~16 works better.
screengrab_x = dino_x + 35  # how far to the right of the dino to start the screenshot
screengrab_width = 75
sct = mss.mss()
img_area = None

# Initial screengrab of area in front of dino
initial_top_color, initial_top_color_count = get_screengrab_top_color(screengrab_x, screengrab_width)

# Run game in infinite loop
while True:
    # Grab screengrab of area in front of dino so it can be checked for obstacles
    top_color, top_color_count = get_screengrab_top_color(screengrab_x, screengrab_width)

    # Detect transition from day mode to night mode
    if DAY_MODE and top_color < 250:
        DAY_MODE = False
        initial_night_top_color_count = top_color_count
        initial_night_top_color = top_color
    # Detect transition from night mode back to day mode
    elif not DAY_MODE and top_color == 255:
        DAY_MODE = True
        initial_top_color_count = top_color_count
        initial_top_color = top_color
    # Detect cactus - If found, press space to jump
    elif (DAY_MODE and top_color == 255 and top_color_count < initial_top_color_count) or (not DAY_MODE and top_color < 200 and top_color_count < ((img_area * 0.25) * 0.95)):
        pyautogui.press('space')
