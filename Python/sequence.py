from math import *
from random import *


class Seq():
    def __init__(self, *values):
        arr = []

        for v in values:
            arr.append([not v == "_", v])

        self.arr = arr
        self.counter = 0

    def sz(self):
        return len(self.arr)

    def inc(self, step=1):
        self.counter += step
        self.counter %= len(self.arr)

    def replace(self,p, new_item):
        if 0 <= p < len(self.arr):
            self.arr[p][1] = new_item
    def item(self,p):
        if 0 <= p < len(self.arr):
            return self.arr[p][1]
        else:
            return 0

    def pos(self, p):
        self.counter = p % len(self.arr)

    def bang(self, step=0):
        if step > 0:
            self.inc(step)

        return self.arr[self.counter][0]

    def val(self, step=0):
        if step > 0:
            self.inc(step)

        v = self.arr[self.counter][1]

        if type(v) == SeqElement:
            return v.get()
        else:
            return v

    def get(self):
        return self.arr[self.counter][0], self.arr[self.counter][1]

    def reset(self):
        self.counter = 0


#######################


class SeqElement():
    def __init__(self, mode, values):
        self.mode = mode
        self.arr = values

        if mode == "cycle":
            self.counter = 0
            self.inc_step = 1

    def get(self):
        v = 0
        if self.mode == "rand":
            v = self.rand()
        elif self.mode == "cycle":
            v = self.cycle()

        if type(v) == SeqElement:
            v = v.get()

        return v

    def rand(self):
        return choice(self.arr)

    def cycle(self):
        if type(self.counter) == SeqElement:
            v = self.arr[self.counter.get()]
        else:
            v = self.arr[self.counter]
            if type(self.inc_step) == SeqElement:
                self.counter += self.inc_step.get()
            else:
                self.counter += self.inc_step
            self.counter %= len(self.arr)

        return v

    def step(self, s):
        self.inc_step = s
        return self

    def pos(self, p):
        self.counter = p
        return self
