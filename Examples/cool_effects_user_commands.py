from counter import Counter
from cycle import Cycle
from funcs import *
from sequence import Seq

_ = "_"


def variables():
    global V

    V = {"k": 1, "i": 0}

    speed(bpm(107, 4))

    new_player("sin")
    toggle(1, "lpf", "reverb", "delay", "decimate")
    effect("reverb", "room", 0.5)
    effect("reverb", "damp", 0.5)
    effect("reverb", "mix", 0.3)
    effect("decimate", "bits", between(8, 32, 2))
    lpf(10000)
    delt(0.0125)
    res(0.5)
    vol(100)
    cut(0)

    new_player("samp")
    param("fold", "107")
    param("samp", 0)
    toggle(1, "lpf", "decimate")
    lpf(8000)
    vol(100)
    dur(8)


def command(t):

    if every(1, 3, 4, 7, 8, 9, 12, 13, 14, 15):
        p("sin")

        if chance(0.1):
            effect("decimate", "bits", between(8, 32, 2))
            dur(2)
        else:
            dur(between(0, 0.1))
        effect("decimate", "rate", between(100, 8000, 100))
        pan(between(-0.5, 0.5))
        note(between(40, 80, 1))
        trig()

    if mod(1) and V["k"]:
        start(between(0, 8, 1) / 8)
        p("samp")
        trig()

        if chance(0.05):
            V["k"] = 0

    if mod(2) and not V["k"]:
        effect("decimate", "rate", between(3000, 8000, 1000))

        if chance(0.1):
            V["k"] = 1
        p("samp")
        trig()
