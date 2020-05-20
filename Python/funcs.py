from math import *
from random import *

import global_variables
from counter import Counter
from cycle import Cycle

# SNIPPETS###############
# CLASSES################


def inc(name, step=1):
    global_variables.variables[name].inc(step)


def bang(name, step=1):
    return global_variables.variables[name].bang(step)


def val(name, step=0):
    return global_variables.variables[name].val(step)


def pos(name, p):
    global_variables.variables[name].pos(p)


# UTILS##################


def nearest(x, n):
    return round(x / n) * n


def every(*t):
    v = False

    for i in t:
        v = v or (global_variables.t == i)

    return v


def new_player(name, s=None):
    if s is None:
        s = name
    p(name)
    synth(s)


def euclid(k, n):

    if (1 <= n <= 32) and (0 < k):
        k = min(k, n)

        return global_variables.euclids[str(k) + ":" +
                                        str(n)][global_variables.t % n]
    else:
        return 0


def brk(i, j):
    dur(1 / i)
    arr = []

    for x in range(i):
        arr.append(x)
    v = arr[j % len(arr)]
    start(v / i)


def tofrom(lo, hi):
    arr = []

    for i in range(hi - lo):
        arr.append(i + lo)

    return arr


def bpm(bpm, bar):
    return 60 / (bpm * bar)


def chance(prob):
    return random() < prob


def between(lo, hi, round_to=-1):
    v = random() * (hi - lo) + lo

    if round_to == -1:
        return v
    else:
        return nearest(v, round_to)


def randsplit(*args):
    if len(args) > 0:
        x = randint(0, len(args) - 1)
        args[x]()


def choose(*args):
    return choice(args)


def offset(n, offsets=[0]):
    output = False

    for i in range(len(n)):
        output = output or ((global_variables.t + offsets[i % len(offsets)]) %
                            n[i] == 0)

    return output


def mod(*n):
    output = False

    for x in n:
        output = output or (global_variables.t % x == 0)

    return output


def t_mod(m):
    global_variables.mod = m


#OSC####################


def trig(*args):
    l = list(args)
    l.insert(0, global_variables.current_player)
    global_variables.osc.add_osc_message("/trig", l)


def speed(sp):
    global_variables.osc.add_osc_message("/speed", sp)


def p(player):
    global_variables.current_player = player


def param(param_name, value):
    global_variables.osc.add_osc_message(
        "/param/" + param_name, [global_variables.current_player, value])


def effect(effect_name, param, value):
    global_variables.osc.add_osc_message(
        "/effect/" + effect_name,
        [global_variables.current_player, param, value])


def toggle(b, *effects):
    for e in effects:
        effect(e, "active", b)


def synth(s):
    param("synth", s)


def samp(s):
    param("sample", s)


def note(n):
    param("note", n)


def freq(f):
    param("freq", f)


def rate(r):
    param("rate", r)


def width(w):
    param("width", w)


def dur(d):
    param("dur", d)


def vol(v):
    param("vol", v / 100)


def lpf(l):
    effect("lpf", "lpf", l)
    #  param("lpf", l)


def res(r):
    effect("lpf", "res", r)
    #  param("res", r)


def delt(t):
    effect("delay", "delaytime", t)


def delT(t):
    effect("delay", "maxDelaytime", t)


def pan(p):
    param("pan", p)


def start(s):
    param("pos", s)


def cut(t):
    param("cut", t)
