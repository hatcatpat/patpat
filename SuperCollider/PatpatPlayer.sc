PatpatPlayer {

	var dict,effect_dict,synth_args, group, bus,samples, synth_node, server;

	*new {
		arg s,master_group,sm;
		^super.new.init(s,master_group,sm);
	}

	init{
		arg s,master_group,sm;

		server = s;

		samples = sm;

		bus = Bus.audio(numChannels:2);

		group = Group.new(master_group);

		dict = Dictionary.new;
		dict.add("synth" -> "");
		dict.add("bus" -> bus);
		dict.add("pan" -> 0);
		dict.add("vol" -> 1);
		dict.add("cut" -> 1);
		dict.add("note" -> 60);
		dict.add("fold" -> nil);
		dict.add("samp" -> nil);

		effect_dict = Dictionary.new;
		effect_dict.add("output" -> Synth.tail(group, "output", [in:bus]) );
		this.addEffect("output", "lpf");
		this.addEffect("lpf","reverb");
		this.addEffect("reverb", "delay");
		this.addEffect("delay", "decimate");
		// effect_dict.add("delay" -> Synth.before(effect_dict["output"], "Effect_Delay", [bus:bus]) );
		// effect_dict.add("reverb" -> Synth.before(effect_dict["output"], "Effect_Reverb", [bus:bus]) );
		// effect_dict.add("lpf" -> Synth.before(effect_dict["output"], "Effect_LPF", [bus:bus]) );

		this.updateArgs;
	}

	updateArgs{
		var fold,samp;
		synth_args = [];

		dict.keysValuesDo{|key, value|
			// [key, value].postln;
			synth_args = synth_args++[key,value];
		};

		fold = dict["fold"];
		samp = dict["samp"];
		if (fold != nil && samp != nil){
			if (samples[fold] != nil){
				if (samples[fold][samp] != nil){
					synth_args = synth_args++["buf", samples[fold.asString][samp] ];
				};
			};
		};
	}

	setParam{
		arg param, value;
		dict.add(param -> value);
		this.updateArgs;
	}

	setEffectParam{
		arg effect_name, param, value;
		var effect = effect_dict[effect_name];
		if (effect != nil){
			effect.set(param, value);
		}
	}

	addEffect{
		arg before_name, effect_name, args=[];
		effect_dict.add(effect_name.asString -> Synth.before(effect_dict[before_name.asString], "effect_"++effect_name, [bus:bus]++args) )
	}

	trig{
		if (dict["cut"] == 0){
			server.makeBundle(server.latency, {
				Synth.head(group, dict["synth"], synth_args);
			});
		} {
			synth_node.free;
			synth_node = Synth.head(group, dict["synth"], synth_args);
		}
	}

	getDict{
		^dict;
	}

	getEffectParams{ ^effect_dict; }

	debug{
		dict.postln;
	}

	kill{
		group.free;
	}

}