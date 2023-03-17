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
            frontSlashHeld = False
            aposHeld = False
            rightBracketHeld = False
            periodHeld = False
            semicolonHeld = False
            leftBracketHeld = False
            commaHeld = False
            lHeld = False
            pHeld = False
            

            # Check to see if the key is in the list of held keys
            for element in self.heldKeys:

                # Characters
                if hasattr(element, 'char'):
                    if element.char == '/':
                        frontSlashHeld = True
                    if element.char == "'":
                        aposHeld = True
                    if element.char == ']':
                        rightBracketHeld = True
                    if element.char == '.':
                        periodHeld = True
                    if element.char == ';':
                        semicolonHeld = True
                    if element.char == '[':
                        leftBracketHeld = True
                    if element.char == ',':
                        commaHeld = True
                    if element.char == 'l':
                        lHeld = True
                    if element.char == 'p':
                        pHeld = True

            
            # Check for held key combos here

            # Leadership
            if frontSlashHeld:
                print('Leadership Mute')
            if aposHeld:
                print('Leadership Low')
            if rightBracketHeld:
                print('Leadership High')


        def onRelease(self, key):
            # Remove elements from list as they are released
            for element in self.heldKeys:
                if element == key:
                    self.heldKeys.remove(key)

            # Trigger altup event if key released is alt
            if key == keyboard.Key.alt_gr:
                self.AltUp()

        def win32_event_filterKey(self, msg, data):

            self.keyListener._suppress = False
            if not (data.vkCode == 165 and msg == 260):
                self.keyListener._suppress = True


        def listen(self):
            print('Listener started')
            self.keyListenerThreads += 1
            print('Key Listener Threads:' + str(self.keyListenerThreads))


            with keyboard.Listener(
                on_press=self.onPress,
                on_release=self.onRelease,
                win32_event_filter=self.win32_event_filterKey
                ) as self.keyListener:
                self.keyListener.join()
        

        def checkIfAlt(self, key):
    
            # Check if right alt
            if key == keyboard.Key.alt_gr:
                # If right alt was not already being held, start a new thread
                if self.heldRightAlt == False:
                    keyThread = threading.Thread(target=self.listen, daemon=True)
                    keyThread.start()
                    self.heldRightAlt = True


        def AltUp(self):
            # clear heldRightAlt if a right alt keyup is detected, and stop the key listening thread
            self.heldRightAlt = False
            self.keyListener.stop()
            self.keyListenerThreads -= 1
            print('Listener stopped')
            print('Key listener threads:' + str(self.keyListenerThreads))

        def win32_event_filterAlt(self, msg, data):
            ph = 'ph'

            self.altListener._suppress = False            
            if (msg == 260 and data.vkCode == 165):
                self.altListener._suppress = True

        def startAltListen(self):
            with keyboard.Listener(
                on_press=self.checkIfAlt,
                win32_event_filter=self.win32_event_filterAlt
                ) as self.altListener:
                self.altListener.join()

        def __init__(self):
            newThread = threading.Thread(target=self.startAltListen, daemon=True)
            newThread.start()
            self.keySender = keyboard.Controller()
            self.heldKeys = []
            self.heldRightAlt = False
            self.keyListenerThreads = 0

    KeyboardListener()