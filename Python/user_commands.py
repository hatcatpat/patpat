from counter import Counter
from cycle import Cycle
from funcs import *
from sequence import Seq

_ = "_"


def variables():
    global V

    V = {}

    speed(bpm(120, 4))


def command(t):
    print("beat")
