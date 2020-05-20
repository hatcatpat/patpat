s.boot; //start the server

p = Patpat.new(s) // start the patpat

StageLimiter.activate // optional, if you have the batlib quark installed



// Do this next!
(
SynthDef(\avTrk, {|in, t_trig, time= 0.01, cutoff= 400, index= 0|
	var l = In.ar(in, 1);
	var valL = Amplitude.kr(BPF.ar(BPF.ar(l, cutoff, 0.1, 5), cutoff, 0.1, 5), time, time);
	var r = In.ar(in+1, 1);
	var valR = Amplitude.kr(BPF.ar(BPF.ar(r, cutoff, 0.1, 5), cutoff, 0.1, 5), time, time);
	var pan = valR-valL;
	SendTrig.kr(t_trig, index, (valL+valR)/2 );
	SendTrig.kr(t_trig, index*(-1), pan );
}).add;
)


// This will run the program
(
//--window setup
var width= 800, height= 800;
var w= Window(":^)", Rect(99, 99, width, height), false);
var u= UserView(w, Rect(0, 0, width, height));

//--variables
var num= 25;                                   //number of tuned filter synths
var cnt= 0;        //vertical drawing position
var amps = 0.dup(num);
var pans = 0.dup(num);
var o= OSCFunc({|m|
	if (m[2] > 0){
		amps= amps.put(m[2]-1, m[3]);
	}{
		pans = pans.put(abs(m[2])-1, m[3]);
	};
}, '/tr', s.addr);
var syns= {
	arg i;
	Synth.after(p.getGroup,\avTrk, [\in, 0, \index, i+1, \cutoff, i.linexp(0, num-1, 200, 6000)]); // use this line if you have patpat running
	// Synth(\avTrk, [\in, 0, \index, i+1, \cutoff, i.linexp(0, num-1, 200, 6000)]); // use this line instead if you dont
}.dup(num);

// these are the parameters which you can change while program is running
~speed= 1;
~w = 50;
~version = 0;
~margin = width*0.3;
~clear = 0;

// main loop
u.drawFunc= {
	var wn= width/num;
	var hn = height/num;

	num.do{|i|

		switch(~version,

			0, {
				Pen.strokeRect(Rect.aboutPoint(Point( (width/2)+( (pans[i]/2)*~margin) , (height/2)+(~margin*(-1+(2*(i/num)))) ),
					amps[i].clip(0,1)*~w,
					~w*0.1
				));
			},

			1, {
				Pen.strokeRect(Rect.aboutPoint(Point( (width/2)+( (pans[i]/2)*~margin) , (height/2)+(~margin*(-1+(2*(i/num)))) ),
					amps[i].clip(0,1)*~w,
					amps[i].clip(0,1)*~w,
				));
			}

		);
	};

	if (~clear == 1){
		u.clearDrawing;
	};

	syns.do{|x| x.set(\t_trig, 1)}; //request amp data

};

// use the keys 1,2,3,4 to change some parameters on the fly!
u.keyDownAction = {
	arg view,char,modifiers,unicode,keycode;

	if (char.asString == "1"){
		~version = 0;
	};
	if (char.asString == "2"){
		~version = 1;
	};
	if (char.asString == "3"){
		~clear = 0;
	};
	if (char.asString == "4"){
		~clear = 1;
	};
};

//--window management
u.clearOnRefresh= false;
w.onClose= {
	syns.do{|x| x.free};
	x.free;
	o.free;
};
w.alwaysOnTop = true;
w.front;
u.animate = true;
CmdPeriod.doOnce({if(w.isClosed.not, {w.close})});
)


// edit these while running
~w = 20
~margin = 200
~version = 0
~version = 1

~clear = 0
~clear = 1









