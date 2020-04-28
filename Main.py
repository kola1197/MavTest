import time

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
        '''if s == 'R' or s == 'r':
            print("Going right second point  (groundspeed set to 10 m/s) ...")
            self.PX.vehicle.mode = VehicleMode("RTL")
        if s == 'Q' or s == 'q':
            print("Going target local point  (groundspeed set to 10 m/s) ...")
            # self.PX.vehicle.goto_position_target_local_ned(30, 60, 60)
            msg = self.PX.vehicle.message_factory.set_position_target_local_ned_encode(
                0,  # time_boot_ms (not used)
                1, 1,  # target system, target component
                mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
                0b0000111111111000,  # type_mask (only positions enabled)
                30, 60, 60,  # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
                0, 0, 0,  # x, y, z velocity in m/s  (not used)
                0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
                0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
            # send command to vehicle
            self.PX.vehicle.send_mavlink(msg)
        if s == 'Z' or s == 'z':
            print("Going target local point  (groundspeed set to 10 m/s) ...")
            # self.PX.vehicle.goto_position_target_local_ned(30, 60, 60)
            msg = self.PX.vehicle.message_factory.set_position_target_global_int_encode(
                0,  # time_boot_ms (not used)
                1, 1,  # target system, target component
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,  # frame
                0b0000111111000111,  # type_mask (only speeds enabled)
                0,  # lat_int - X Position in WGS84 frame in 1e7 * meters
                0,  # lon_int - Y Position in WGS84 frame in 1e7 * meters
                0,  # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
                # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
                20,  # X velocity in NED frame in m/s
                0,  # Y velocity in NED frame in m/s
                0,  # Z velocity in NED frame in m/s
                0, 0, 0,  # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
                0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
            # send command to vehicle
            self.PX.vehicle.send_mavlink(msg)
            pass
        if s == 'C' or s == 'c':
            print("Going target local point  (groundspeed set to 10 m/s) ...")
            msg = self.PX.vehicle.message_factory.command_long_encode(
                1, 1,  # target system, target component
                mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
                0,  # confirmation
                30,  # param 1, yaw in degrees
                0,  # param 2, yaw speed deg/s
                1,  # param 3, direction -1 ccw, 1 cw
                0,  # param 4, relative offset 1, absolute angle 0
                0, 0, 0)  # param 5 ~ 7 not used
            # send command to vehicle
            self.PX.vehicle.send_mavlink(msg)
        if s == 'x' or s == 'X':
            print("Going target local point  (groundspeed set to 10 m/s) ...")
            msg = self.PX.vehicle.message_factory.command_long_encode(
                1, 1,  # target system, target component
                mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
                1,  # confirmation
                20,  # param 1, yaw in degrees
                2,  # param 2, yaw speed deg/s
                1,  # param 3, direction -1 ccw, 1 cw
                1,  # param 4, relative offset 1, absolute angle 0
                0, 0, 0)  # param 5 ~ 7 not used
            self.PX.vehicle.send_mavlink(msg)
        if s == 'v' or s == 'V':
            print("Going target local point  (groundspeed set to 10 m/s) ...")
            msg = self.PX.vehicle.message_factory.set_position_target_local_ned_encode(
                0,  # time_boot_ms (not used)
                1, 1,  # target system, target component
                mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
                0b0000111111111000,  # type_mask (only positions enabled)
                1000, 1000, -100,  # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
                0, 0, 0,  # x, y, z velocity in m/s  (not used)
                0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
                0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
            # send command to vehicle
            self.PX.vehicle.send_mavlink(msg)
        if s == 'h' or s == 'H':
            self.PX.setModeGuided()
        if s == 'N' or s == 'n':
            point2 = LocationGlobalRelative(35.363244, 149.168801, 20)
            self.PX.vehicle.simple_goto(point2)
        if s == 'I' or s == 'i':
            print("Going target local point  (groundspeed set to 10 m/s) ...")
            msg = self.PX.vehicle.message_factory.command_int_encode(
                1, 1,  # target system, target component
                0, 192, 0, 0, -1, 1, 0, 0, 598759654, 307199456,
                234.92)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
            # send command to vehicle
            self.PX.vehicle.send_mavlink(msg)
        if s == 'l' or s == 'L':
            print("Going target local point  (groundspeed set to 10 m/s) ...")
            msg = self.PX.vehicle.message_factory.command_int_encode(
                1, 1,  # target system, target component
                0, 192, 0, 0, -1, 1, 0, 0, 608759654, 317199456,
                234.92)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
            # send command to vehicle
            self.PX.vehicle.send_mavlink(msg)
        if s == 'G' or s == 'g':
            print("Going target local point  (groundspeed set to 10 m/s) ...")
            # self.savedMSG.x=598800000
            self.PX.vehicle.send_mavlink(self.savedMSG)'''

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

    def CreateServer(self):
        # self.PX.Connect()
        self.MAV.Start()
        self.PX.vehicle._handler.pipe(self.MAV.conn)
        print("started")
        self.PX.setModeGuided()  # vehicle.mode = VehicleMode("GUIDED")
        while not self.__stop:
            s = raw_input()
            self.ReactToConsoleMsg(s)
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
