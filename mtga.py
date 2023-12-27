from PIL import ImageGrab, ImageOps
import speech
import utilities
import time

CARDS_LEFT = 189
CARDS_RIGHT = 1350
CARDS_Y = 915

PIXEL_OFFSET = 15
SLEEP_TIME = 0.4
RESOLUTION_SCALING = 0.798958

debug = False



'''
click on nth playable (highlighted) card on the screen
1-based numbering system
'''
def click_card_x(card_num):
    if card_num < 1:
        raise ValueError("Need positive card number")
    cards = get_card_coordinates()
    if len(cards) < card_num:
        raise ValueError("Card number too large - not enough playable cards: " + str(cards) + " " + str(card_num))
    else:
        card_x = cards[card_num - 1] + PIXEL_OFFSET
        card_x = int((card_x+0.0) * RESOLUTION_SCALING)
        card_y = CARDS_Y = CARDS_Y * RESOLUTION_SCALING
        if debug:
            print("card click: " + card_x + " " + card_y)
        utilities.leftDoubleClickCord((card_x, card_y))
    time.sleep(SLEEP_TIME)

'''
get x-coordinates of playable on-screen cards by looking for blue highlighted outline
'''
def get_card_coordinates():
    screen = ImageGrab.grab()
    card_xs = []
    i = CARDS_LEFT
    while i < CARDS_RIGHT:
        pixel = screen.getpixel((i, CARDS_Y))
        # check for blue highlight next to card
        if pixel[0] <2 and pixel[1] > 200 and pixel[2] > 200:
            card_xs.append(i)
            i += PIXEL_OFFSET
        i += 1
    return card_xs
