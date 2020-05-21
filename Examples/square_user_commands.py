from counter import Counter
from cycle import Cycle
from funcs import *
from sequence import Seq

_ = "_"


def variables():
    global V

    V = {
        "a": Counter(2),
        "b": 80,
        "seq0": Seq(60, 72, _, 60, 75, 80, _, 60),
        "long": Seq(40, 50),
        "longC": Counter(32)
    }

    speed(bpm(120, 4))

    new_player("saw")
    toggle(1, "lpf")
    pan(0)
    dur(0.5)
    delt(0.125)
    lpf(6000)
    cut(0)

    new_player("sin")
    dur(0.125)
    toggle(1, "lpf")
    toggle(0, "reverb")
    pan(0)
    lpf(10000)
    cut(0)


def command(t):

    if chance(0.1) or mod(16):
        inc("a")

    if val("a") == 0 or 0:
        if chance(0.1):
            p("saw")
            dur(0.5)
            toggle(choose(1, 0), "delay")
            note(between(70, 100, 2))
            pan(between(-1, 1))
            trig()
        else:
            if mod(3):
                p("saw")
                cut(0)
                dur(0.25)
                note(choose(50, 60))
                pan(between(0, 1))
                trig()

        if euclid(3, 8) and 1:
            p("sin")
            cut(0)
            note(choose(60, 52, 50, 55))
            pan(between(-1, 0))
            dur(0.25)
            trig()

        if chance(0.1) and mod(2) and 1:
            p("sin")
            note(between(60, 80, 2))
            dur(0.25)
            trig()

        if mod(1) and 1:
            p("saw")
            dur(0.125)
            pan(0)
            note(val("long"))
            trig()
    else:

        if euclid(5, 8):
            p("saw")
            toggle(0, "delay")
            pan(-0.25)
            note(choose(80, 90, 70))
            dur(0.5)
            cut(0)
            trig()

        if mod(2, 3):
            p("sin")
            note(val("seq0", 1))
            pan(0.25)
            dur(0.5)
            cut(0)
            trig()

        if mod(16):
            p("saw")
            dur(2)
            pan(0)
            note(val("long"))
            trig()

    if val("longC", 1) == 0:
        inc("long")
