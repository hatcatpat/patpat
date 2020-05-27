from counter import Counter
from cycle import Cycle
from funcs import *
from sequence import Seq

_ = "_"


def variables():
    global V

    V = {}

    speed(bpm(107, 8))

    new_player("samp")
    param("fold", "vio")
    toggle(1, "lpf", "decimate")
    effect("lpf", "lpf", 5000)
    param("samp", 0)
    dur(2)
    cut(1)

    new_player("saw")
    toggle(1, "lpf")
    lpf(5000)
    dur(1)
    vol(50)
    cut(1)


def command(t):
    if chance(0.5):
        a(t)

        if chance(0.5):
            a(t)
    else:
        trig("samp")

    if mod(8) or (chance(0.5) and mod(2)):
        p("saw")
        lpf(between(100, 8000, 100))
        scale("chromatic", choose(0, 2), 2)
        trig()


def a(t):

    if euclid(3, 8):
        trig("samp")
        param("rate", choose(1, 2))
        start(between(0, 15, 1) / 16)

    if chance(0.5):
        x = choose("vio", "107")

        if x == "vio":
            pan(0)
        else:
            pan(between(-1, 1))
        param("fold", x)
        effect("decimate", "rate", between(1000, 10000, 100))
