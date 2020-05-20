from counter import Counter
from cycle import Cycle
from funcs import *
from sequence import Seq

_ = "_"


def variables():
    global V

    V = {"c": Counter(16), "d": Counter(9), "s": 60}

    speed(bpm(120, 4))

    new_player("saw")
    toggle(1, "lpf", "delay")
    dur(0.5)
    delt(0.125)
    lpf(5000)
    cut(0)

    new_player("sin")
    dur(0.125)
    toggle(1, "lpf")
    lpf(10000)
    cut(0)

    new_player("samp")
    param("fold", "vio")
    param("samp", 0)


def command(t):

    if chance(0.1):
        p("saw")
        dur(0.1)
        note(between(70, 100, 2))
        trig()
    else:
        if mod(3):
            p("saw")
            dur(0.25)
            note(50)
            trig()

    if euclid(3, 8):
        p("sin")
        note(choose(60, 70, 50, 55))
        trig()
