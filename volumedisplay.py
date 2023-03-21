# Tkinter gui window

##############################
# IMPORTS
##############################

from tkinter import *
import os
from PIL import ImageTk, Image  
from multiprocessing.managers import BaseManager

##############################
# Global Variables
##############################

ipcQueueItems = []

##############################
# INITIALIZE WINDOW
##############################

def initGui():
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

        # Reset ipcQueueItems
        def resetQueueItems():
            global ipcQueueItems
            ipcQueueItems = []

        # Add to ipcQueueItems
        def updateQueue(newItem):
            global ipcQueueItems

            print(newItem)

            # Add item
            ipcQueueItems.append(newItem)

            # Send to multiprocess queue
            manager = BaseManager(address=('localhost', 50000), authkey=b'blahkey')
            manager.connect()

            currentQueue = manager.getIpcQueue()
            
            if not currentQueue.empty():
                print(currentQueue.get())
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

        # Set up update function
        def update(levelsData, frames):
            handleUpdateClick(levelsData, frames)
            root.after(2000, lambda: update(levelsData, frames))

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
            scales = []
            i = 0
            for dateObj in levelsData:
                # High Sliders
                dateObj.highScale = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=75, label='      High')
                dateObj.highScale.bind("<ButtonRelease-1>", lambda event : updateScalesValues(scales))
                dateObj.highScale.pack()
                dateObj.highScale.set(70)
                dateObj.highScale.place(anchor='center', x=100 + (i * 100), y=195)

                # Low Sliders
                dateObj.lowScale = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=75, label='      Low')
                dateObj.lowScale.bind("<ButtonRelease-1>", lambda event : updateScalesValues(scales))
                dateObj.lowScale.pack()
                dateObj.lowScale.set(30)
                dateObj.lowScale.place(anchor='center', x=100 + (i * 100), y=255)

                scales.append(dateObj)

                i += 1
            return scales
        scales = renderScales(levelsData)
        # On app mount update
        updateScalesValues(scales)



        # Settings Button
        def renderSettingsBtn():
            img = Image.open("./assets/gear.png")
            img.resize((50, 50), Image.ANTIALIAS)
            finalImg = ImageTk.PhotoImage(img)
            settingsBtn = Button(root, image=finalImg)
            settingsBtn.pack()
            settingsBtn.image = finalImg
            settingsBtn.place(anchor='center', x=380, y=310)
        renderSettingsBtn()

        # Log Label
        def renderLog():
            actionsLog = Label(root, text='Log:', fg='white', bg='black', anchor='w', justify=LEFT, relief='ridge')
            actionsLog.pack()
            actionsLog.place(bordermode=INSIDE, width=300, height=25, x=200, y=310, anchor='center')
        renderLog()

        # call update function
        root.after(2000, lambda: update(levelsData, frames))
        root.mainloop()

    render()
