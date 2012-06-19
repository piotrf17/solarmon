# Acquire data from XBee and output to text file.  File format is simply:
# timestamp0 solar_current0 solar_voltage0 battery_current0 battery_voltage0
# timestamp1 solar_current1 solar_voltage1 battery_current1 battery_voltage1
# etc.

import datetime
import os
import serial
import struct
import time

class XBMessage(object):
    def __init__(self, data):
        # Fix alignment, if necessary.
        if data[1] == '\x7e':
            data = data[1:]
        # Verify header data.
        assert data[0] == '\x7e'        # start delimeter
        assert data[1:3] == '\x00\x10'  # length
        assert data[3] == '\x83'        # API identifier
        assert data[4:6] == '\x22\x00'  # source address
        # Parse out information.
        values = struct.unpack('!BBBHHHHH', data[6:19])
        self.time = time.time()
        self.signal = values[0]
        self.solar_current = values[4]
        self.solar_voltage = values[5]
        self.battery_current = values[6]
        self.battery_voltage = values[7]

class SolarData(object):
    def __init__(self, xb_msg):
        self.time = xb_msg.time
        self.solar_current = xb_msg.solar_current / 145.9     # [A]
        self.solar_voltage = xb_msg.solar_voltage / 30.42     # [V]
        self.battery_current = xb_msg.battery_current / 155.1 # [A]
        self.battery_voltage = xb_msg.battery_voltage / 30.66 # [V]

    def Print(self):
        print '%s| (Panel) %fA %fV / (Battery) %fA %fV'%(time.ctime(self.time), self.solar_current, self.solar_voltage, self.battery_current, self.battery_voltage)

    def Write(self, outfile):
        outfile.write('%f %f %f %f %f\n'%(self.time, self.solar_current, self.solar_voltage, self.battery_current, self.battery_voltage))

def GetOutputFilename():
    today = datetime.date.today()
    filename = '%4d%02d%02d.txt'%(today.year, today.month, today.day)
    filename = os.path.join('data', filename)
    return filename

if __name__=="__main__":
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    cur_filename = GetOutputFilename()
    outfile = open(cur_filename, 'a')
    while True:
        xb_msg = XBMessage(ser.read(20))
        data = SolarData(xb_msg)
        data.Print()
        # Filename changes daily, for simplicity verify every output.
        if GetOutputFilename() != cur_filename:
            outfile.close()
            cur_filename = GetOutputFilename()
            outfile = open(cur_filename, 'a')
        # Output and flush outfile.
        data.Write(outfile)
        outfile.flush()
