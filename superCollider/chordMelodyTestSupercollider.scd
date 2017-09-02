(
SynthDef(\melodyTest, {
		arg freq=400,amp=0.8;
	var env, osc,osc2;

	env = EnvGen.ar(
		/*Env.new(times:[0.1,0.5],curve:'exp')*/
		Env.adsr(attackTime:0.08)
		,doneAction:2);
	osc = SinOsc.ar(freq)+(BPF.ar(WhiteNoise.ar(),(freq+SinOsc.ar(10)*5)*2,0.0005)*40);
	// osc2 = Pan2.ar(LPF.ar(Saw.ar(freq+(SinOsc.ar(2)*0.2)),2750))*env;
	osc2 = Pan2.ar(osc)*env;

	Out.ar(0,osc2*amp);

}).add;



SynthDef(\harmonyTest2,{|out= 0 freq = 440 amp = 0.1 gate=1 lforate = 4.85 lfowidth= 0.5 cutoff= 2000 rq=0.5 pan = 0.0|

	var pulse, filter, env;

	pulse = Pulse.ar(freq*[1,33.5.midiratio],[0.2,0.1],[0.7,0.3]);

	env = EnvGen.ar(Env.adsr(0.0,1.0,0.8,3.0),gate,doneAction:2);

	//keyboard tracking filter cutoff
	filter = BLowPass4.ar(pulse,(cutoff*(env.squared))+200+freq,rq);

	Out.ar(out,Pan2.ar(Mix(filter)*env*amp,pan));

}).add;


SynthDef(\harmonyTest, {
		arg freq=400,amp=0.2;
	var env, osc;

	env = EnvGen.ar(Env.adsr(0.05,0.8,0.5,1)

/*		Env.new(times:[0.1,0.5],curve:'exp')*/


		,doneAction:2);

	osc = Pan2.ar(SinOsc.ar(freq)+(SinOsc.ar(freq*2)*0.5)+(SinOsc.ar(freq*3)*0.3)+(SinOsc.ar(freq*1.01)*0.2)+(SinOsc.ar(freq*1.99)*0.15)+(SinOsc.ar(freq*3.01)*0.1))*env;

	Out.ar(0,osc*amp);

}).add;

)

Server.default.makeGui

(
var melodySynth, harmonySynth, chordDict, ninth, maj9, min7,min6,dim7,seventh,maj7;

harmonySynth = Array.fill(4,{0;});

ninth = [0,4,7,11,14];
maj9 = [0,4,7,11,14];
min7 = [0,3,7,10];
min6 = [0,3,7,9];
dim7 = [0,3,6,9];
seventh = [0,4,7,10];
maj7 = [0,4,7,11];

chordDict = Dictionary.new;
chordDict.put("Gb9",ninth+54);
chordDict.put("Cmaj9",maj9+48);
chordDict.put("Fmin6",min6+53);
chordDict.put("Amin7",min7+57);
chordDict.put("Cdim7",dim7+60);
chordDict.put("Dmin7",min7+50);

chordDict.put("Cmaj7",maj7+48);
chordDict.put("G9",ninth+55);


chordDict.put("Gmin7",min7+55);
chordDict.put("C7",seventh+48);
chordDict.put("Fmaj7",maj7+53);
chordDict.put("Bbmaj7",maj7+46);
chordDict.put("Emin7",min7+52);
chordDict.put("A7",seventh+57);

chordDict.put("G7",seventh+55);
/*
chordDict.["Gb9"].[1].postln;*/

/*

chords.add("Gmin7");
    chords.add("C7");
    chords.add("Fmaj7");
    chords.add("Bbmaj7");
    chords.add("Emin7");
    chords.add("A7");
    chords.add("Dmin7");




chords.add("Gb9");
  chords.add("Cmaj9");
  chords.add("Gb9");
  chords.add("Cmaj9");
  chords.add("Fmin6");
  chords.add("Amin7");
  chords.add("Cdim7");
  chords.add("Dmin7");
*/

OSCdef('/newChord', {arg msg,time,addr,recvPort;
	msg.postln;

	for(0,harmonySynth.size-1, {arg i;
		harmonySynth[i].free;
	});
	chordDict.[msg[1]].postln;
	harmonySynth = Array.fill(chordDict.[msg[1].asString].size, {arg i;
		"tewt".postln;
		Synth(\harmonyTest, [\freq, chordDict.[msg[1].asString].[i].midicps]);
	});
		},"/newChord");

OSCdef('/newNote', {arg msg,time,addr,recvPort;
	melodySynth.free;
	melodySynth = Synth(\melodyTest, [\freq,msg[1].midicps]);
	msg.postln;
		},"/newNote");

OSCdef('/mouseReleased', {arg msg,time,addr,recvPort;
	melodySynth.free;
	msg.postln;
		},"/mouseReleased");
)


(var chordDict, harmonySynth,testChord;

chordDict = Dictionary.new;
chordDict.put("Gb9",[0,4,7,11,14]+54);
chordDict.put("Cmaj9",[0,4,7,11,14]+48);
chordDict.put("Fmin6",[0,3,7,9]+53);
chordDict.put("Amin7",[0,3,7,10]+58);
chordDict.put("Cdim7",[0,3,6,9]+60);
chordDict.put("Dmin7",[0,3,7,10]+50);
testChord = "Dmin7";

harmonySynth = Array.fill(chordDict.[testChord].size, {arg i;
		"tewt".postln;
		Synth(\harmonyTest, [\freq, chordDict.[testChord].[i].midicps]);
	});
)