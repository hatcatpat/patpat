from math import *


class Seq():
    def __init__(self, *values):
        arr = []

        for v in values:
            arr.append([not v == "_", v])

        self.arr = arr
        self.counter = 0

    def inc(self, step=1):
        self.counter += step
        self.counter %= len(self.arr)

    def pos(self, p):
        self.counter = p % len(self.arr)

    def bang(self, step=0):
        if step > 0:
            self.inc(step)

        return self.arr[self.counter][0]

    def val(self, step=0):
        if step > 0:
            self.inc(step)

        return self.arr[self.counter][1]

    def get(self):
        return self.arr[self.counter][0], self.arr[self.counter][1]

    def reset(self):
        self.counter = 0
