#!/usr/bin/env python

"""Reads sensor data and generates data for a Google Charts plot

This tool follows a text output file with the format as defined in acquire.py,
and every 10 seconds generates a summary page with plots for:
    * last minute
    * last hour
    * current day
Each plot has solar and battery voltage and current on one plot.
"""

import collections
import datetime
import time
import os
import numpy
from mako.template import Template
import data_pb2

class AveragingBuffer(object):
    """A circular buffer that provides averaged last values for a given time
    period and resolution."""

    def __init__(self, period, resolution):
        self.buf = collections.deque(maxlen=resolution)
        self.temp = []
        self.last_cutoff = time.time() - period
        self.period = float(period) / resolution

    def _AverageTemp(self):
        if self.temp:
            average = [float(sum(col)) / len(col) for col in zip(*self.temp)]
            self.buf.append(average)
            self.temp = []
        self.last_cutoff += self.period

    def AddValues(self, data):
        for value in data:
            if value[0] > self.last_cutoff + self.period:
                self._AverageTemp()
            elif value[0] > self.last_cutoff:
                self.temp.append(value)

    def Last(self):
        if self.temp:
            average = [float(sum(col)) / len(col) for col in zip(*self.temp)]
            return list(self.buf) + [average]
        else:
            return list(self.buf)

def LoadOldData():
    data = []
    for days_ago in range(-6, 0):
        # Construct the appropriate filename.
        day = datetime.date.today() + datetime.timedelta(days=days_ago)
        filename = '%4d%02d%02d.dat'%(day.year, day.month, day.day)
        filename = os.path.join('data', filename)
        if not(os.path.exists(filename)):
            continue
        # Load proto.
        print 'Loading', filename
        solar_data = data_pb2.SolarData()
        solar_data.ParseFromString(open(filename, 'rb').read())
        # Unpack values into our simple lists.
        for v in solar_data.data:
            data.append([v.timestamp, v.solar_current, v.solar_voltage, 
                v.battery_current, v.battery_voltage, v.temperature])
    return data

def GetInputFilename():
    today = datetime.date.today()
    filename = '%4d%02d%02d.txt'%(today.year, today.month, today.day)
    filename = os.path.join('data', filename)
    return filename

def ParseData(filename, pos, data):
    infile = open(filename, 'r')
    infile.seek(pos)
    for line in infile:
        data.append([float(x) for x in line.split()])
    end_pos = infile.tell()
    infile.close()
    return end_pos

def FormatValues(values):
    formatted = []
    for value in values:
        dt = datetime.datetime.fromtimestamp(value[0])
        time_str = 'new Date(%d, %d, %d, %d, %d, %d, %d)'%(dt.year, dt.month-1, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond/1000)
        formatted.append('[%s, %f, %f, %f, %f, %f],\n'%tuple([time_str]+list(value[1:])))
    return ''.join(formatted)

if __name__=="__main__":
    # Build averaging buffers with old data.
    old_data = LoadOldData()
    print 'Preloading averaging buffers with historical data.'
    last_hour = AveragingBuffer(60*60, 120)
    last_day = AveragingBuffer(24*60*60, 144)
    last_week = AveragingBuffer(7*24*60*60, 168)
    last_hour.AddValues(old_data)
    last_day.AddValues(old_data)
    last_week.AddValues(old_data)
    # Start main loop of tracking one input file.
    print 'Starting to read live data.'
    last_pos = 0
    current_filename = GetInputFilename()
    while True:
        start = time.time()
        # Handle filename switch over at midnight.
        if GetInputFilename() != current_filename:
            # Sleep to give acquire time to create the new file.
            time.sleep(30)
            last_pos = 0
            current_filename = GetInputFilename()
        # Read data and add to buffers.
        data = []
        last_pos = ParseData(current_filename, last_pos, data)
        last_hour.AddValues(data)
        last_day.AddValues(data)
        last_week.AddValues(data)
        # Output HTML summary page with plots.
        template = Template(filename='index.tpl')
        html = template.render(
            UPDATE_TIME=time.ctime(),
            LAST_HOUR=FormatValues(last_hour.Last()),
            LAST_DAY=FormatValues(last_day.Last()),
            LAST_WEEK=FormatValues(last_week.Last()))
        open('/var/www/solar/index.html', 'w').write(html)
        plottime = time.time() - start
        print time.ctime(), '| Generated plots in', plottime, 's'
        time.sleep(max(10 - plottime, 1))
