import pyautogui
from pynput import mouse, keyboard
# print(pyautogui.displayMousePosition())

mousePosition = (0,0)
keyPressed = None

def on_press(key):
    global keyPressed
    try:
        # print('alphanumeric key {0} pressed'.format(key.char))
        keyPressed = key
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    # print('{0} released'.format(key))
    global keyPressed
    keyPressed = None
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def on_move(x, y):
    # print('Pointer moved to {0}'.format((x, y)))
    global mousePosition
    mousePosition = (x,y)

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))


def startListening():
    # ...or, in a non-blocking fashion:
    KBlistener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    KBlistener.start()

    Mlistener = mouse.Listener(
        on_move=on_move,
        # on_click=on_click)
        )
    Mlistener.start()