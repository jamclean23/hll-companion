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
import os

##############################
# LIBRARY ASSIGNMENT
##############################

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()


###############################
# GLOBAL VARS
###############################

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

    def setLogMessage(self, message, mode='write'):
        manager = BaseManager(address=('localhost', 50000), authkey=b'blahkey')
        manager.connect()
        currentQueue = manager.getLogMessage()
        currentQueue.put(message + '\\n' + mode)

    def parseSettingsString(self, settingsString):
        resultObj = types.SimpleNamespace()

        # Remove first bracket
        settingsString = settingsString[1:]
        # Remove last bracket
        settingsString = settingsString[:-1]

        # Split objects
        objectsStrings = settingsString.split('][')

        for obj in objectsStrings:
            newObj = obj
            # Check if first character is a bracket and remove
            if newObj[1] == '[':
                newObj = obj[1:]
            if newObj[-1] == ']':
                newObj = obj[:-1]
            

            # Split category name and assign to result
            catName = newObj.split(':{')[0]
            setattr(resultObj, catName, types.SimpleNamespace())
            
            # Remove last curly brace of value pairs
            valuePairs = newObj.split(':{')[1]
            if valuePairs[-1] == '}':
                valuePairs = valuePairs[:-1]
            
            # Split into individual pairs
            indvPairs = valuePairs.split(',')
            
            # Split into key value pairs
            for pair in indvPairs:
                keyValueList = pair.split(':')
                # Assign attribute to category
                setattr(getattr(resultObj, catName), keyValueList[0], keyValueList[1])
            return resultObj

    def updateResolution(self):
        # Read and parse settings.txt
        settingsFile = open(self.settingsPath, 'r')
        settingsObj = self.parseSettingsString(settingsFile.read())

        # Assign to self.resolution
        self.resolution.x = int(settingsObj.resolution.x)
        self.resolution.y = int(settingsObj.resolution.y) 

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
        return round(self.resolution.x * ratio)        

    def yRatioToPixel(self, ratio):
        return round(self.resolution.y * ratio)
    
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
            print('HLL Window Found')
            time.sleep(.4)
            return True
        except:
            self.setLogMessage('HLL window not found')
            print('HLL Window not found')
            self.commandRunning = False
            return False

    # Leadership

    # Threads
    def leadershipMuteThread(self):

        # Focus Hell Let Loose
        if not self.focusHll():
            return
        

        # Go to audio tab
        self.goToAudio()

        # Move mouse to leadership mute position
        mouse.position = (self.xRatioToPixel(self.ratioScaleStart), self.yRatioToPixel(.38703))
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

        try:
            scalesValues = self.getScalesObj()
            lowValue = int(scalesValues.LeadershipVoiceVolume.low)
        except:
            lowValue = int(preferences.leadership.low)

        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to leadership low position
        mouse.position = (self.xRatioToPixel(self.percentToRatio(lowValue)), self.yRatioToPixel(.38703))
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

        try:
            scalesValues = self.getScalesObj()
            highValue = int(scalesValues.LeadershipVoiceVolume.high)
        except:
            highValue = int(preferences.leadership.high)
  
        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to leadership high
        mouse.position = (self.xRatioToPixel(self.percentToRatio(highValue)), self.yRatioToPixel(.38703))
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
        if self.commandRunning == False:
            self.setLogMessage('Setting Leadership to Mute...')
            print('Setting leadership to mute')
            self.updateResolution()
            newThread = threading.Thread(target=self.leadershipMuteThread, daemon=True)
            newThread.start()
            self.commandRunning = True
        else:
            print('Other command running')

    def leadershipLow(self):
        if self.commandRunning == False:
            self.updateResolution()
            self.setLogMessage('Setting Leadership to Low')
            print('Setting leadership to low')
            newThread = threading.Thread(target=self.leadershipLowThread, daemon=True)
            newThread.start()
            self.commandRunning = True
        else:
            print('Other command running')
    def leadershipHigh(self):
        if self.commandRunning == False:
            self.setLogMessage('Setting Leadership to High')
            print('Setting leadership to high')
            self.updateResolution()
            newThread = threading.Thread(target=self.leadershipHighThread, daemon=True)
            newThread.start()
            self.commandRunning = True
        else:
            print('Other command running')

    # Unit

    # Threads
    def unitMuteThread(self):
        
        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to mute position
        mouse.position = (self.xRatioToPixel(self.ratioScaleStart), self.yRatioToPixel(.35925))
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

        try:
            scalesValues = self.getScalesObj()
            lowValue = int(scalesValues.UnitVoiceVolume.low)
        except:
            lowValue = int(preferences.unit.low)
        print(lowValue)
        
        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to low position
        mouse.position = (self.xRatioToPixel(self.percentToRatio(lowValue)), self.yRatioToPixel(.35925))
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

        try:
            scalesValues = self.getScalesObj()
            highValue = int(scalesValues.UnitVoiceVolume.high)
        except:
            highValue = int(preferences.unit.high)
        print(highValue)
  
        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to high position
        mouse.position = (self.xRatioToPixel(self.percentToRatio(highValue)), self.yRatioToPixel(.35925))
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
        self.updateResolution()
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.unitMuteThread, daemon=True)
            newThread.start()
            self.commandRunning = True
    def unitLow(self):
        print('Setting unit to low')
        self.updateResolution()
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.unitLowThread, daemon=True)
            newThread.start()
            self.commandRunning = True
    def unitHigh(self):
        print('Setting unit to high')
        self.updateResolution()
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
        mouse.position = (self.xRatioToPixel(self.ratioScaleStart), self.yRatioToPixel(.33240))
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

        try:
            scalesValues = self.getScalesObj()
            lowValue = int(scalesValues.ProximityVoiceVolume.low)
        except:
            lowValue = int(preferences.proximity.low)
        print(lowValue)
        
        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse to proximity low position
        mouse.position = (self.xRatioToPixel(self.percentToRatio(lowValue)), self.yRatioToPixel(.33240))
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

        try:
            scalesValues = self.getScalesObj()
            highValue = int(scalesValues.ProximityVoiceVolume.high)
        except:
            highValue = int(preferences.proximity.high)
        print(highValue)
  
        # Focus Hell Let Loose
        if not self.focusHll():
            return

        # Go to audio tab
        self.goToAudio()

        # Move mouse
        mouse.position = (self.xRatioToPixel(self.percentToRatio(highValue)), self.yRatioToPixel(.33240))
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
        self.setLogMessage('Setting Proximity to Mute')
        print('Setting proximity to mute')
        self.updateResolution()
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.proxMuteThread, daemon=True)
            newThread.start()
            self.commandRunning = True
    def proxLow(self):
        self.setLogMessage('Setting Proximity to Low')        
        print('Setting proximity to low')
        self.updateResolution()
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.proxLowThread, daemon=True)
            newThread.start()
            self.commandRunning = True
    def proxHigh(self):
        self.setLogMessage('Setting Proximity to High')        
        print('Setting proximity to high')
        self.updateResolution()
        if self.commandRunning == False:
            newThread = threading.Thread(target=self.proxHighThread, daemon=True)
            newThread.start()
            self.commandRunning = True


    # Init

    def __init__(self):
        self.test = 'test'
        self.sleepInterval = .12
        self.commandRunning = False
        self.ratioScaleLength = .13281
        self.ratioScaleStart = .40989
        self.ratioScaleEnd = .54270
        self.resolution = types.SimpleNamespace()
        self.resolution.x = 1920
        self.resolution.y = 1080
        self.storagePath = os.path.join(os.getenv('LOCALAPPDATA'), 'hll-companion')
        self.settingsPath = os.path.join(self.storagePath, 'settings.txt')