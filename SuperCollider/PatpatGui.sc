PatpatGui {

	var window, patpat, editors;

	*new {
		arg p;
		^super.new.init(p);
	}

	init{
		arg p;
		var remove_button, add_button, routine;
		patpat = p;
		editors = [];

		// window.close;
		window = Window.new(":^)", Rect(800,800,300,25) ).layout_(VLayout());

		remove_button = Button(window).string_("-");
		remove_button.action_({
			this.removeParamEditor(editors.size-1);
		});
		remove_button.maxWidth = 25;

		add_button = Button(window).string_("+");
		add_button.action_({
			this.addParamEditor;
		});
		add_button.maxWidth = 25;

		window.layout.add( HLayout( remove_button,add_button ) );

		window.alwaysOnTop = true;

		window.front;

		MIDIIn.connect;
		MIDIIn.addFuncTo(\control, { arg src,chan,num,val; this.midiControl(src,chan,num,val); });

		routine = Routine{
			loop{
				editors.do({
					arg editor;
					{editor.updateMidiString}.defer;
					{editor.updateKnob}.defer;
				});
				(1/60).yield;
			}
		};
		TempoClock.default.sched(0, routine);

		window.onClose = ({ routine.stop; });
	}

	midiControl{
		arg src, chan, num, val;

		// [src,chan,num,val].postln;

		editors.do({
			arg editor;
			editor.midiControl(chan,num,val);
		});

	}

	getWindow{ ^window; }

	addParamEditor{ editors = editors.add(PatpatParamEditor(window,patpat)); }

	removeParamEditor{
		arg i;
		if (0 <= i && i < editors.size){
			editors[i].remove;
			editors.removeAt(i);
		};
	}

}