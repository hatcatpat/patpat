#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Cycle():
    def __init__(self, *args):
        self.arr = args
        self.counter = 0

    def inc(self, step=1):
        self.counter += 1
        self.counter %= len(self.arr)

    def get(self, inc_on=True):
        a = self.arr[self.counter]

        if inc_on:
            self.inc()

        return a
