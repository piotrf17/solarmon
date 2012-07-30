# Acquire data from XBee and output to text file.  File format is simply:
# timestamp0 solar_current0 solar_voltage0 battery_current0 battery_voltage0
# timestamp1 solar_current1 solar_voltage1 battery_current1 battery_voltage1
# etc.

import binascii
import datetime
import os
import serial
import struct
import time

class XBSource(object):
    """A wrapper around a serial connected XB device."""

    def __init__(self, device, baud):
        self.device = serial.Serial(device, baud)
        self.delim = '\x7e'
    
    def Read(self):
        """Read an XB frame, following their API.

        Look for the frame delimeter, then read the length and frame data.
        Also verify the checksum on the frame.
        """
        # Keep trying till we get a valid packet.
        while True:
            # Look for frame delimiter.
            c = self.device.read(1)
            while c != self.delim:
                c = self.device.read(1)
            # Unpack length and read data.
            length, = struct.unpack('>H', self.device.read(2))
            data = self.device.read(length+1)
            # Verify checksum.
            if sum([ord(c) for c in data]) & 0xff == 0xff:
                return data
            else:
                print '%s| packet fails checksum: %s' % (time.ctime(self.time()), binascii.hexlify(data))

class XBMessage(object):
    def __init__(self, data):
        # Verify API frame for RX packet
        assert data[0] == '\x83'       # API identifier for RX packet
        assert data[1:3] == '\x22\x00' # source address
        # Parse out information
        values = struct.unpack('!BBBHHHHHH', data[3:18])
        self.time = time.time()
        self.signal = values[0]
        self.solar_current = values[4]
        self.solar_voltage = values[5]
        self.battery_current = values[6]
        self.battery_voltage = values[7]
        self.temperature = values[8]

class SolarData(object):
    def __init__(self, xb_msg):
        self.time = xb_msg.time
        self.solar_current = 2 * xb_msg.solar_current / 145.9     # [A]
        self.solar_voltage = xb_msg.solar_voltage / 30.42         # [V]
        self.battery_current = 2 * xb_msg.battery_current / 155.1 # [A]
        self.battery_voltage = xb_msg.battery_voltage / 30.66     # [V]
        self.temperature = 275/1664.0*xb_msg.temperature - 800/39.0 # [deg C]
        # Clamp down values below what the Op-Amp can measure
        if self.solar_current < 0.075:
            self.solar_current = 0
        if self.battery_current < 0.075:
            self.battery_current = 0
            

    def Print(self):
        print '%s| (Panel) %fA %fV / (Battery) %fA %fV / %fC'%(time.ctime(self.time), self.solar_current, self.solar_voltage, self.battery_current, self.battery_voltage, self.temperature)

    def Write(self, outfile):
        outfile.write('%f %f %f %f %f %f\n'%(self.time, self.solar_current, self.solar_voltage, self.battery_current, self.battery_voltage, self.temperature))

def GetOutputFilename():
    today = datetime.date.today()
    filename = '%4d%02d%02d.txt'%(today.year, today.month, today.day)
    filename = os.path.join('data', filename)
    return filename

if __name__=="__main__":
    source = XBSource('/dev/ttyUSB0', 9600)
    cur_filename = GetOutputFilename()
    outfile = open(cur_filename, 'a')
    while True:
        try:
            xb_msg = XBMessage(source.Read())
        except AssertionError:
            print '%s| ERROR: frame api data incorrect, dropping' % (time.ctime(self.time()))
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
