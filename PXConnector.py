from dronekit import *
# from Logger import Logger
import serial


class PXConnector:
    def __init__(self, path):
        self.path = path
        self.vehicleExists = 0
        self.vehicle = connect(self.path, 57600)
        print('Connecting to PX4 on %s' % self.path)

        # self.ReactToMsg = _ReactToMsg

    def __init__(self):
        """ constructor """
        # self.Logger = Logger
        self.path = "/dev/ttyUSB1"
        self.vehicleExists = 0
        print('Connecting to PX4 on %s' % self.path)
        self.vehicle = connect(self.path, baud=57600)
        #self.vehicle.wait_ready(True, raise_exeption=False)
        print('PX4 connected')
        #fn = self.react
        #def listener(self, name, msg):
        #    fn(msg, name)
        #    print msg
        #     #    #self.Logger.Write(str(msg))
        # try:
        #     self.vehicle = connect(self.path, baud=57600)
        #     # self.vehicle.wait_ready(True, raise_exeption=False)
        #     self.vehicleExists = 1
        #     # self.Logger.Write
        #     print('PX4 connected')
        #     # self.Logger.Write
        #     print("startListening")
        #     # fn = self.react
        #     # def listener(self, name, msg):
        #     #    fn(msg, name)
        #     #    #print msg
        #     #    #self.Logger.Write(str(msg))
        #     # self.vehicle.add_message_listener('*', listener)
        # except serial.serialutil.SerialException as e:
        #     # self.Logger.Write
        #     print('Can not connect to %s' % self.path)
        #     print(str(e))

    def setModeGuided(self):
        self.vehicle.mode = VehicleMode("GUIDED")

    def Connect(self):
        result = 1
        # self.Logger.Write
        print('Connecting to PX4 on %s' % self.path)
        try:
            self.vehicle = connect(self.path, 57600)
            # self.vehicle.wait_ready(True, raise_exeption=False)
            self.vehicleExists = 1
            # self.Logger.Write
            print('PX4 connected')
            # self.Logger.Write
            print("startListening")
            # fn = self.react
            # def listener(self, name, msg):
            #    fn(msg, name)
            #    #print msg
            #    #self.Logger.Write(str(msg))
            # self.vehicle.add_message_listener('*', listener)
        except serial.serialutil.SerialException as e:
            # self.Logger.Write
            print('Can not connect to %s' % self.path)
            print(str(e))
            result = 0
        return result

    '''def listener(self, name, msg):
        self.Logger.Write(str(msg))
        #self.ReactToMsg(msg)
       '''

    def startListening(self):
        pass
        '''self.Logger.Write("startListening")
        fn = self.ReactToMsg
        v = self.vehicle
        @v.on_message('*')
        def listener(self, name, msg):
            self.Logger.Write(str(msg))
            fn(msg)
'''

    def react(self, msg, name):
        self.ReactToMsg(msg, name)

    def Stop(self):
        if self.vehicleExists == 1:
            self.vehicle.close()
