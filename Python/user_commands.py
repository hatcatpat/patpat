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
    x = 0
    y = 4
    z = [0, 3, 4, 5, 7]
    V = {
        "a": Seq(a, a, c, e, e),
        "m": Seq(4, 2),
        "m2": Seq("a6", "g6"),
        "s": Seq("b6", "e6", "c6", "f6"),
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
    lpf(2000)
    cut(0)
    rel(0.5)


def command(t):
    global V

    f1(t)


def f2(t):
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
        pan(0)
        rel(0.1)
        trig()

    if mod(16):
        inc("m")
        if chance(0.5):
            inc("m2")

    if mod(16):
        p("saw")
        note(val("s", 1))
        pan(0.5)
        trig()


def f1(t):

    if euclid(val("euc", 0), 16):
        p("sin")
        rel(0.1)
        cut(1)
        toggle(0, "delay", "reverb")
        note(choose(g, a, c, e) + str(choose(3, 4, 5, 6, 7)))
        trig()
    if every(val("euc", 0)):
        inc("euc")
