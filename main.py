from PCANBasic import *

class PCANBasicApp:
    def __init__(self):
        
        # Example's configuration
        self.InitializeBasicComponents()
        


    ## Destructor
    ##
    def destroy (self):
        pass  

    ## Message loop
    ##
    def loop(self):
        # This is an explict replacement for _tkinter mainloop()
        # It lets catch keyboard interrupts easier, and avoids
        # the 20 msec. dead sleep() which burns a constant CPU.
        while self.exit < 0:
            # There are 2 whiles here. The outer one lets you continue
            # after a ^C interrupt.
            pass

################################################################################################################################################
### Help functions
################################################################################################################################################

    ## Initializes app members
    ##
    def InitializeBasicComponents(self):
        self.m_objPCANBasic = PCANBasic()
        print "Initialing the Tool ..."
        """
          Initializes a PCAN Channel

        Parameters:
          Channel  : A TPCANHandle representing a PCAN Channel
          Btr0Btr1 : The speed for the communication (BTR0BTR1 code)
          HwType   : Non-PnP: The type of hardware and operation mode
          IOPort   : Non-PnP: The I/O address for the parallel port
          Interrupt: Non-PnP: Interrupt number of the parallel port
        
        Returns:
          A TPCANStatus error code
        """
        self.m_Channel = PCAN_USBBUS1
        self.m_Btr0Btr1 = PCAN_BAUD_500K
        result = self.m_objPCANBasic.Initialize(self.m_Channel,self.m_Btr0Btr1)#,HwType=TPCANType(0),IOPort=c_uint(0),Interrupt=c_ushort(0))
        if result == PCAN_ERROR_OK:
            print "Device initialized properly"
        else:
            print "Device not initialized"

     
        
        
    


###*****************************************************************
### ROOT
###*****************************************************************
def RunMain (root):
    global app

    # Creates a PCAN-Basic app
    #
    app = PCANBasicApp()

    # Runs the Application / loop-start
    #
    #app.loop()
    
    # Application's destrution / loop-end
    #
    #app.destroy()

if __name__ == '__main__':
    # Creates the Tkinter-extension Root
    #
    #root = Tix.Tk()
    root = ""
    # Uses the root to launch the PCAN-Basic Example application
    #
    RunMain(root)
###*****************************************************************
