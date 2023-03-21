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


keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()




###############################
# ACTIONS
###############################

class Actions:

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
    
    # Leadership

    # Threads
    def leadershipMuteThread(self):

        print(self.getScalesObj())

        # Focus Hell Let Loose
        try:
            self.focusWindow()
            time.sleep(.2)
        except:
            print('HLL Window not found')
            self.commandRunning = False
            return
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (180, 567)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (816, 149)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (787, 420)
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
        
        # Focus Hell Let Loose
        try:
            self.focusWindow()
            time.sleep(.2)
        except:
            print('HLL Window not found')
            self.commandRunning = False
            return
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (180, 567)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (816, 149)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (840, 420)
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
        
        # Focus Hell Let Loose
        try:
            self.focusWindow()
            time.sleep(.2)
        except:
            print('HLL Window not found')
            self.commandRunning = False
            return
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (180, 567)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (816, 149)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (940, 420)
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
        try:
            self.focusWindow()
            time.sleep(.2)
        except:
            print('HLL Window not found')
            self.commandRunning = False
            return
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (180, 567)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (816, 149)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (787, 385)
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
        
        # Focus Hell Let Loose
        try:
            self.focusWindow()
            time.sleep(.2)
        except:
            print('HLL Window not found')
            self.commandRunning = False
            return
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (180, 567)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (816, 149)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (840, 385)
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
        
        # Focus Hell Let Loose
        try:
            self.focusWindow()
            time.sleep(.2)
        except:
            print('HLL Window not found')
            self.commandRunning = False
            return
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (180, 567)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (816, 149)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (940, 385)
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
        try:
            self.focusWindow()
            time.sleep(.2)
        except:
            print('HLL Window not found')
            self.commandRunning = False
            return
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (180, 567)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (816, 149)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (787, 355)
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
        
        # Focus Hell Let Loose
        try:
            self.focusWindow()
            time.sleep(.2)
        except:
            print('HLL Window not found')
            self.commandRunning = False
            return
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (180, 567)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (816, 149)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (840, 355)
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
        
        # Focus Hell Let Loose
        try:
            self.focusWindow()
            time.sleep(.2)
        except:
            print('HLL Window not found')
            self.commandRunning = False
            return
        # Esc
        keyboard.tap(Key.esc)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (180, 567)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (816, 149)
        time.sleep(self.sleepInterval)
        # Left click
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(self.sleepInterval)
        # Move mouse
        mouse.position = (1000, 355)
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
