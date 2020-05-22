s.boot

p = Patpat.new(s)

StageLimiter.activate

(
SynthDef("messy", {
	arg in, freq=8, width=0.5, delay = 0.125, decay = 1;
	var input = In.ar(in,2);

	input = input + CombC.ar(input, 0, 0.25, 4);
	input = input * Pulse.ar(freq, width);
	input = input + CombC.ar(input, 0.2, delay, decay);

	ReplaceOut.ar(0, input);
}).add;

x.free;
x = Synth.after(p.getGroup, "messy");
)

// randomise me babyyyy!
(
x.set("freq", rrand(1,500));
x.set("width", rrand(0.1,0.9));
x.set("delay", rrand(0.0,0.1));
x.set("decay", rrand(0,1));
)
