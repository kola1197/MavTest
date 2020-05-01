import threading
import time
import keyboard
from past.builtins import raw_input

from PXConnector import PXConnector, LocationGlobalRelative, VehicleMode, mavutil
from MAVConnector import MAVConnector
import socket
import sys


class Main:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PX = PXConnector()
        self.MAV = MAVConnector('udpin:0.0.0.0:50000', 57600, self.MAVListener)
        self.__stop = False
        self.first = True
        self.ch = [1500, 1500, 1500, 1500]

    def stop(self):
        self.MAV.Stop()
        self.PX.Stop()
        self.__stop = True

    def start(self):
        self.CreateServer()
        # while not self.__stop:
        #   try:
        #       self.CreateServer()
        #   finally:
        #       pass

    def reactToData(self, data):
        s = data.replace('_', ' ')
        ch = [int(x) for x in s.split()]
        print("got data: " + str(ch))
        self.PX.vehicle.channels.overrides(ch)

    def MAVListener(self, msg, name):
        # print(name)
        # print(msg)
        if ("COMMAND_INT" in str(msg) and self.first):
            print(msg)
            self.first = False
            self.savedMSG = msg
        pass  # print(msg)

    def stopWork(self):
        print('stop')
        self.stop = True

    def ReactToConsoleMsg(self, s):
        point = self.PX.vehicle.location.global_relative_frame
        print(point)
        if s == 'stop' or s == 'Stop':
            self.stopWork()
        if s == 'W' or s == 'w':
            print("w:: 0, 0, 10")
            # point1 = self.PX.vehicle.
            point2 = LocationGlobalRelative(60, 30, 80)
            self.SendSET_POSITION_TARGET_LOCAL_NED(0, 0, 10)
        if s == 'S' or s == 's':
            print("s:: 0, 0, -10")
            point2 = LocationGlobalRelative(61, 31, 80)
            self.SendSET_POSITION_TARGET_LOCAL_NED(0, 0, -10)
        if s == 'A' or s == 'a':
            print("A:: 10, 0, 0")
            point2 = LocationGlobalRelative(60, 31, 80)
            self.SendSET_POSITION_TARGET_LOCAL_NED(10, 0, 0)
        if s == 'D' or s == 'd':
            print("d:: -10, 0, 0")
            point2 = LocationGlobalRelative(61, 30, 80)
            self.SendSET_POSITION_TARGET_LOCAL_NED(-10, 0, 0)
        if s == 'P' or s == 'p':
            print("POSITION mode")
            self.PX.setModeGuided()

    # COMMAND_INT {target_system : 1, target_component : 1, frame : 0, command : 192, current : 0,
    # autocontinue : 0, param1 : -1.0, param2 : 1.0, param3 : 0.0, param4 : nan, x : 598764140, y : 307225294, z : 62.0359992980957}

    def SendSET_POSITION_TARGET_LOCAL_NED(self, x, y, z):
        msg = self.PX.vehicle.message_factory.set_position_target_local_ned_encode(
            0,  # time_boot_ms (not used)
            1, 1,  # target system, target component
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
            0b0000111111111000,  # type_mask (only positions enabled)
            x, y, z,  # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
            0, 0, 0,  # x, y, z velocity in m/s  (not used)
            0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
        # send command to vehicle
        self.PX.vehicle.send_mavlink(msg)

    def SendCh(self):
        self.PX.vehicle.channels.overrides = {'1': self.ch[0], '2': self.ch[1], '3': self.ch[2], '4': self.ch[3]}

    def threadVoid(self):
        # while (not self.__stop):
        time.sleep(0.03)

    def CreateServer(self):
        # self.PX.Connect()
        self.MAV.Start()
        self.PX.vehicle._handler.pipe(self.MAV.conn)
        print("started")
        threading.Timer(0.03, self.SendCh).start()
        self.PX.setModeGuided()  # vehicle.mode = VehicleMode("GUIDED")
        while not self.__stop:
            self.ch = [1500, 1500, 1500, 1500]
            if keyboard.is_pressed('a'):
                self.ch[0] += 100
            if keyboard.is_pressed('d'):
                self.ch[0] -= 100
            if keyboard.is_pressed('w'):
                self.ch[1] += 100
            if keyboard.is_pressed('s'):
                self.ch[1] -= 100
            # s = raw_input()
            # self.ReactToConsoleMsg(s)
        # while True:
        #    time.sleep(1000)
        #    self.PX.vehicle.message_factory.local_position()
        #    self.PX.vehicle.message_factory.mav_cmd_nav_takeoff_encode()
        '''if (self.PX.connected):
            server_address = ('localhost', 10239)
            print >> sys.stdout, 'starting up on %s port %s' % server_address
            self.sock.bind(server_address)
            self.sock.listen()
            while True:
                # Wait for a connection
                print >> sys.stdout, 'waiting for a connection'
                connection, client_address = self.sock.accept()
                try:
                    print >> sys.stdout, 'connection from', client_address
                    # Receive the data in small chunks and retransmit it
                    while True:
                        data = connection.recv(26)
                        if data:
                            self.reactToData(data)
                            # print >> sys.stderr, 'sending data back to the client'
                            # connection.sendall(data)
                        else:
                            print >> sys.stderr, 'no more data from', client_address
                            break
                finally:
                    # Clean up the connection
                    connection.close()'''

    def reactToMessage(self, msg):
        print(msg)


if __name__ == '__main__':
    M = Main()
    M.start()
