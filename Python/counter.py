#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Counter():
    def __init__(self, mod):
        self.mod = mod
        self.counter = 0

    def inc(self, step=1):
        self.counter += step
        self.counter %= self.mod

    def pos(self, p):
        self.counter = p % self.mod

    def reset(self):
        self.counter = 0

    def setMod(self, new_mod):
        self.mod = new_mod

    def val(self, step=0):
        if step > 0:
            self.inc(step)

        return self.counter

    def valP(self, step=0):
        if step > 0:
            self.inc(step)

        return self.counter / self.mod
