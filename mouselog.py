#!/usr/bin/env python
#
# mouselog 0.1
#
# Log mouse distance over time to a CSV file.
# Also display a simple graph on the console.
#
# Either run as root or give permissions to read /dev/input/mice, with for instance:
# chmod a+r /dev/input/mice
#
# Thanks to meuh at https://unix.stackexchange.com/a/397985/3920 for the unpack + euler distance calculation.
#
# oct 2017
#
# Alexander F Rødseth <xyproto@archlinux.org>
# MIT licensed
#

import collections
import csv
import time
import struct
import sys

class MouseCollector:

    def __init__(self, mouse_device, output_file, terminal_width=40):
        try:
            self.mice = open(mouse_device, "rb")
        except Exception as err:
            print("Could not open " + mouse_device + ":", err)
            sys.exit(1)
        self.distance = collections.OrderedDict()
        self.counter = 0
        self.total = 0
        try:
            self.csv = open(output_file, "w")
        except Exception as err:
            print("Could not open " + output_file + " for writing:", err)
            sys.exit(1)
        self.written = []
        self.timestamp = 0
        self.terminal_width = terminal_width

    def movement(self):
        """Thank you https://unix.stackexchange.com/a/397985/119298"""
        x, y = struct.unpack("xbb", self.mice.read(3))
        distance = (x*x+y*y)**.5
        self.total += distance
        return distance

    def update(self):
        if self.timestamp in self.distance:
            self.distance[self.timestamp] += self.movement()
        else:
            self.distance[self.timestamp] = self.movement()

    def next(self, timestamp_start):
        self.counter += 1
        self.timestamp = int(time.time() - timestamp_start)
    
    def write(self):
        writer = csv.writer(self.csv)
        for key, value in self.distance.items():
            if key in self.written:
                continue
            writer.writerow([key, value, self.total])
            self.written.append(key)
        self.csv.flush()
        #print("Wrote to", self.csv.name)

    def stats(self, full=False, stat_lines=10):
        if full:
            keys = self.distance.keys()
        else:
            keys = list(self.distance.keys())
            len_keys = len(keys)
            if len_keys > stat_lines:
                keys = keys[len_keys-stat_lines:]
        maxvalue = 0
        for key in keys:
            if self.distance[key] > maxvalue:
                maxvalue = self.distance[key]
        s = ""
        # Output stats as a graph with "*" for bars
        for key in keys:
            value = self.distance[key]
            s += str(key) + ": " + "*" * int((value/maxvalue)*self.terminal_width) + "\n"
        return s + "Last distance: " + str(int(self.distance[key])) + "\n" + "Total distance: " + str(int(self.total))

    def __str__(self):
        return self.stats(full=True)

def log_mouse(output_file="output.csv", log_resolution=60, stat_lines=40, while_function=lambda x: True, verbose=False, mouse_device="/dev/input/mice"):
    """log_resolution is in seconds, and is the "buckets" where mouse distances are logged, the while_function returns True as long as the logging should continue, and receives the elapsed time in seconds"""
    timestamp_start = time.time()
    mc = MouseCollector(mouse_device, output_file)
    while while_function(time.time() - timestamp_start):
        start_time = time.time()
        while (time.time() - start_time) < log_resolution:
            mc.update()
        if verbose:
            print(mc.stats(stat_lines=stat_lines))
        mc.next(timestamp_start)
        mc.write()
    return mc

def main():
    mc = None
    try:
        mc = log_mouse("/tmp/output.csv", 1, verbose=True)
    except KeyboardInterrupt:
        print(mc)

if __name__ == "__main__":
    main()
