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
import webbrowser

##############################
# Global Variables
##############################

ipcQueueItems = []
storagePath = os.path.join(os.getenv('LOCALAPPDATA'), 'hll-companion')
settingsPath = os.path.join(storagePath, 'settings.txt')
scalesPositionsPath = os.path.join(storagePath, 'sliders.txt')
windowOnTop = 0

##############################
# INITIALIZE WINDOW
##############################

def initGui():
    ##############################
    # DATA MANIPULATION
    ##############################

    def getPath(filename):
        return os.path.join(os.path.realpath(os.path.dirname(__file__)), filename)

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
        settingsFile.write('[resolution:{x:1920,y:1080}][stayOnTop:{value:0}]')

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
            print(obj)
            newObj = obj
            # Check if first character is a bracket and remove
            if newObj[1] == '[':
                newObj = obj[1:]
            if newObj[-1] == ']':
                newObj = obj[:-1]
            

            # Split category name and assign to result
            catObj = types.SimpleNamespace()
            catName = newObj.split(':{')[0]
            setattr(catObj, catName, types.SimpleNamespace())
            
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
                setattr(catObj, keyValueList[0], keyValueList[1])
                setattr(resultObj, catName, catObj)
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
        # root.wm_iconbitmap(getPath("assets\\tank.ico"))

        # Get Settings from settings txt and parse to object
        def getSettingsObj():
            settingsFile = open(settingsPath, 'r')
            return parseSettingsString(settingsFile.read())

        # Check if window should be on top and update global variable
        def checkIfTop(displayOnTop=False):
            
            if displayOnTop == False:
                savedSettings = getSettingsObj()
                global windowOnTop
                windowOnTop = int(savedSettings.stayOnTop.value)
            elif displayOnTop == True:
                windowOnTop = 1

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

            # Stay on top?
            if windowOnTop == 1:
                root.attributes('-topmost', True)
            else:
                root.attributes('-topmost', False)

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

            # Variables to be used in widgets
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

            # Stay on top
            stayTopFrame = Frame(settingsFrame, relief='ridge')
            stayTopFrame.pack()
            stayTopFrame.place(anchor='ne', width=150, height=75, x=380, y=20)

            stayTopLabel = Label(stayTopFrame, text='Stay On Top')
            stayTopLabel.pack()
            stayTopLabel.place(anchor='nw', x=5, y=5)

            stayTop = IntVar()
            stayTop.set(int(savedSettings.stayOnTop.value))
            stayTopCheck = Checkbutton(stayTopFrame, variable=stayTop, onvalue=1, offvalue=0 )
            stayTopCheck.pack()
            stayTopCheck.place(anchor='ne', x=145, y=5)

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

                # # Serialize stay on top setting
                stringToWrite += '[stayOnTop:{value:' + str(stayTop.get()) + '}]'

                # Write to file
                settingsFile = open(settingsPath, 'w')
                settingsFile.write(stringToWrite)
                settingsFile.close()

                checkIfTop(bool(stayTop.get()))

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
            
            # img = Image.open(getPath("assets\\gear.png"))
            # img.resize((50, 50), Image.ANTIALIAS)
            # finalImg = ImageTk.PhotoImage(img)
            settingsBtn = Button(root, command=startSettingsModal) #  image=finalImg,
            settingsBtn.pack()
            # settingsBtn.image = finalImg
            settingsBtn.place(anchor='center', x=380, y=310)
        renderSettingsBtn()

        ######################################################
        # INFO MODAL
        ######################################################

        def startInfoModal():
            # Create frame and overlay
            infoFrame = Frame(root, background='gray50')
            infoFrame.pack()
            infoFrame.place(height=330, width=400)            

            # Event handler for OK Button
            def handleOKInfoModal(infoFrame):
                infoFrame.destroy()

            # Render Ok button
            okBtn = Button(infoFrame, text='OK', command=lambda: handleOKInfoModal(infoFrame))
            okBtn.pack()
            okBtn.place(anchor='center', width=75, height=25, x=200, y=310)

            # Render Hotkeys Frame
            hotFrame = Frame(infoFrame)
            hotFrame.pack()
            hotFrame.place(anchor='nw', width=360, height=160, x=20, y=10)

            # Hotkey Title Label
            hotTitleLbl = Label(hotFrame, text='Hotkeys\nAction triggers after Right Alt is released\nRelease all other keys while triggering hotkey')
            hotTitleLbl.pack(side=TOP)

            # Proximity hotkeys frame
            proxFrame = Frame(hotFrame, bd=2, relief='ridge')
            proxFrame.pack()
            proxFrame.place(width=120, height=90, x=0, y=60, anchor='nw')
            
            proxTitle = Label(proxFrame, text='Proximity', anchor='center')
            proxTitle.pack(side=TOP)

            proxActionsContent = ' High:\nLow:\n Mute:'
            proxActions = Label(proxFrame, anchor='nw', text=proxActionsContent)
            proxActions.pack()
            proxActions.place(width=55, height=60, anchor='nw', y=20, x=0)

            proxKeysContent = ' RAlt + p\nRAlt + l\nRAlt + ,'
            proxKeys = Label(proxFrame, anchor='nw', text=proxKeysContent)
            proxKeys.pack()
            proxKeys.place(width=55, height=60, anchor='nw', y=20, x=60)

            # Unit hotkeys frame
            unitFrame = Frame(hotFrame, bd=2, relief='ridge')
            unitFrame.pack()
            unitFrame.place(width=119, height=90, x=120, y=60, anchor='nw')
            
            unitTitle = Label(unitFrame, text='Unit', anchor='center')
            unitTitle.pack(side=TOP)

            unitActionsContent = ' High:\nLow:\n Mute:'
            unitActions = Label(unitFrame, anchor='nw', text=unitActionsContent)
            unitActions.pack()
            unitActions.place(width=55, height=60, anchor='nw', y=20, x=0)

            unitKeysContent = 'RAlt + [\nRAlt + ;\nRAlt + .'
            unitKeys = Label(unitFrame, anchor='nw', text=unitKeysContent)
            unitKeys.pack()
            unitKeys.place(width=55, height=60, anchor='nw', y=20, x=60)            

            # Leadership hotkeys frame
            leadershipFrame = Frame(hotFrame, bd=2, relief='ridge')
            leadershipFrame.pack()
            leadershipFrame.place(width=120, height=90, x=239, y=60, anchor='nw')
            
            leadershipTitle = Label(leadershipFrame, text='Leadership', anchor='center')
            leadershipTitle.pack(side=TOP)

            leadershipActionsContent = ' High:\nLow:\n Mute:'
            leadershipActions = Label(leadershipFrame, anchor='nw', text=leadershipActionsContent)
            leadershipActions.pack()
            leadershipActions.place(width=55, height=60, anchor='nw', y=20, x=0)

            leadershipKeysContent = 'RAlt + ]\nRAlt + \'\nRAlt + /'
            leadershipKeys = Label(leadershipFrame, anchor='nw', text=leadershipKeysContent)
            leadershipKeys.pack()
            leadershipKeys.place(width=55, height=60, anchor='nw', y=20, x=60)            

            # Buy me a coffee frame

            coffeeFrame = Frame(infoFrame)
            coffeeFrame.pack()
            coffeeFrame.place(anchor='nw', width=360, height=110, x=20, y=175)
            
            coffeeMessage = 'Buy Me a Beer?\nHas this app improved your gaming experience? \nAre you pulling off headshots at 400m because you\'re\n no longer distracted by all those PESKY callouts?\n We\'re glad you like the app!\nPlease consider buying us a beer for our hard work.'

            coffeeMessageFrame = Label(coffeeFrame, text=coffeeMessage, pady=0)
            coffeeMessageFrame.pack()
            coffeeMessageFrame.place(width=300, height=90, anchor='n', x=180, y=2)

            def openBeerLink():
                url = 'https://www.buymeacoffee.com/rooseveltcat'
                webbrowser.open_new(url)
            # Render beer Button 
            # img = Image.open(getPath("assets\\beer.png"))
            # img.resize((50, 50), Image.ANTIALIAS)
            # finalImg = ImageTk.PhotoImage(img)
            beerBtn = Button(coffeeFrame, command=openBeerLink) #  image=finalImg,
            beerBtn.pack()
            # beerBtn.image = finalImg
            beerBtn.place(anchor='se', width=35, height=35, x=355, y=105)            
        

        # Render info Button
        def renderInfoBtn():
            
            # img = Image.open(getPath("assets\\info.png"))
            # img.resize((50, 50), Image.ANTIALIAS)
            # finalImg = ImageTk.PhotoImage(img)
            infoBtn = Button(root, command=startInfoModal) # , image=finalImg
            infoBtn.pack()
            # infoBtn.image = finalImg
            infoBtn.place(anchor='center', x=380, y=270)
        renderInfoBtn()
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
        checkIfTop()
        root.after(500, lambda: update(levelsData, frames, log))
        root.mainloop()

    render()
