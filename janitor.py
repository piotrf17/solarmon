#!/usr/bin/env python

import data_pb2
import glob
import time

def LoadDataFromRaw(filename):
    data = []
    infile = open(filename, 'r')
    for line in infile:
        data.append([float(x) for x in line.split()])
    infile.close()
    return data

def SaveDataToProto(data, filename):
    solar_data = data_pb2.SolarData()
    for value in data:
        data_point = solar_data.data.add()
        data_point.timestamp = value[0]
        data_point.solar_current = value[1]
        data_point.solar_voltage = value[2]
        data_point.battery_current = value[3]
        data_point.battery_voltage = value[4]
        try:
            data_point.temperature = value[5]
        except IndexError:
            # TODO(piotrf): remove this check after old data processed.
            pass
    open(filename, 'wb').write(solar_data.SerializeToString())

def IsProtoGood(filename, expected_len):
    solar_data = data_pb2.SolarData()
    try:
        infile = open(filename, 'rb')
        solar_data.ParseFromString(infile.read())
        infile.close()
    except IOError:
        return False
    return len(solar_data.data) == expected_len

def GetAveragedTimePeriod(data, num_points):
    def ave(list):
        return float(sum(list)) / len(list)
    def average(values):
        return [ave(col) for col in zip(*values)]
    t0 = data[0][0]
    dt = float(data[-1][0] - t0 + 1) / num_points
    buckets = [[] for i in range(num_points)]
    for value in data:
        buckets[int((value[0] - t0) / dt)].append(value)
    output = []
    for bucket in buckets:
        if len(bucket):
            output.append(average(bucket))
    return output

if __name__ == "__main__":
    # Find files to archive.
    raw_files = glob.glob('data/*.txt')
    raw_files.sort()

    # Archive all but the last file, which we assume is still active.
    for filename in raw_files[:-1]:
        print 'Archiving', filename
        proto_filename = filename[:-4] + '.dat'
        data = LoadDataFromRaw(filename)
        data = GetAveragedTimePeriod(data, 24*60)
        SaveDataToProto(data, proto_filename)
        # For paranoia, check that the output is good before deleting original.
        if IsProtoGood(proto_filename, len(data)):
            print 'Deleting ', filename
