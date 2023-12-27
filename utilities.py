import win32api, win32con
import time
import pyautogui

X_PADDING = 0
Y_PADDING = 0
sleeptimeSlow = 0.3
sleeptime = 0.08
sleeptimeQuick = 0.05

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(sleeptime)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def leftClickCord(cord):
    mousePos(cord)
    leftClick()

def leftDoubleClick():
    leftClick()
    time.sleep(sleeptimeQuick)
    leftClick()

def leftDoubleClickCord(cord):
    mousePos(cord)
    leftDoubleClick()
    
def mousePos(cord):
    win32api.SetCursorPos((X_PADDING + cord[0], Y_PADDING + cord[1]))
     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - X_PADDING
    y = y - Y_PADDING
    print ("current coordinates: " + str(x) + "," + str(y))
    return(x,y)

def scroll(dist):
    pyautogui.scroll(dist)

def main():
    print("x, y padding: " + str(X_PADDING) + ", " +  str(Y_PADDING))

if __name__ == '__main__':
    main()
