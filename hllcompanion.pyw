# Index file

##############################
# IMPORTS
##############################

import hotkeylistener
import volumedisplay
import pyuac

def main():
    # Key/Action Handler
    print('Initializing listeners')
    hotkeylistener.initListener()
    # Gui
    print('Starting Gui')
    volumedisplay.initGui()

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:        
        main()  # Already an admin here.





