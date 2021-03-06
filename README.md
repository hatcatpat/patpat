# patpat
A Python based OSC sequencer for audio applications, with SuperCollider integration.

##### contents
[what](#what)
[how](#how)
[extras](#extras)

# what
Patpat is a Python based sequencer which sends OSC messages. Due to delays in OSC messages, it sends each message ahead of time. It is then the job of the audio program to process and trigger these events in time, and then tell the Python program to increase its position. The Python is very general, so it can be used by any program capable of receiveing and sending OSC. 
This repo comes with a set of classes for SuperCollider integration. It also contains a GUI program with MIDI interface, which can be used to manually edit the parameters used by the Patpat-SC players.

# how
## For the SuperCollider (without GUI):

### installing: 

First, create folder called "Patpat" in the folder given by executing the following command in SuperCollider:
```supercollider
Platform.userExtensionDir;
```
Then, in Scide, go to *Edit, Preferences, Interpreter*. Add the folder you just created to the *Include* section. Then, restart (maybe just Recompile The Class Library with Ctrl-Shift-L), and you should be happy as Larry.

### using:

```supercollider
s.boot; // first boot the server

p = Patpat.new(s); // initialise the Patpat class with the given server

StageLimiter.activate; // if you have the BatLib quark installed (highly recommended), then you can use this limiter to keep everything at a nice volume

// Manual stuff (the below code is automatically ran when you use the Python script)
// SETTING PARAMETERS
p.addPlayer("alfred") // you can manually add a player to p, however this is optional as trying to set a parameter of a non-existant player will automatically add one. Moreover, the Python code should specify the players as well (see below).

// you can use p.setEffectParam( PLAYER, EFFECT, PARAM, VALUE ) to change specific parameters of the effect synthdefs. This will update given parameter of the constantly running effect synth nodes
p.setEffectParam("alfred","lpf", "lpf", 10000);
p.setEffectParam("alfred","lpf", "res", 1);

// you can use p.setParam( PLAYER, PARAM, VALUE ) to change the parameters of the player's synth. The changes will be used the next time the player is triggered.
p.setParam("alfred", "synth", "any_old_synthdef")
p.setParam("alfred", "freq", 880)

// NOTE: The parameter names can be whatever you want, but it will only have an effect if the synthdef has such an argument
```



## for the Python:

### installing:

*Hopefully* you will just need to install [python-osc](https://pypi.org/project/python-osc/) with Pip. This project is Python 3+ only. Place the folder *Python* wherever the bleedin' hell ya like.

### using:

You run the program by executing *python main.py*.
You interact with the program by editing the file *user_commands.py*, and then sending an OSC message with address "/update_commands" to localhost:5005. You can do this by executing *python send_osc_message.py*, which can be found in the Python folder.
I use Vim and so I use the hotkey Ctrl-e to save and update:
```vim
nnoremap <silent> <c-e> :w<CR>:silent exec "!python send_osc_message.py"<CR>
```

The file *user_commands* consists of 2 functions: *variables* and *command*. 
The *variables* function is called every time you update the file. It contains a global dictionary *V*, for "variables". In dictionary you can store the objects **Counter or Seq**, as well as any other value. Objects stored in this dictionary will retain their value when the file is updated. You will also use this function to set the speed of the program. Another thing that you could do in this function is create new players. The *new_player* function will create a new player with a given name and synth (if only a name is given, it will automatically set the synth to be equal to the name). Make sure the synth actually exists. It work explode or anything, but it will just make SuperCollider cry :( . Really, you just want to use *variables* to run commands that you only want to be done "once".
The *command* function is the main fella. It is called every "beat". By using a sequence of if-statements, chance, and modulo arithmetic, you can create algorithmic musical patterns. As *user_commands.py* is just good ol' Python, you can define new functions wherever you want, and you can put whatever you like in *command* (except for errors). Most errors will just freeze the program until you fix the error, there are a few errors which will straight up crash it though.
There are also a few imports n' stuff at the top of the file.

Take a look in *funcs.py* to look at all the current functions. Most of them are simply shortcuts. Use *param(name,value)* to set the value of a synth param, and use *effect(effect_name, param_name, value)* to set the value of an effect param.

Here's an example:
```python
# imports n' stuff :)
from counter import Counter
from cycle import Cycle
from funcs import *
from sequence import Seq

# just a nice shortcut. So you can use _ to represent an empty bit in a Seq
_ = "_"


def variables():
    global V

    V = {"c": Counter(16), "d": Counter(9), "s": 60}

    speed(bpm(120, 4)) # bpm takes BPM and BARS

    new_player("saw") # makes a new player "saw", using synth "saw"
    toggle(1, "lpf", "delay") # toggles the effects "lpf" and "delay"
    dur(0.5) # length of each note
    delt(0.125) # shortcut for effect("delay", "delaytime", 0.125)
    lpf(5000) # shortcut for effect("lpf", "lpf", 5000)
    cut(0) # cut = 0 means that new synths will be added, rather than replacing the current (i.e, multiple notes at once)

    new_player("sin")
    dur(0.125)
    toggle(1, "lpf")
    lpf(10000)
    cut(0)


def command(t): # variable t reprents the current time. It's mostly not used for anything, because all of the functions directly reference the main time variable

    if chance(0.1): # returns true if a random number from 0-1 is less than 0.1
        p("saw") # selects the player "saw"
        dur(0.1) # sets duration of "saw"
        note(between(70, 100, 2)) # sets the note to be from 70 to 100, in intervals of 2
        trig() # triggers the sound!
    else:
        if mod(3): # returns true if t%3 == 0. i.e, once every 3 beats.
            p("saw")
            dur(0.25)
            note(50)
            trig()

    if euclid(3, 8): # eu know the drill
        p("sin")
        note(choose(60, 70, 50, 55)) # sets the note to be a randomly chosen element of [60,70,50,55]
        trig()
```

# extras

## gooey

I have also made a MIDI integrated GUI editor for the synth/effect params. To use it, simply execute the following lines in SuperCollider:
```supercollider
s.boot;
p = Patpat.new(s);
w = PatpatGui.new(p);
```
The below image shows how to use it:
![Image of the GUI](https://github.com/hatcatpat/patpat/tree/master/Examples/gui_explanation.png)

I have no idea how MIDI devices work on Windows/Mac. For Linux, you just have to connect your midi device to a SuperCollider midi input using (for example) Qjackctl.

## supercollider: post processing shenanagans

Because SuperCollider is a nice lady, you can apply your own effects/processing on top of the Patpat synths/effects. Below is an example of applying a granular synthesis filter + delay to a Patpat session.
```supercollider
s.boot;
p = Patpat.new(s);
StageLimiter.activate

(
SynthDef("messy", {
	arg freq=8, width=0.5, delay = 0.125, decay = 1;
	var input = In.ar(0,2);

	input = input + CombC.ar(input, 0, 0.25, 4);
	input = input * Pulse.ar(freq, width);
	input = input + CombC.ar(input, 0.2, delay, decay);

	ReplaceOut.ar(0, input); // use ReplaceOut to remove all the sounds before this node, use Out to simply add to it
}).add;

x.free;
x = Synth.after(p.getGroup, "messy"); // have to insert our synth after all the patpat guys
)

// execute this to randomise all the values!
(
x.set("freq", rrand(1,500));
x.set("width", rrand(0.1,0.9));
x.set("delay", rrand(0.0,0.1));
x.set("decay", rrand(0,1));
)
```

