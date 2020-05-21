s.boot; // boot the server

p = Patpat.new(s); // boot the patpat

p.setOscOutput(true); // tell patpat to send its events out to our AV program

StageLimiter.activate

(
var width= 800, height= 800;
var margin = 0.5;
var w= Window(":^)", Rect(99, 99, width, height), false);
var u= UserView(w, Rect(width*margin/2, height*margin/2, width*margin, height*margin));

// this will recieve patpat "trig" messages, m[1] is the name of the player being triggered
var o= OSCFunc({
	arg m;
	m.postln;
	if (m[1] == 'saw'){
		col = Color.black;
	};
	if (m[1] == 'sin'){
		t = 0;
	};
	if (m[2] > 70){
		col = Color.red;
	};
	~ypos = rrand(0.0,1.0);
}, '/patpat/trig');
var col = Color.white;
var t = 0;
~dur = 10;
~xpos = 0;
~ypos = 0;

u.drawFunc = {

	Pen.fillColor = col;
	Pen.fillRect( Rect(width*margin*~xpos,height*margin*~ypos,width*margin, height*margin) );

	t = t + 1;
	if (t >= ~dur){
		col = Color.white;
	};

};

~setMargin = {
	arg m;
	margin = m;
};

u.keyDownAction = {
	arg view,char,modifiers,unicode,keycode;
};

u.clearOnRefresh= true;
w.onClose= {
	o.free;
};
w.alwaysOnTop = true;
w.front;
u.animate = true;
CmdPeriod.doOnce({if(w.isClosed.not, {w.close})});
)

// editable parameters
~setMargin.value(100);
~dur = 10;

Synth("sin", [out:0,pan:0, bus:0])