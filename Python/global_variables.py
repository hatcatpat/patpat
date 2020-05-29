from importlib import reload
from math import *

from counter import Counter
from osc_manager import OSCManager


def init():
    global first_command, osc, t, mod, quit_flag, speed, current_player, update_flag, euclids, notes, variables
    first_command = True
    osc = OSCManager()
    t = 0
    speed = 0.125
    mod = 16
    quit_flag = False
    update_flag = True
    current_player = ""
    variables = {}
    notes = {
        "c": 0,
        "C": 1,
        "d": 2,
        "D": 3,
        "e": 4,
        "f": 5,
        "F": 6,
        "g": 7,
        "G": 8,
        "a": 9,
        "A": 10,
        "b": 11
    }

    generate_scales()
    generate_euclids()

    osc.reset_bundle()
    update_commands()
    init_bang()


def note_to_number(note_string):
    note = note_string[0]

    if len(note_string) > 1:
        octave = int(note_string[1:]) + 1
    else:
        octave = 2

    if note in notes:
        return notes[note] + octave * 12
    else:
        return 0


def scale_to_number(scale, element=0, octave=2):

    if scale in scales:
        return scales[scale][element % len(scales[scale])] + (octave + 1) * 12
    else:
        return 0


def generate_scales():
    global scales

    scales = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    }


def generate_euclids():
    global euclids
    euclids = {}

    for i in range(32):
        i += 1

        for j in range(i):
            j += 1
            euclids[str(j) + ":" + str(i)] = euclid(j, i)

    print(euclids)


def euclid(k, n):
    L = []
    R = []

    for i in range(k):
        L.append([1])

    for i in range(n - k):
        R.append([0])

    while (len(R) > 1):
        X = min(len(L), len(R))
        used_R = []
        used_L = []
        NL = []
        NR = []

        for i in range(X):
            NL.append(L[i] + R[i])
            used_R.append(R[i])
            used_L.append(L[i])

        for r in used_R:
            R.remove(r)

        for l in used_L:
            L.remove(l)

        NR = L + R

        L = NL
        R = NR

    END_LIST = L + R
    END = []

    for i in END_LIST:
        for j in i:
            END.append(j)

    print("END", END)

    return END


def init_bang(*args):
    global t, mod
    t = 0
    trigger_update_flag()

    for i in range(mod - 1):
        bang()


def bang(*args):
    global t, mod, update_flag
    print(f"t:{t}")

    osc.reset_bundle()

    if update_flag and t == 0:
        update_commands()
        update_flag = False

    user_commands.command(t)
    osc.send_full_bundle()

    t += 1
    t %= mod


def trigger_update_flag(*args):
    global update_flag
    update_flag = True


def update_commands():
    print("read commands")
    global user_commands, first_command, cycles, counters

    if first_command:
        import user_commands
        first_command = False
    else:
        reload(user_commands)

    user_commands.variables()
    update_variables()

def update_variables():
    global variables
    for v in user_commands.V:
        if v in variables:
            if v != variables[v]:
                variables[v] = user_commands.V[v]
            else:
                user_commands.V[v] = variables[v]
        else:
            variables[v] = user_commands.V[v]
