# Index file

##############################
# IMPORTS
##############################

import hotkeylistener
import volumedisplay
import pyuac
from multiprocessing.managers import BaseManager
import threading
import time
import queue


##############################
# Init
##############################

def main():

    def newServer():
        # Multiprocess Queue
        ipcQueue = queue.Queue()
        BaseManager.register('getIpcQueue', callable=lambda: ipcQueue)
        manager = BaseManager(address=('localhost', 50000), authkey=b'blahkey')
        server = manager.get_server()
        print('server running')

        def startServer():
            server.serve_forever()

        newThread = threading.Thread(target=startServer, daemon=True)
        newThread.start()

        # Key/Action Handler
        print('Initializing listeners')
        hotkeylistener.initListener()
        # Gui
        print('Starting Gui')
        volumedisplay.initGui()

    newServer()


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:        
        main()  # Already an admin here.





