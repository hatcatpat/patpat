from importlib import reload
from math import *

from counter import Counter
from osc_manager import OSCManager


def init():
    global first_command, osc, t, mod, quit, printStrings, speed, current_player, update_flag, counters, cycles, euclids, variables
    first_command = True
    osc = OSCManager()
    t = 0
    speed = 0.125
    mod = 16
    quit = False
    update_flag = True
    current_player = ""
    counters = {}
    cycles = {}
    generate_euclids()

    variables = {}

    osc.reset_bundle()
    update_commands()
    init_bang()


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
    global user_commands, first_command, cycles, counters, variables

    if first_command:
        import user_commands
        first_command = False
    else:
        reload(user_commands)

    user_commands.variables()

    # TODO: Try and make this more efficient

    for v in user_commands.V:
        if v in variables:
            if v != variables[v]:
                variables[v] = user_commands.V[v]
            else:
                user_commands.V[v] = variables[v]
        else:
            variables[v] = user_commands.V[v]

    # for c in user_commands.C:
    #     if c in counters:
    #         if user_commands.C[c].mod != counters[c].mod:
    #             counters[c] = user_commands.C[c]
    #         else:
    #             user_commands.C[c] = counters[c]
    #     else:
    #         counters[c] = user_commands.C[c]

    # for y in user_commands.Y:
    #     if y in cycles:
    #         if user_commands.Y[y].arr != cycles[y].arr:
    #             cycles[y] = user_commands.Y[y]
    #         else:
    #             user_commands.Y[y] = cycles[y]
    #     else:
    #         cycles[y] = user_commands.Y[y]
