##############################
# IMPORTS
##############################

from tkinter import *
import os
import pygetwindow
from pynput import keyboard
import threading
import time


##############################
# SET UP KEYBOARD LISTENERS
##############################

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



##############################
# DATA MANIPULATION
##############################

# Declare data storage class
class ParsedObj:
        def __init__(self, option, value):
             self.option = option
             self.value = value

# Retrieve data from game ini and store in levelsData
def getData(levelsData):
    levelsData.clear()
    # Read ini file and assign to list
    f = open(os.path.expanduser('~') + '\\AppData\\Local\\HLL\\Saved\\Config\\WindowsNoEditor\\GameUserSettings.ini')
    lines = f.readlines()

    # Function for parsing read data
    def parseData(lines, levelsData):
        for i in range(len(lines)):
            parsed = lines[i].rsplit("=")

            if parsed[0] == "ProximityVoiceVolume" or parsed[0] == "UnitVoiceVolume" or parsed[0] == "LeadershipVoiceVolume":
                levelsData.append(ParsedObj(parsed[0], parsed[1]))
        return levelsData
    levelsData = parseData(lines, levelsData)
    return levelsData
levelsData = []
levelsData = getData(levelsData)


###############################
# RENDER PROCESS
###############################

# Render a window and display data

def render():

    ##############################
    # Event Handlers
    ##############################


    def handleUpdateClick(levelsData, frames):
        #  Refresh levels data
        levelsData = getData(levelsData)

        # Update height of meters
        def updateMeter(levelsData, frames):
            i = 0
            for frame in frames:
                # Set meter height
                meterHeight = round(float(levelsData[i].value) * 100)
                frame.config(height=meterHeight)
                i += 1

                # Set color of meter according to meterHeight
                if meterHeight > 75:
                    meterColor = 'green'
                elif meterHeight < 76 and meterHeight > 50:
                    meterColor = 'yellow'
                elif meterHeight < 51 and meterHeight > 25:
                    meterColor = 'orange'
                elif meterHeight < 26:
                    meterColor = 'red'
                frame.config(bg=meterColor)
        updateMeter(levelsData, frames) 
        
    ###############################
    # Set up window
    ###############################
    root = Tk()
    root.geometry('400x200')
    root.title('HLL Assistant')
    root.configure(background='black')
    root.resizable(False, False)

    # Set up update function
    def update(levelsData, frames):
        handleUpdateClick(levelsData, frames)
        root.after(2000, lambda: update(levelsData, frames))

    # Render meters frame
    metersFrame = Frame(root, bg='gray30')
    metersFrame.pack()
    metersFrame.place(bordermode=OUTSIDE, anchor='nw', height=150, width=380, x=10, y=10)

    # Render meters
    def renderMeters(levelsData):
        frames = []
        i = 0
        for dataObj in levelsData:
            # Determine height of meter according to levels
            meterHeight = round(float(dataObj.value) * 100)

            # Set color of meter according to meterHeight
            if meterHeight > 75:
                 meterColor = 'green'
            elif meterHeight < 76 and meterHeight > 50:
                 meterColor = 'yellow'
            elif meterHeight < 51 and meterHeight > 25:
                 meterColor = 'orange'
            elif meterHeight < 26:
                 meterColor = 'red'

            # Create meters
            frame = Frame(metersFrame, bg=meterColor, height=meterHeight)
            frame.pack() 
            frame.place(bordermode=OUTSIDE, anchor='sw', width=40, x=70 + (i * 100), y=110)
            frames.append(frame)
            i += 1
        return frames
    frames = renderMeters(levelsData)

    # Render Labels
    def renderLabels(levelsData):
        i = 0
        for dateObj in levelsData:
             label = Label(metersFrame, relief='ridge', text=dateObj.option.split('Voice')[0], padx=5, pady=3)
             label.pack()
             label.place(bordermode=OUTSIDE, anchor='center', x=90 + (i * 100), y=130)
             i += 1
    renderLabels(levelsData)
    
    # call update function
    root.after(2000, lambda: update(levelsData, frames))
    root.mainloop()

render()




