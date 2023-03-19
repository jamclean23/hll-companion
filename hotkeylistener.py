# Keyboard listeners

##############################
# IMPORTS
##############################
from pynput import keyboard as Keyboard
import threading
import actions

Actions = actions.Actions()

##############################
# SET UP KEYBOARD LISTENERS
##############################

def initListener():

    class KeyboardListener:


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
            tHeld = False
            

            # Check to see if the key is in the list of held keys
            for element in self.heldKeys:

                # Characters
                if hasattr(element, 'char'):
                    if element.char == 't':
                        tHeld = True
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

            if self.actionOngoing == False:

                # Leadership
                if frontSlashHeld:
                    self.actionOngoing = True
                    self.nextAction = Actions.leadershipMute
                elif aposHeld:
                    self.actionOngoing = True
                    self.nextAction = Actions.leadershipLow
                elif rightBracketHeld:
                    self.actionOngoing = True
                    self.nextAction = Actions.leadershipHigh
                
                # Unit
                elif periodHeld:
                    self.actionOngoing = True
                    self.nextAction = Actions.unitMute
                elif semicolonHeld:
                    self.actionOngoing = True
                    self.nextAction = Actions.unitLow
                elif leftBracketHeld:
                    self.actionOngoing = True
                    self.nextAction = Actions.unitHigh

                # Proximity
                elif commaHeld:
                    self.actionOngoing = True
                    self.nextAction = Actions.proxMute
                elif lHeld:
                    self.actionOngoing = True
                    self.nextAction = Actions.proxLow
                elif pHeld:
                    self.actionOngoing = True
                    self.nextAction = Actions.proxHigh

                # Test
                elif tHeld:
                    print(Actions.test)
                    self.actionOngoing = True
                

        def onRelease(self, key):
            # Remove elements from list as they are released
            for element in self.heldKeys:
                if element == key:
                    self.heldKeys.remove(key)

            # Trigger altup event if key released is alt
            if key == Keyboard.Key.alt_gr:
                self.AltUp()

        def win32_event_filterKey(self, msg, data):

            self.keyListener._suppress = False
            if not (data.vkCode == 165 and msg == 260):
                self.keyListener._suppress = True


        def listen(self):
            self.keyListenerThreads += 1

            with Keyboard.Listener(
                on_press=self.onPress,
                on_release=self.onRelease,
                win32_event_filter=self.win32_event_filterKey
                ) as self.keyListener:
                self.keyListener.join()
        

        def checkIfAlt(self, key):
    
            # Check if right alt
            if key == Keyboard.Key.alt_gr:
                # If right alt was not already being held, start a new thread
                if self.heldRightAlt == False:
                    self.actionOngoing = False
                    keyThread = threading.Thread(target=self.listen, daemon=True)
                    keyThread.start()
                    self.heldRightAlt = True


        def AltUp(self):
            # clear heldRightAlt if a right alt keyup is detected, and stop the key listening thread
            self.heldRightAlt = False
            self.keyListener.stop()
            self.keyListenerThreads -= 1
            self.nextAction()
            self.nextAction = 'none'

        def win32_event_filterAlt(self, msg, data):
            # Suppress normal operation of right alt key
            self.altListener._suppress = False            
            if (msg == 260 and data.vkCode == 165):
                self.altListener._suppress = True

        def startAltListen(self):
            with Keyboard.Listener(
                on_press=self.checkIfAlt,
                win32_event_filter=self.win32_event_filterAlt
                ) as self.altListener:
                self.altListener.join()

        def __init__(self):
            newThread = threading.Thread(target=self.startAltListen, daemon=True)
            newThread.start()
            self.keySender = Keyboard.Controller()
            self.heldKeys = []
            self.heldRightAlt = False
            self.keyListenerThreads = 0
            self.actionOngoing = False
            self.nextAction = ''

    KeyboardListener()