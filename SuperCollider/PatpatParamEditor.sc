PatpatParamEditor {

	var window,k,param_text,midi_text,effect_toggle,k_waiting,midi_string;

	*new {
		arg w,patpat;
		^super.new.init(w,patpat);
	}

	init {
		arg w,patpat;

		window = w;

		param_text = TextView();
		param_text.maxHeight = 25;
		param_text.hasVerticalScroller = false;
		param_text.hasHorizontalScroller = false;

		midi_text = TextView();
		midi_text.maxHeight = 25;
		midi_text.hasVerticalScroller = false;
		midi_text.hasHorizontalScroller = false;
		midi_string = [-1,-1];

		effect_toggle = CheckBox();

		k = Knob().action_({
			var string = param_text.string.split($,);
			var value = k.value;

			if (k_waiting != value){
				k_waiting = value;
			};

			if (effect_toggle.value == false){

				if (string[3] != nil){ // max
					value = value * (string[3].asInteger-string[2].asInteger);
				};
				if (string[2] != nil){ // min
					value = value + string[2].asInteger;
				};
				if (string[0] != nil && string[1] != nil){ // player, param
					patpat.setParam(string[0].asSymbol,string[1], value);
				};
			}{

				if (string[4] != nil){ // max
					value = value * (string[4].asInteger-string[3].asInteger);
				};
				if (string[3] != nil){ // min
					value = value + string[3].asInteger;
				};
				if (string[0] != nil && string[1] != nil && string[2] != nil){ // player, effect, param
					patpat.setEffectParam(string[0].asSymbol,string[1], string[2], value);
				};
			};

		});
		k.mode = \vert;

		window.layout.add( HLayout( VLayout(k,effect_toggle),param_text,midi_text ) )
	}

	midiControl{
		arg chan,knob,value;

		if (chan.asString == midi_string[0] && knob.asString == midi_string[1]){
			k_waiting = value/127;
		}

	}

	updateKnob{
		if (k_waiting != k.value){
			k.valueAction = k_waiting;
		}
	}

	updateMidiString{
		midi_string = midi_text.string.split($,);
	}

	getMidiString{ ^midi_string; }

	remove{
		k.remove;
		param_text.remove;
		midi_text.remove;
		effect_toggle.remove;
		this.kill;
	}

}