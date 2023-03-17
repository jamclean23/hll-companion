# Keyboard listeners

##############################
# IMPORTS
##############################
import pygetwindow
from pynput import keyboard
import threading


##############################
# SET UP KEYBOARD LISTENERS
##############################

def initListener():
    class KeyboardListener:
        def focusWindow(self):
            winToBeFocused = pygetwindow.getWindowsWithTitle('Hell Let Loose')[0]
            winToBeFocused.activate()

        def onPress(self, key):
            # If key does not exist in heldKeys, add it to the list
            addKey = True
            for element in self.heldKeys:
                if element == key:
                    addKey = False
            if addKey:
                self.heldKeys.append(key)

            # DEFINE HOTKEYS HERE

            # Declare the key to a variable
            rightAltHeld = False
            frontSlashHeld = False
            commaHeld = False
            rightBracketHeld = False

            # Check to see if the key is in the list of held keys
            for element in self.heldKeys:

                # Characters
                if hasattr(element, 'char'):
                    if element.char == '/':
                        frontSlashHeld = True
                    if element.char == "'":
                        commaHeld = True
                    if element.char == ']':
                        rightBracketHeld = True

                # Special keys
                else:
                    if element.alt_gr:
                        rightAltHeld = True
            
            # Conditionally check for held key combos here

            if rightAltHeld and frontSlashHeld:
                print('Leadership Mute')
            
            if rightAltHeld and commaHeld:
                print('Leadership Low')
            
            if rightAltHeld and rightBracketHeld:
                print('Leadership High')


        def onRelease(self, key):
            # self.heldKeys = list(filter((key).__ne__, self.heldKeys))
            for element in self.heldKeys:
                if element == key:
                    self.heldKeys.remove(key)

        def listen(self):
            with keyboard.Listener(
                on_press=self.onPress,
                on_release=self.onRelease
                ) as listener:
                listener.join()
        
        def __init__(self):
            newThread= threading.Thread(target=self.listen, daemon=True)
            newThread.start()
            self.heldKeys = []
    keyboardListener = KeyboardListener()