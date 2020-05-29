from counter import Counter
from cycle import Cycle
from funcs import *
from sequence import Seq

_ = "_"


def variables():
    global V
    speed(bpm(120, 4))
    V = {"a":
            Seq(
                C( "a4", C("b4",_), "e3", R("f5",_) ),
                R("c5")
            )
        }

    new_player("sin")
    dur(0)
    rel(0.1)
    cut(0)


def command(t):
    global V

    if bang("a") or chance(0.25):
        p("sin")
        note(val("a", choose(0,1)))
        trig()

    if mod(16):
        V["a"].replace(0, V["a"].item(0).step(1) )
