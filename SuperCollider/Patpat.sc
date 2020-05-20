Patpat {

	var group, players, samples, timeline, oscFunc, speed, t, netAddr, internalNetAddr, routine, server;
	var osc_out = false;

	*new {
		arg s;
		^super.new.init(s);
	}

	init{
		arg s;

		server = s;

		players = Dictionary.new;

		group = Group.new;

		timeline = Array.fill(16, []);

		oscFunc = {
			arg msg, time, addr;
			var i;
			if (msg[0] != '/status.reply'){
				// msg.postln;
				if (msg[1] != nil){
					i = msg[1].asInteger()%timeline.size();
					timeline[i] = timeline[i]++[msg];
				};
			};
		};
		thisProcess.addOSCRecvFunc(oscFunc);

		speed = 0.25;
		t = 0;

		netAddr = NetAddr.new("127.0.0.1", 5005);
		internalNetAddr = NetAddr.new("127.0.0.1", 57120);

		routine = Routine({
			loop {
				this.process.value(t.asInteger());
				netAddr.sendMsg("/bang");
				speed.wait;
			}
		});
		TempoClock.default.sched(0, routine);

		this.loadSamples;
		this.loadSynthDefs;
	}

	getGroup{
		^group;
	}

	addPlayer{
		arg name;
		players.add(name -> PatpatPlayer.new(server,group,samples) );
		// players[name].init(group);
	}

	getPlayer{
		arg name;
		if (players[name] == nil){
			this.addPlayer(name);
		};
		^players[name];
	}

	getPlayers{ ^players; }

	trig{
		arg name;
		this.getPlayer(name).trig;

		if (osc_out == true){
			internalNetAddr.sendMsg("/patpat/trig", name, this.getPlayer(name).getDict["note"] );
		};
	}

	setOscOutput{
		arg b;
		osc_out = b;
	}

	setParam{
		arg player_name, param, value;
		this.getPlayer(player_name).setParam(param, value);
	}

	setEffectParam{
		arg player_name, effect_name, param, value;
		this.getPlayer(player_name).setEffectParam(effect_name, param, value);
	}

	getTimeline{
		^timeline;
	}

	getT{
		^t;
	}

	killPlayer{
		arg player_name;
		if (players[player_name] != nil){
			players[player_name].kill;
		}
	}

	process{

		if (timeline[t].size() > 0){
			for(0, timeline[t].size()-1, {
				arg i;
				var address = "";
				var msg = timeline[t][i];
				// ("i"+i).postln;
				// ("msg"+msg).postln;
				if (msg.size() > 0){
					address = msg[0].asString();
					// address.postln;
					if (address == "/speed"){
						speed = msg[2];
					};
					if (address == "/trig"){
						this.trig(msg[2]);
					};
					if (address.beginsWith("/param/")){
						address = address.replace("/param/","");
						this.setParam(msg[2], address, msg[3]);
					};
					if (address.beginsWith("/effect/")){
						address = address.replace("/effect/","");
						this.setEffectParam(msg[2], address, msg[3], msg[4]);
						//player, effect, param, value
					};

				};
			});
		};

		timeline[t] = [];
		t = t + 1;
		t = t % timeline.size();
	}

	loadSynthDefs{
		".local/share/SuperCollider/Extensions/Patpat/SynthDefs.scd".load;
	}

	loadSamples{
		samples = Dictionary.new;
		samples.add("foldernames" -> PathName(".local/share/SuperCollider/Extensions/Patpat/Samples").entries);
		for (0, samples["foldernames"].size-1,
			{arg i;
				samples.add(samples["foldernames"][i].folderName.asString -> samples["foldernames"][i].entries.collect({
					arg sf;
					Buffer.read(path:sf.fullPath);
				});
		)});
	}

	getSample{
		arg folder,sample;
		if (0 <= sample && sample < samples[folder.asString].size ){
			^samples[folder.asString][sample.asInteger];
		};
	}

}