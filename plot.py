#!/usr/bin/env python

"""Reads sensor data and generate plots and a summar page.

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
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

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

def CreateCurrentVoltagePlot(t, c, v, title, filename, xlim=(0,60)):
    figure = Figure(figsize=(8,4))
    figure.suptitle(title)
    axis1 = figure.add_subplot(111)
    axis1.grid(True)
    lines = []
    lines.extend(axis1.plot(t, c, 'b'))
    axis1.set_xlabel('Time')
    axis1.set_ylabel('Current [A]')
    axis1.set_xlim(xlim)
    axis1.set_ylim([0, 6])
    axis2 = axis1.twinx()
    lines.extend(axis2.plot(t, v, 'r'))
    axis2.set_ylabel('Voltage [V]')
    axis2.set_ylim([11, 15])
    figure.legend(lines, ('Current', 'Voltage'), 'upper left')
    canvas = FigureCanvasAgg(figure) 
    canvas.print_figure(filename, dpi=80)

def PlotLastMinute(data, output_dir):
    t0 = time.time() - 60
    last_minute = [x for x in data if x[0] > t0]
    t, sc, sv, bc, bv = zip(*last_minute)
    t = [t_ - t0 for t_ in t]
    CreateCurrentVoltagePlot(t, bc, bv, 'Battery Output', os.path.join(output_dir, 'lastminute_battery.png'))    
    CreateCurrentVoltagePlot(t, sc, sv, 'Solar Input', os.path.join(output_dir, 'lastminute_solar.png'))    

def PlotLastHour(data, output_dir):
    t0 = time.time() - 3600
    last_hour = [x for x in data if x[0] > t0]
    t, sc, sv, bc, bv = zip(*last_hour)
    sc = Smooth(sc, 50)
    sv = Smooth(sv, 50)
    bc = Smooth(bc, 50)
    bv = Smooth(bv, 50)
    t = [(t_ - t0)/60.0 for t_ in t]
    CreateCurrentVoltagePlot(t, bc, bv, 'Battery Output', os.path.join(output_dir, 'lasthour_battery.png'))    
    CreateCurrentVoltagePlot(t, sc, sv, 'Solar Input', os.path.join(output_dir, 'lasthour_solar.png'))    

def PlotLastDay(data, output_dir):
    t0 = time.mktime(datetime.date.today().timetuple())
    today = [x for x in data if x[0] > t0]
    t, sc, sv, bc, bv = zip(*today)
    sc = Smooth(sc, 1000)
    sv = Smooth(sv, 1000)
    bc = Smooth(bc, 1000)
    bv = Smooth(bv, 1000)
    t = [(t_ - t0)/3600.0 for t_ in t]
    CreateCurrentVoltagePlot(t, bc, bv, 'Battery Output', os.path.join(output_dir, 'lastday_battery.png'), (0, 24))    
    CreateCurrentVoltagePlot(t, sc, sv, 'Solar Input', os.path.join(output_dir, 'lastday_solar.png'), (0, 24))    

if __name__=="__main__":
    data = []
    last_pos = 0
    while True:
        last_pos = ParseData(GetInputFilename(), last_pos, data)
        start = time.time()
        PlotLastMinute(data, '/var/www/solar/plots/')
        PlotLastHour(data, '/var/www/solar/plots/')
        PlotLastDay(data, '/var/www/solar/plots/')
        plottime = time.time() - start
        print time.ctime(), '| Generated plots in', plottime, 's'
        time.sleep(10 - plottime)
