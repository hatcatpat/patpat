from counter import Counter
from cycle import Cycle
from funcs import *
from sequence import Seq

_ = "_"


def variables():
    global V

    V = {"count": Counter(32), "seq": Seq("a", "e", "d", "g")}

    speed(bpm(120, 4))

    new_player("sin")
    toggle(1, "lpf", "reverb", "delay")
    delt(0.5)
    delT(2)
    rel(0.25)
    atk(0.1)
    dur(0.0)
    cut(0)


def command(t):

    if every(0) or (every(4) and chance(0.5)) or (every(8) and chance(0.25)):
        p("sin")
        note("c" + str(choose(3, 4, 5)))
        trig()

    if mod(8):
        p("sin")
        scale("major", between(0, 7, 1), 4)
        trig()

    if mod(16):
        p("sin")
        atk(choose(0, 0.1))

    if euclid(3, 8):
        p("sin")
        atk(0)
        rel(0.1)
        scale("major", between(0, 12, 1))
        trig()

    if val("count", 1) == 0:
        p("sin")
        a = between(0, 0.5)
        atk(a)
        rel(1.0 - a)
        note(val("seq", 1) + "3")
        trig()
