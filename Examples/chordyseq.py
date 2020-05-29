from counter import Counter
from cycle import Cycle
from funcs import *
from sequence import Seq

_ = "_"
a = "a"
A = "A"
b = "b"
B = "B"
c = "c"
C = "C"
d = "d"
D = "D"
e = "e"
E = "E"
f = "f"
F = "F"
g = "g"
G = "G"


def variables():
    global V, x, y
    V = {
        "a": Seq(a, a, c, e, e),
        "m": Seq(4, 2),
        "m2": Seq("a5", "g5"),
        "s": Seq("a5", "e5", "c5", "f5"),
        "euc": Seq(11, 13, 11, 15)
    }
    speed(bpm(120, 4))

    new_player("sin")
    toggle(1, "delay")
    toggle(1, "reverb")
    room(0.5)
    delt(0.125)
    dur(0.0)
    rel(0.5)
    cut(0)

    new_player("saw")
    toggle(1, "lpf", "reverb")
    room(0.5)
    lpf(1000)
    cut(0)
    rel(0.5)


def command(t):
    if mod(2, 3) and not mod(5):
        p("sin")
        if chance(0.5):
            note(val("a") + "4")
            rel(0.25)
        else:
            rel(0.1)
            note(val("a") + "5")
        if chance(0.1):
            pos("a", between(0, sz("a"), 1))
        pan(between(-1, 1))
        trig()
    if mod(val("m", 0)):
        p("sin")
        note(val("m2", 0))
        pan(0.25)
        rel(0.1)
        trig()

    if mod(16):
        inc("m")
        if chance(0.5):
            inc("m2")

    if chance(0.5):
        p("sin")

    if mod(16):
        p("saw")
        note(val("s", 1))
        pan(-0.25)
        trig()
