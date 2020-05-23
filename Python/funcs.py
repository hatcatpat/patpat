from math import *
from random import *

import global_variables
from counter import Counter
from cycle import Cycle

# OBJECT UTILS ###################


def inc(name, step=1):  # increases the counter of an object stored in V
    global_variables.variables[name].inc(step)


def bang(name, step=1):  # returns true if the object wants to be triggered
    return global_variables.variables[name].bang(step)


def val(name, step=0):  # returns the value of an object
    return global_variables.variables[name].val(step)


def pos(name, p):  # returns the current counter of an object
    global_variables.variables[name].pos(p)


def reset(name):
    global_variables.variables[name].reset()


# PATTERN UTILS##################


def nearest(x, n):  # rounds x to nearest multiple of n
    return round(x / n) * n


def every(*t_list):  # returns true if t equals one of the arguments
    v = False

    for i in t_list:
        v = v or (global_variables.t == i)

    return v


def new_player(name, s=None):  # makes a new player, and sets its synth
    if s is None:
        s = name
    p(name)
    synth(s)


def euclid(
    k, n
):  # returns true (or 1) according to euclidean rythmns. No calculation here, the euclid-sets are done at init

    if (1 <= n <= 32) and (0 < k):
        k = min(k, n)

        return global_variables.euclids[str(k) + ":" +
                                        str(n)][global_variables.t % n]
    else:
        return 0


def brk(i, j):  # breakbeat, where j is the specific beat section
    dur(1 / i)
    arr = []

    for x in range(i):
        arr.append(x)
    v = arr[j % len(arr)]
    start(v / i)


def tofrom(lo, hi):  # creates a list from lo to hi
    arr = []

    for i in range(hi - lo):
        arr.append(i + lo)

    return arr


def bpm(bpm, bar):
    return 60 / (bpm * bar)


def chance(prob):  # true if a random number from 0 to 1 is less than prob
    return random() < prob


def between(
    lo,
    hi,
    round_to=-1
):  # returns a value from lo to hi, if round_to is given then it will pass it through nearest
    v = random() * (hi - lo) + lo

    if round_to == -1:
        return v
    else:
        return nearest(v, round_to)


def randsplit(*args):  # randomly calls a function from a list of functions
    if len(args) > 0:
        x = randint(0, len(args) - 1)
        args[x]()


def choose(*args):  # returns a value from its argument list
    return choice(args)


def mod(*n):
    output = False

    for x in n:
        output = output or (global_variables.t % x == 0)

    return output


def offset(n, offset):
    output = False

    if (global_variables.t + offset) % n == 0:
        output = True

    return output


def t_mod(m):
    global_variables.mod = m


#OSC####################


def trig(
    *args
):  # triggers the current player. Optionally, use arguments PLAYER, NOTE, to set specific player and note

    if len(args) > 0:
        p(args[0])

        if len(args) > 1:
            note(args[1])

    global_variables.osc.add_osc_message("/trig",
                                         global_variables.current_player)


def speed(sp):  # sets the speed of the host (i.e, supercollider)
    global_variables.osc.add_osc_message("/speed", sp)


def p(player):  # sets current player
    global_variables.current_player = player


def param(param_name, value):  # changes specified synth parameter
    global_variables.osc.add_osc_message(
        "/param/" + param_name, [global_variables.current_player, value])


def effect(effect_name, param, value):  # changes specific effect parameter
    global_variables.osc.add_osc_message(
        "/effect/" + effect_name,
        [global_variables.current_player, param, value])


def toggle(b, *effects):  # enables/disables a list of effects
    for e in effects:
        effect(e, "active", b)


# PARAMETER SHORTCUTS ###############################


def synth(s):
    param("synth", s)


def samp(s):  # WIP
    param("sample", s)


def midi_note(n):
    param("note", n)


def note(n):
    param("note", global_variables.note_to_number(n))


def scale(s, i=0, octave=4):
    param("note", global_variables.scale_to_number(s, i, octave))


def freq(f):
    param("freq", f)


def rate(r):
    param("rate", r)


def width(w):
    param("width", w)


def dur(d):
    param("dur", d)


def rel(r):
    param("rel", r)


def atk(a):
    param("atk", a)


def vol(v):
    param("vol", v / 100)


def lpf(l):
    effect("lpf", "lpf", l)


def res(r):
    effect("lpf", "res", r)


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
