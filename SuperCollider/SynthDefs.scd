(
//============================

SynthDef("sin", {
	arg bus=0, note=60, atk=0.0,rel=0.0,dur=0.5, vol=1,pan=0;
	var sig,env,freq;

	freq = note.midicps;
	sig = SinOsc.ar(freq);
	env = EnvGen.ar(Env.linen(atk,dur,rel), doneAction:Done.freeSelf);

	Out.ar(bus, Pan2.ar(sig,pan,env*vol) );
}).add;

SynthDef("saw", {
	arg bus=0, note=60, atk=0,rel=0,dur=0.5, vol=1,pan=0;
	var sig,env,freq;

	freq = note.midicps;
	sig = Saw.ar(freq);
	env = EnvGen.ar(Env.linen(atk,dur,rel), doneAction:Done.freeSelf);

	Out.ar(bus, Pan2.ar(sig,pan,env*vol) );
}).add;

SynthDef(\samp,
	{arg buf,bus = 0, rate = 1, vol=0.5, pan = 0, pos = 0, dur=0.5, loop=0;
		var sig,env;

		sig = Mix.ar(PlayBuf.ar(
			2,
			buf,
			BufRateScale.ir(buf) * rate,
			1,
			BufDur.kr(buf)*pos*44100,
			loop
			)
		);

		env = EnvGen.ar(Env.linen(0.0,dur,0),doneAction:Done.freeSelf);
		Out.ar(bus,Pan2.ar(sig,pan,env*vol));
}).add;

// EFFECTS
SynthDef("effect_delay", {
	arg bus=0,active=0, delaytime=0.5,maxDelaytime=2;
	var input, effect, env;
	input=In.ar(bus,2); //get two channels of input starting (and ending) on bus
	effect = Select.ar(active,[
		input,
		CombC.ar(input, delaytime:delaytime, decaytime:maxDelaytime)
	]);
	// env = EnvGen.ar( Env.perc(delaytime,maxDelaytime), doneAction:2 );
	Out.ar(bus,effect);
}).add;

SynthDef("effect_lpf", {
	arg bus=0,active=0, lpf=10000, res=1;
	var input, effect, env;
	input=In.ar(bus,2); //get two channels of input starting (and ending) on bus
	effect = Select.ar(active,[
		input,
		RLPF.ar(input, lpf, res)
	]);
	ReplaceOut.ar(bus,effect);
}).add;

SynthDef("effect_reverb", {
	arg bus=0,active=0, mix=0.33, room=0.5, damp=0.0;
	var input, effect, env;
	input=In.ar(bus,2); //get two channels of input starting (and ending) on bus
	effect = Select.ar(active,[
		input,
		FreeVerb.ar(input, mix, room, damp)
	]);
	ReplaceOut.ar(bus,effect);
}).add;

SynthDef("effect_decimate", {
	arg bus=0,active=0, rate=44100.0,bits=24;
	var input, effect, env;
	input=In.ar(bus,2); //get two channels of input starting (and ending) on bus
	effect = Select.ar(active,[
		input,
		Decimator.ar(input,rate,bits)
	]);
	ReplaceOut.ar(bus,effect);
}).add;

SynthDef("output", {
	arg in=0, out=0;
	var input = In.ar(in, 2);
	Out.ar(out, input);
}).add;

//===============================
)