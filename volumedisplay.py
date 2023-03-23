# Tkinter gui window

##############################
# IMPORTS
##############################

from tkinter import *
import os
from PIL import ImageTk, Image  
from multiprocessing.managers import BaseManager
import types
import sys
import threading

##############################
# Global Variables
##############################

ipcQueueItems = []
storagePath = os.path.join(os.getenv('LOCALAPPDATA'), 'hll-companion')
settingsPath = os.path.join(storagePath, 'settings.txt')
scalesPositionsPath = os.path.join(storagePath, 'sliders.txt')

##############################
# INITIALIZE WINDOW
##############################

def initGui():
    ##############################
    # DATA MANIPULATION
    ##############################

    def getPath(filename):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, filename)
        else: 
            return filename

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

    # Set up Local Storage
    def createSettingsFile():
        print('Creating Settings file')
        settingsFile = open(settingsPath, 'w')
        settingsFile.write('[resolution:{x:1920,y:1080}]')

    def createSlidersFile():
        print('Creatings sliders.txt...')
        slidersFile = open(scalesPositionsPath, 'w')
        slidersFile.write('{ProximityVoiceVolume:{high:70,low:30}}{UnitVoiceVolume:{high:70,low:30}}{LeadershipVoiceVolume:{high:70,low:30}}')

    def initLocal():
        # If no folder, create folder
        if os.path.exists(storagePath):
            print('Storage present')
        else:
            print('Storage not found, creating...')
            os.mkdir(storagePath)

        # # If no settings file, create settings file
        if os.path.isfile(settingsPath):
            print('Settings file found')
        else:
            print('Settings file not found')
            createSettingsFile()
        
        # # if no scalesPositions file, create scalesPosition file
        if os.path.isfile(scalesPositionsPath):
            print('sliders.txt found')
        else:
            print('sliders.txt not found')
            createSlidersFile()
    initLocal()

    def parseSettingsString(settingsString):
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

    def parseScaleValuesString(scaleValuesString):

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
    

    ###############################
    # RENDER PROCESS
    ###############################

    # Render a window and display data

    def render():

        ##############################
        # Event Handlers
        ##############################

        # Reset ipcQueueItems
        def resetQueueItems():
            global ipcQueueItems
            ipcQueueItems = []

        # Add to ipcQueueItems
        def updateQueue(newItem):
            global ipcQueueItems

            # Add item
            ipcQueueItems.append(newItem)

            # Send to multiprocess queue
            manager = BaseManager(address=('localhost', 50000), authkey=b'blahkey')
            manager.connect()

            currentQueue = manager.getIpcQueue()
            
            if not currentQueue.empty():
                currentQueue.get()
                
            currentQueue.put(newItem)

            # Reset Queue
            resetQueueItems()

        # Serialize scales values
        def serializeScalesValues(scales):

            scalesValuesString = ''
            for scale in scales:
                # Start Item
                scalesValuesString += '{'
                # name
                scalesValuesString += scale.option
                # Start object
                scalesValuesString += ':{'
                # High value
                scalesValuesString += 'high:' + str(scale.highScale.get()) + ','
                # Low value
                scalesValuesString += 'low:' + str(scale.lowScale.get())
                # End object
                scalesValuesString += '}'
                # Close item
                scalesValuesString += '}'
            return scalesValuesString

        # Update Scales Values
        def updateScalesValues(scales):
            scalesValuesString = serializeScalesValues(scales)
            file = open(scalesPositionsPath, 'w')
            file.write(scalesValuesString)
            updateQueue(scalesValuesString)

        def handleUpdateClick(levelsData, frames):
            #  Refresh levels data
            levelsData = getData(levelsData)

            # Update height of meters
            def updateMeter(levelsData, frames):
                i = 0
                for frame in frames:
                    # Set meter height
                    meterHeight = round(float(levelsData[i].value) * 100)


                    # Set color of meter according to meterHeight
                    if meterHeight > 75:
                        meterColor = 'green'
                    elif meterHeight < 76 and meterHeight > 50:
                        meterColor = 'yellow'
                    elif meterHeight < 51 and meterHeight > 25:
                        meterColor = 'orange'
                    elif meterHeight < 26:
                        meterColor = 'red'
                
                    if meterHeight == 0:
                        meterHeight = 100
                        meterColor = 'gray20'

                    # Send Options
                    frame.config(bg=meterColor)
                    frame.config(height=meterHeight)

                    i += 1
            updateMeter(levelsData, frames) 
            
        ###############################
        # Set up window
        ###############################
        root = Tk()
        root.geometry('400x330')
        root.title('HLL Companion')
        root.configure(background='gray30')
        root.resizable(False, False)
        root.wm_iconbitmap(getPath('tank.ico'))

        # Get Settings from settings txt and parse to object
        def getSettingsObj():
            settingsFile = open(settingsPath, 'r')
            return parseSettingsString(settingsFile.read())

        # Set the log message
        def setLogMessage(message, mode='write'):
            manager = BaseManager(address=('localhost', 50000), authkey=b'blahkey')
            manager.connect()
            currentQueue = manager.getLogMessage()
            currentQueue.put(message + '\\n' + mode)

        # Update log from ipc 
        def updateLogMessage(log):

            def startLogUpdateThread(log):
                manager = BaseManager(address=('localhost', 50000), authkey=b'blahkey')
                manager.connect()
                currentQueue = manager.getLogMessage()
                
                if currentQueue.empty() == False:
                    queueString = currentQueue.get()
                    receivedMessage = queueString.split('\\n')[0]
                    receivedMode = queueString.split('\\n')[1]
                    if receivedMode == 'write':
                        message = receivedMessage
                    elif receivedMode == 'append':
                        message = log.cget("text") + receivedMessage
                    else:
                        message = ''
                    log.config(text=message)

            newThread = threading.Thread(target=lambda: startLogUpdateThread(log), daemon=True)
            newThread.start()

        # Set up update function
        def update(levelsData, frames, log):
            handleUpdateClick(levelsData, frames)
            updateLogMessage(log)
            root.after(500, lambda: update(levelsData, frames, log))

        # Render meters frame
        metersFrame = Frame(root, bg='gray10', relief='ridge', bd=2)
        metersFrame.pack()
        metersFrame.place(bordermode=INSIDE, anchor='nw', height=120, width=380, x=10, y=10)

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
                frame.place(bordermode=OUTSIDE, anchor='sw', width=40, x=70 + (i * 100), y=115)
                frames.append(frame)
                i += 1
            return frames
        frames = renderMeters(levelsData)

        # Render Labels
        def renderLabels(levelsData):
            i = 0
            for dateObj in levelsData:
                label = Label(root, relief='ridge', text=dateObj.option.split('Voice')[0], padx=5, pady=3)
                label.pack()
                label.place(bordermode=OUTSIDE, anchor='center', x=100 + (i * 100), y=150)
                i += 1
        renderLabels(levelsData)

        
        # Render Scales
        def renderScales(levelsData):
            scalesFile = open(scalesPositionsPath, 'r')
            scalesValues = parseScaleValuesString(scalesFile.read())
            print(scalesValues)

            scales = []
            i = 0
            for dateObj in levelsData:
                
                # Get starting values from local storage file
                if dateObj.option == 'LeadershipVoiceVolume':
                    highValue = scalesValues.LeadershipVoiceVolume.high
                    lowValue = scalesValues.LeadershipVoiceVolume.low
                elif dateObj.option == 'UnitVoiceVolume':
                    highValue = scalesValues.UnitVoiceVolume.high
                    lowValue = scalesValues.UnitVoiceVolume.low
                elif dateObj.option == 'ProximityVoiceVolume':
                    highValue = scalesValues.ProximityVoiceVolume.high
                    lowValue = scalesValues.ProximityVoiceVolume.low
                
                # High Sliders
                dateObj.highScale = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=75, label='      High')
                dateObj.highScale.bind("<ButtonRelease-1>", lambda event : updateScalesValues(scales))
                dateObj.highScale.pack()
                dateObj.highScale.set(highValue)
                dateObj.highScale.place(anchor='center', x=100 + (i * 100), y=195)

                # Low Sliders
                dateObj.lowScale = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=75, label='      Low')
                dateObj.lowScale.bind("<ButtonRelease-1>", lambda event : updateScalesValues(scales))
                dateObj.lowScale.pack()
                dateObj.lowScale.set(lowValue)
                dateObj.lowScale.place(anchor='center', x=100 + (i * 100), y=255)

                scales.append(dateObj)

                i += 1
            return scales
        scales = renderScales(levelsData)
        # On app mount update
        updateScalesValues(scales)

        ###################################################
        # SETTINGS MODAL
        ###################################################

        def startSettingsModal():

            # Local Storage
            savedSettings = getSettingsObj()

            # Placeholder values, to be replaced by reading from config file in local storage
            savedHeight = StringVar()
            savedHeight.set(savedSettings.resolution.y)

            savedWidth = StringVar()
            savedWidth.set(savedSettings.resolution.x)

            # Create frame and overlay
            settingsFrame = Frame(root, background='gray50')
            settingsFrame.pack()
            settingsFrame.place(height=330, width=400)

            # Resolution Settings
            resFrame = Frame(settingsFrame, relief='ridge')
            resFrame.pack()
            resFrame.place(anchor='nw', width=150, height=75, x=20, y=20)

            # Resolution label
            resNameLbl = Label(resFrame, text='Resolution')
            resNameLbl.pack(side=TOP)

            # Width label
            resXLbl = Label(resFrame, text='Width:')
            resXLbl.pack()
            resXLbl.place(anchor='ne', x=50, y=20)

            # Width spinbox
            resXSpin = Spinbox(resFrame, from_=0, to=3840, width=5, textvariable=savedWidth)
            resXSpin.pack()
            resXSpin.place(anchor='nw', x=95, y=22)

            # Height label
            resYLbl = Label(resFrame, text='Height:')
            resYLbl.pack()
            resYLbl.place(anchor='ne', x=50, y=40)

            # Height spinbox
            resYSpin = Spinbox(resFrame, from_=0, to=2160, width=5, textvariable=savedHeight)
            resYSpin.pack()
            resYSpin.place(anchor='nw', x=95, y=42)

            def handleOKSettingsModal(settingsFrame):
                stringToWrite = '['

                # Serialize resolution settings
                stringToWrite += 'resolution:{'
                # Width
                stringToWrite += 'x:' + savedWidth.get()
                # New Item
                stringToWrite += ','
                # Height
                stringToWrite += 'y:' + savedHeight.get() + '}'

                # Close String
                stringToWrite += ']'

                # Write to file
                settingsFile = open(settingsPath, 'w')
                settingsFile.write(stringToWrite)

                # Remove Gui
                settingsFrame.destroy()

            # Render Ok button
            okBtn = Button(settingsFrame, text='OK', command=lambda: handleOKSettingsModal(settingsFrame))
            okBtn.pack()
            okBtn.place(anchor='center', width=75, height=25, x=150, y=300)

            # Update log
            setLogMessage('Settings Saved')

            def handleCancelSettingsModal(settingsFrame):
                settingsFrame.destroy()
                setLogMessage('Changes to Settings Discarded')

            # Render cancel button
            cancelBtn = Button(settingsFrame, text='Cancel', command=lambda: handleCancelSettingsModal(settingsFrame))
            cancelBtn.pack()
            cancelBtn.place(anchor='center', width=75, height=25, x=250, y=300)

        # Render settings Button
        def renderSettingsBtn():
            
            img = Image.open(getPath("gear.png"))
            img.resize((50, 50), Image.ANTIALIAS)
            finalImg = ImageTk.PhotoImage(img)
            settingsBtn = Button(root, image=finalImg, command=startSettingsModal)
            settingsBtn.pack()
            settingsBtn.image = finalImg
            settingsBtn.place(anchor='center', x=380, y=310)
        renderSettingsBtn()

        ######################################################

        # Log Label
        def renderLog():
            # Initial Log Message
            settingsObj = getSettingsObj()
            message = 'Resolution at ' + settingsObj.resolution.x + ' x ' + settingsObj.resolution.y + '.  Click button to change.  →'  

            # Render
            log = actionsLog = Label(root, text=message, fg='white', bg='black', anchor='center', justify=LEFT, relief='ridge')
            actionsLog.pack()
            actionsLog.place(bordermode=INSIDE, width=300, height=25, x=200, y=310, anchor='center')
            return log
        log = renderLog()

        # call update function
        root.after(500, lambda: update(levelsData, frames, log))
        root.mainloop()

    render()
