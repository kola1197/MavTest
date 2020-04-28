
import serial
from dronekit import mavlink
import os


class MAVConnector:
    def __init__(self, path, boudrate, ReactToMsg):
        """ constructor """
        #self.Logger = Logger
        self.path = path
        self.boudrate = boudrate
        self.connExists = 0
        self.ReactToMsg = ReactToMsg

    def listener2(self, name, msg):
        self.ReactToMsg(msg, name)

    def Start(self):
        result = 1
        #self.Logger.Write('Connecting by mav to %s' % self.path)
        try:
            if self.path[0] == 'u':
                self.conn = mavlink.MAVConnection(self.path, source_system=1)
            else:
                self.conn = mavlink.MAVConnection(
                    self.path, source_system=1, baud=self.boudrate)
            self.connExists = 1
            self.conn.master.mav.srcComponent = 1
            self.conn.start()
            fn = self.listener2
            self.conn.forward_message(self.listener2)
        except serial.serialutil.SerialException as e:
            #self.Logger.Write('Can not connect to %s' % self.path)
            print(str(e))
            result = 0
        return result

    def Stop(self):
        if self.connExists == 1:
            self.conn.close()
