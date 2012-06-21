#!/usr/bin/env python

"""Reads sensor data and generates data for a Google Charts plot

This tool follows a text output file with the format as defined in acquire.py,
and every 10 seconds generates a summary page with plots for:
    * last minute
    * last hour
    * current day
Each plot has solar and battery voltage and current on one plot.
"""

import datetime
import time
import os
import numpy
from mako.template import Template

def Smooth(x,window_len=11,window='hanning'):
    s=numpy.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    if window == 'flat': #moving average
        w=numpy.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')
    y=numpy.convolve(w/w.sum(),s,mode='same')
    return y[window_len-1:-window_len+1]

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
        formatted.append('[%s, %f, %f, %f, %f],\n'%tuple([time_str]+list(value[1:])))
    return ''.join(formatted)

def GetLastMinute(data):
    t0 = time.time() - 60
    last_minute = [x for x in data if x[0] > t0]
    return last_minute

def GetSmoothedTimePeriod(data, time_len):
    t0 = time.time() - time_len
    last_hour = [x for x in data if x[0] > t0]
    last_hour = last_hour[::(time_len/60)]
    t, sc, sv, bc, bv = zip(*last_hour)
    sc = Smooth(sc, 11)
    sv = Smooth(sv, 11)
    bc = Smooth(bc, 11)
    bv = Smooth(bv, 11)
    return zip(t, sc, sv, bc, bv)

def GetAveragedTimePeriod(data, time_len, num_points):
    def ave(list):
        return float(sum(list)) / len(list)
    def average(values):
        t, sc, sv, bc, bv = zip(*values)
        return [t[len(t)/2], ave(sc), ave(sv), ave(bc), ave(bv)]
    t0 = time.time() - time_len
    last_time = [x for x in data if x[0] > t0]
    output = []
    bucket_size = len(last_time) / num_points
    for i in range(0, len(last_time), bucket_size):
        output.append(average(last_time[i:i+bucket_size]))
    return output

if __name__=="__main__":
    data = []
    last_pos = 0
    while True:
        last_pos = ParseData(GetInputFilename(), last_pos, data)
        start = time.time()
        template = Template(filename='index.tpl')
        open('/var/www/solar/index.html','w').write(template.render(
            UPDATE_TIME=time.ctime(),
            LAST_MINUTE=FormatValues(GetLastMinute(data)),
            LAST_HOUR=FormatValues(GetAveragedTimePeriod(data, 60*60, 100)),
            LAST_DAY=FormatValues(GetAveragedTimePeriod(data, 24*60*60, 100))))
        plottime = time.time() - start
        print time.ctime(), '| Generated plots in', plottime, 's'
        time.sleep(max(10 - plottime, 1))
