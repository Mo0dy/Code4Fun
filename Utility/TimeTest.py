import sys
import math
import time


class Timestamp(object):
    def __init__(self, name):
        self.time = time.clock()
        self.name = name


class Tester(object):
    def __init__(self, name):
        self.name = name
        self.timestamps = []
        self.last_loop_time = 0
        self.loop_time = 0

    def timestamp(self, name):
        self.timestamps.append(Timestamp(name))

    def loop_start(self):
        self.last_loop_time = time.clock()

    def loop_end(self):
        current_time = time.clock()
        self.loop_time = current_time - self.last_loop_time
        self.last_loop_time = current_time
        self.print_results()
        self.timestamps = []

    def loop(self):
        if self.last_loop_time == 0:
            self.last_loop_time = time.clock()
        else:
            current_time = time.clock()
            self.loop_time = current_time - self.last_loop_time
            self.last_loop_time = current_time
        self.print_results()
        self.timestamps = []

    def print_results(self):
        if self.loop_time == 0:
            print(self.name + " looptime zero")
        else:
            print("====" + self.name + "====")
            if len(self.timestamps) > 0:
                for i in range(len(self.timestamps) - 1):
                    dt = self.timestamps[i + 1].time - self.timestamps[i].time
                    print(self.timestamps[i].name + " takes " + str(dt / self.loop_time * 100) + "%")
                dt = self.last_loop_time - self.timestamps[len(self.timestamps) - 1].time
                print(self.timestamps[len(self.timestamps) - 1].name + " takes " + str(dt / self.loop_time * 100) + "%")
        print("")
