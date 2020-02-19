from PCANBasic import *

import threading               ## Threading-based Timer library



fd_config_80M_500K_80____2M_80_ISO = { 80000000, 4, 31, 8, 8, 96, 0, 1, 4, 7, 2, 2} #// 80 MHz, 500K 80%, 2M 80%, ISO
import os

class PCANBasicApp:

    def __init__(self):
        
        # Example's configuration
        self.InitializeBasicComponents()
        self.ConfigurationDevice()
        self._lock = threading.RLock()


    ## Destructor
    ##
    def destroy (self):
        self.UninitializeBasicComponents() 

    

    ## Message loop
    ##
    def loop(self):
        # This is an explict replacement for _tkinter mainloop()
        # It lets catch keyboard interrupts easier, and avoids
        # the 20 msec. dead sleep() which burns a constant CPU.
        i=0
        while (i<=50):
            # There are 2 whiles here. The outer one lets you continue
            # after a ^C interrupt.
            i+=1
            self.ReadMessages()
            
        #clear = lambda: os.system('cls') #on Windows System
        #clear()
################################################################################################################################################
### Help functions
################################################################################################################################################

    ## Initializes app members
    ##
    def InitializeBasicComponents(self):
        self.m_objPCANBasic = PCANBasic()
        print ("Initialing the Tool ...")

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
        #self.m_BitrateTXT = TPCANBitrateFD(f_clock=80000000,nom_brp=10,nom_tseg1=5,nom_tseg2=2,nom_sjw=1,data_brp=4,data_tseg1=7,data_tseg2=2,data_sjw=1)
        #self.m_Bitrate = TPCANBitrateFD()
        self.m_Channel = PCAN_USBBUS1#PCAN_USBBUS1
        self.m_Btr0Btr1 = PCAN_BAUD_500K
        result = self.m_objPCANBasic.InitializeFD(self.m_Channel,"f_clock=80000000, nom_brp=10, nom_tseg1=12, nom_tseg2=3, nom_sjw=1, data_brp=4, data_tseg1=7, data_tseg2=2, data_sjw=1")#,HwType=TPCANType(0),IOPort=c_uint(0),Interrupt=c_ushort(0))
        if result == PCAN_ERROR_OK:
            
            print ("Device initialized properly")
        else:
            print ("Device not initialized")

     
    def ConfigurationDevice(self):
        self.m_CanRead = True
    
    def UninitializeBasicComponents(self):
        # The USB Channel is released
        #
        result = self.m_objPCANBasic.Uninitialize(PCAN_USBBUS1)
        if result != PCAN_ERROR_OK:
            # An error occurred, get a text describing the error and show it
            #
            result = self.m_objPCANBasic.GetErrorText(result)
            print (result[1])
        else:
            print ("PCAN-USB (Ch-1) was released")
        
    def ReadMessages(self):
        stsResult = PCAN_ERROR_OK
        # We read at least one time the queue looking for messages.
        # If a message is found, we look again trying to find more.
        # If the queue is empty or an error occurr, we get out from
        # the dowhile statement.
        #
        empty = True
        while (empty):
            #stsResult = self.ReadMessageFD() if self.m_IsFD else self.ReadMessage()
            
            stsResult = self.m_objPCANBasic.ReadFD(PCAN_USBBUS1)
            if stsResult == PCAN_ERROR_ILLOPERATION:
                print ("PCAN_ERROR_ILLOPERATION")
                break

            if (not(stsResult[0] & PCAN_ERROR_QRCVEMPTY)):
                empty = False
                #print "Message Received"
                print (stsResult[1].ID, hex(stsResult[1].DLC)),
                itsTimeStamp = stsResult[2]    
                '''newTimestamp = TPCANTimestampFD()
                newTimestamp.value = (itsTimeStamp.micros + 1000 * itsTimeStamp.millis + 0x100000000 * 1000 * itsTimeStamp.millis_overflow)'''
                '''
                    TPCANTimestampFD
                    Represents the timestamp of a CAN message with flexible data rate. The time-stamp contains the number of microseconds since the start of Windows.
                '''
                
                print itsTimeStamp.value , " us",#newTimestamp.value,
                for i in range(stsResult[1].DLC):
                    print hex(stsResult[1].DATA[i]),
                print "\r"
            
        #with self._lock:
        '''
        theMsg = stsResult[1]
        
        itsTimeStamp = stsResult[2]    
        newTimestamp = TPCANTimestamp()
        newTimestamp.value = (itsTimeStamp.micros + 1000 * itsTimeStamp.millis + 0x100000000 * 1000 * itsTimeStamp.millis_overflow)
        newMsg = TPCANMsg()
        newMsg.ID = theMsg.ID
        newMsg.DLC = theMsg.LEN
        #for i in range(8 if (theMsg.LEN > 8) else theMsg.LEN):
        #    newMsg.DATA[i] = theMsg.DATA[i]
        #newMsg.MSGTYPE = theMsg.MSGTYPE
        #newTimestamp = TPCANTimestamp()
        #newTimestamp.value = (itsTimeStamp.micros + 1000 * itsTimeStamp.millis + 0x100000000 * 1000 * itsTimeStamp.millis_overflow)
        '''
        '''
        while (stsResult[0][0] & PCAN_ERROR_QRCVEMPTY) != PCAN_ERROR_QRCVEMPTY:
            # Check the receive queue for new messages
            #
            readResult = self.m_objPCANBasic.Read(PCAN_USBBUS1)
            if readResult[0] != PCAN_ERROR_QRCVEMPTY:
                # Process the received message
                #
                print "A message was received"
                print result[1] + "\t"
                print result[2] + "\n"
                #ProcessMessage(result[1],result[2]) # Possible processing function, ProcessMessage(msg,timestamp)
            else:
                # An error occurred, get a text describing the error and show it
                #
                result = self.m_objPCANBasic.GetErrorText(readResult[0])
                print result[1]
                #HandleReadError(readResult[0]) # Possible errors handling function, HandleError(function_result)
        '''

    '''def ProcessMessageFD(self, *args):
        with self._lock:
            # Split the arguments. [0] TPCANMsgFD, [1] TPCANTimestampFD
            #
            theMsg = args[0][0]
            itsTimeStamp = args[0][1]
            
            for msg in self.m_LastMsgsList:
                if (msg.CANMsg.ID == theMsg.ID) and (msg.CANMsg.MSGTYPE == theMsg.MSGTYPE):
                    msg.Update(theMsg, itsTimeStamp)                    
                    return
            self.InsertMsgEntry(theMsg, itsTimeStamp)'''

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
    app.loop()
    
    # Application's destrution / loop-end
    #
    app.destroy()

if __name__ == '__main__':
    # Creates the Tkinter-extension Root
    #
    #root = Tix.Tk()
    root = ""
    # Uses the root to launch the PCAN-Basic Example application
    #
    RunMain(root)
###*****************************************************************
