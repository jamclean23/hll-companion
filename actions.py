# Actions to be triggered by hotkeys

##############################
# IMPORTS
##############################

from pynput import keyboard
import pygetwindow


###############################
# ACTIONS
###############################

class Actions:

    def focusWindow(self):
        winToBeFocused = pygetwindow.getWindowsWithTitle('Hell Let Loose')[0]
        winToBeFocused.activate()
    

    # Leadership

    def leadershipMute(self):
        print('Setting leadership to mute')
    def leadershipLow(self):
        print('Setting leadership to low')
    def leadershipHigh(self):
        print('Setting leadership to high')

    # Unit

    def unitMute(self):
        print('Setting unit to mute')
    def unitLow(self):
        print('Setting unit to low')
    def unitHigh(self):
        print('Setting unit to high')

    # Proximity
    
    def proxMute(self):
        print('Setting proximity to mute')
    def proxLow(self):
        print('Setting proximity to low')
    def proxHigh(self):
        print('Setting proximity to high')


    # Init

    def __init__(self):
        self.test = 'test'
