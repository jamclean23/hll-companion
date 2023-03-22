# Actions to be triggered by hotkeys

##############################
# IMPORTS
##############################

from pynput.keyboard import Key
from pynput.mouse import Button
import pynput
import pygetwindow
import time
import threading
from multiprocessing.managers import BaseManager
import types

##############################
# LIBRARY ASSIGNMENT
##############################

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()


###############################
# GLOBAL VARS
###############################

resolution = types.SimpleNamespace()
resolution.x = 1920
resolution.y = 1080

preferences = types.SimpleNamespace()
# Leadership
preferences.leadership = types.SimpleNamespace()
preferences.leadership.low = 30
preferences.leadership.high = 70
# Unit
preferences.unit = types.SimpleNamespace()
preferences.unit.low = 30
preferences.unit.high = 70
# Proximity
preferences.proximity = types.SimpleNamespace()
preferences.proximity.low = 30
preferences.proximity.high = 70

###############################
# ACTIONS
###############################

class Actions:

    def percentToRatio(self, percentage):
        return (self.ratioScaleLength * (percentage / 100) + self.ratioScaleStart)

    def goToAudio(self):
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Move mouse to options
        mouse.position = (self.xRatioToPixel(.1005), self.yRatioToPixel(.51018))
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse to audio tab
        mouse.position = (self.xRatioToPixel(.4375), self.yRatioToPixel(.13981))
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)

    def xRatioToPixel(self, ratio):
        global resolution
        return round(resolution.x * ratio)        

    def yRatioToPixel(self, ratio):
        global resolution
        return round(resolution.y * ratio)
    
    def getScalesObj(self):
        manager = BaseManager(address=('localhost', 50000), authkey=b'blahkey')
        manager.connect()
        currentQueue = manager.getIpcQueue()

        if not currentQueue.empty():
            scaleValuesString = currentQueue.get()
            currentQueue.put(scaleValuesString)
            return self.parseScaleValuesString(scaleValuesString)

    def parseScaleValuesString(self, scaleValuesString):

        resultObj = types.SimpleNamespace()

        # Remove first character
        scaleValuesString = scaleValuesString[1:]
        # Remove last character
        scaleValuesString = scaleValuesString[:-1]

        elements = scaleValuesString.split('}{')
        for element in elements:
            splitElement = element.split(':{')
            name = splitElement[0]

            # Set attributes with names
            setattr(resultObj, name, types.SimpleNamespace())
            
            # Parse values
            # remove last character
            splitElement[1] = splitElement[1][:-1]
            # split
            valuePair = splitElement[1].split(',')
            # Assign values to new object, assign new object to result object
            setattr(vars(resultObj)[name], 'high', valuePair[0].split(':')[1])
            setattr(vars(resultObj)[name], 'low', valuePair[1].split(':')[1])
        return resultObj

    def focusWindow(self):
        winToBeFocused = pygetwindow.getWindowsWithTitle('Hell Let Loose')[0]
        winToBeFocused.activate()
    

    def focusHll(self):
        try:
            self.focusWindow()
            time.sleep(.2)
            return True
        except:
            print('HLL Window not found')
            self.commandRunning = False
            return False

    # Leadership

    # Threads
    def leadershipMuteThread(self):

        print(self.getScalesObj())

        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to leadership mute position
        mouse.position = (self.xRatioToPixel(.40989), self.yRatioToPixel(.38703))
        time.sleep(self.sleepInterval)
        # Left Click
        mouse.press(Button.left)
        mouse.release(Button.left)
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Report Action completed
        print('Action Complete')
        self.commandRunning = False

    def leadershipLowThread(self):
        global preferences
        
        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to leadership low position
        mouse.position = (self.xRatioToPixel(self.percentToRatio(preferences.leadership.low)), self.yRatioToPixel(.38703))
        time.sleep(self.sleepInterval)
        # Left Click
        mouse.press(Button.left)
        mouse.release(Button.left)
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Report Action completed
        print('Action Complete')
        self.commandRunning = False

    def leadershipHighThread(self):
        global preferences
        
        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to leadership high
        mouse.position = (self.xRatioToPixel(self.percentToRatio(preferences.leadership.high)), self.yRatioToPixel(.38703))
        time.sleep(self.sleepInterval)
        # Left Click
        mouse.press(Button.left)
        mouse.release(Button.left)
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Report Action completed
        print('Action Complete')
        self.commandRunning = False


    # Actions
    def leadershipMute(self):
        print('Setting leadership to mute')
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.leadershipMuteThread, daemon=True)
            newThread.start()
            self.commandRunning = True

    def leadershipLow(self):
        print('Setting leadership to low')
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.leadershipLowThread, daemon=True)
            newThread.start()
            self.commandRunning = True
    def leadershipHigh(self):
        print('Setting leadership to high')
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.leadershipHighThread, daemon=True)
            newThread.start()
            self.commandRunning = True

    # Unit

    # Threads
    def unitMuteThread(self):
        
        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to mute position
        mouse.position = (self.xRatioToPixel(.40989), self.yRatioToPixel(.35925))
        time.sleep(self.sleepInterval)
        # Left Click
        mouse.press(Button.left)
        mouse.release(Button.left)
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Report Action completed
        print('Action Complete')
        self.commandRunning = False

    def unitLowThread(self):
        global preferences

        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to low position
        mouse.position = (self.xRatioToPixel(self.percentToRatio(preferences.unit.low)), self.yRatioToPixel(.35925))
        time.sleep(self.sleepInterval)
        # Left Click
        mouse.press(Button.left)
        mouse.release(Button.left)
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Report Action completed
        print('Action Complete')
        self.commandRunning = False

    def unitHighThread(self):
        global preferences

        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to high position
        mouse.position = (self.xRatioToPixel(self.percentToRatio(preferences.unit.high)), self.yRatioToPixel(.35925))
        time.sleep(self.sleepInterval)
        # Left Click
        mouse.press(Button.left)
        mouse.release(Button.left)
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Report Action completed
        print('Action Complete')
        self.commandRunning = False


    # Actions
    def unitMute(self):
        print('Setting unit to mute')
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.unitMuteThread, daemon=True)
            newThread.start()
            self.commandRunning = True
    def unitLow(self):
        print('Setting unit to low')
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.unitLowThread, daemon=True)
            newThread.start()
            self.commandRunning = True
    def unitHigh(self):
        print('Setting unit to high')
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.unitHighThread, daemon=True)
            newThread.start()
            self.commandRunning = True

    # Proximity

    # Threads
    def proxMuteThread(self):
        
        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse
        mouse.position = (self.xRatioToPixel(.40989), self.yRatioToPixel(.33240))
        time.sleep(self.sleepInterval)
        # Left Click
        mouse.press(Button.left)
        mouse.release(Button.left)
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Report Action completed
        print('Action Complete')
        self.commandRunning = False

    def proxLowThread(self):
        global preferences

        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse
        mouse.position = (self.xRatioToPixel(self.percentToRatio(preferences.proximity.low)), self.yRatioToPixel(.33240))
        time.sleep(self.sleepInterval)
        # Left Click
        mouse.press(Button.left)
        mouse.release(Button.left)
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Report Action completed
        print('Action Complete')
        self.commandRunning = False

    def proxHighThread(self):
        global preferences

        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse
        mouse.position = (self.xRatioToPixel(self.percentToRatio(preferences.proximity.high)), self.yRatioToPixel(.33240))
        time.sleep(self.sleepInterval)
        # Left Click
        mouse.press(Button.left)
        mouse.release(Button.left)
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Report Action completed
        print('Action Complete')
        self.commandRunning = False


    # Actions
    def proxMute(self):
        print('Setting proximity to mute')
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.proxMuteThread, daemon=True)
            newThread.start()
            self.commandRunning = True
    def proxLow(self):
        print('Setting proximity to low')
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.proxLowThread, daemon=True)
            newThread.start()
            self.commandRunning = True
    def proxHigh(self):
        print('Setting proximity to high')
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.proxHighThread, daemon=True)
            newThread.start()
            self.commandRunning = True


    # Init

    def __init__(self):
        self.test = 'test'
        self.sleepInterval = .15
        self.commandRunning = False
        self.ratioScaleLength = .13281
        self.ratioScaleStart = .40989
        self.ratioScaleEnd = .54270
