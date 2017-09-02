/*
Joe Munday
Master Thesis: Interfaces for Improvising with a Jazz Melody Generation System
Intervallic Keyboard Interface

Master in Sound and Music Computing
Universitat Pompeu Fabra 2016-2017

An interface based on extending the keyboard interface metaphor for touch screens, for use with a melody generator.
*/

import oscP5.*;
import netP5.*;


ArrayList<Button> buttons;
int noKeys = 5;
OscP5 oscP5;
NetAddress supercollider;
NetAddress python;
int chordIndex = 0;
ArrayList<String> chords;
ArrayList<Integer> notes;
ArrayList<String> printBuffer;
PImage bg;
boolean recording = false;
recordingSwitch recordButton;

void setup() {
  size(1280, 800);
  keyInit();
  colorMode(RGB);
  buttons = new ArrayList<Button>();
  notes = new ArrayList<Integer>();
  notes.add(55);
  notes.add(59);
  notes.add(60);
  notes.add(62);
  notes.add(69);
  for (int i = 0; i<noKeys; i++) {
    buttons.add(new Button(i, 1+(width/noKeys)*i, 0, (width/noKeys), int(height*0.75), notes.get(i)));
    buttons.get(i).setColour(color(50, 50, 50));
  }

  oscP5 = new OscP5(this, 12000);
  supercollider = new NetAddress("127.0.0.1", 57120);
  python = new NetAddress("127.0.0.1", 57125);

  chordsInit();

  printBuffer = new ArrayList<String>();
  printBuffer.add("midiNote, chord");

  recordButton = new recordingSwitch((width/2)-50, 650);

  bg = loadImage("keyboardBG1.png");
}


void draw() {
  background(color(0));

  recordButton.update();
  recordButton.display();


  chordDraw();

  for ( Button b : buttons) {
    b.update();
    b.display();
  }

  fill(color(255));

  strokeWeight(1);
  keyDraw();
}

void initKeys(int noKeys) {
  for (int i = 0; i<noKeys; i++) {
    fill(color(50, 50, 50, 180));
    rect(1+(width/noKeys)*i, 0, (width/noKeys), height*0.75);
  }
}

void mousePressed() {
  for (int i = 0; i<noKeys; i++) {
    if (buttons.get(i).mouseOver()) {
      buttons.get(i).clicked();
      OscMessage myMessage = new OscMessage("/newNote");
      myMessage.add(buttons.get(i).getNote());
      myMessage.add(chords.get(chordIndex));
      oscP5.send(myMessage, supercollider);
      oscP5.send(myMessage, python);
      if (recording) {
        newNoteBuffer(buttons.get(i).getNote(), chords.get(chordIndex));
      }
    }
  }
}


void mouseClicked() {
  if (recordButton.overButton()) {
    if (recording) {
      stopRecording();
    } else {
      startRecording();
    }
  }
}

void startRecording() {
  recording = true;
  printBuffer = new ArrayList<String>();
  printBuffer.add("midiNote, chord");
}

void stopRecording() {
  recording = false;
  saveMelody();
}
void saveMelody() {
  String[] outputArray = new String[printBuffer.size()];
  printBuffer.toArray(outputArray);
  String outputName = "MelodyOutput_" + day() +"-"+month()+"-"+year()+"_"+hour()+"-"+second()+".csv";
  saveStrings(outputName, outputArray);
}


void mouseReleased() {
  for (Button b : buttons) {
    b.unClicked();
  }

  OscMessage myMessage = new OscMessage("/mouseReleased");
  oscP5.send(myMessage, supercollider);
}

void newNoteBuffer(int note, String chord) {
  String printString = note+", "+chord;
  printBuffer.add(printString);
}

void stop() {
  OscMessage myMessage = new OscMessage("/quit");
  oscP5.send(myMessage, python);
}


void oscEvent(OscMessage theOscMessage) {
  if (theOscMessage.addrPattern().equals("/newSuggestions")) {
    for (int i = 0; i<5; i++) {
      buttons.get(i).setNote(theOscMessage.get(i).intValue());
      buttons.get(i).setModel(theOscMessage.get(i+5).intValue());
      buttons.get(i).update();
    }
    int testCounter = 0;

    for (Key aKey : whiteKeys) {
      aKey.resetColour();
    }

    for (Key aKey : blackKeys) {
      aKey.resetColour();
    }
    for (Button b : buttons) {

      for (Key aKey : whiteKeys) {
        if (aKey.getNote() == b.getNote()) {
          aKey.setColour(b.getColour());
        }
      }

      for (Key aKey : blackKeys) {
        if (aKey.getNote() == b.getNote()) {
          aKey.setColour(b.getColour());
        }
      }
    }
  }
}

void keyPressed() {
  if (key=='a') {
    buttons.get(0).clicked();
    OscMessage myMessage = new OscMessage("/newNote");
    myMessage.add(buttons.get(0).getNote());
    myMessage.add(chords.get(chordIndex));
    oscP5.send(myMessage, supercollider);
    oscP5.send(myMessage, python);
  }
  if (key=='s') {
    buttons.get(1).clicked();
    OscMessage myMessage = new OscMessage("/newNote");
    myMessage.add(buttons.get(1).getNote());
    myMessage.add(chords.get(chordIndex));
    oscP5.send(myMessage, supercollider);
    oscP5.send(myMessage, python);
  }
  if (key=='d') {
    buttons.get(2).clicked();
    OscMessage myMessage = new OscMessage("/newNote");
    myMessage.add(buttons.get(2).getNote());
    myMessage.add(chords.get(chordIndex));
    oscP5.send(myMessage, supercollider);
    oscP5.send(myMessage, python);
  }
  if (key=='f') {
    buttons.get(3).clicked();
    OscMessage myMessage = new OscMessage("/newNote");
    myMessage.add(buttons.get(3).getNote());
    myMessage.add(chords.get(chordIndex));
    oscP5.send(myMessage, supercollider);
    oscP5.send(myMessage, python);
  }
  if (key=='g') {
    buttons.get(4).clicked();
    OscMessage myMessage = new OscMessage("/newNote");
    myMessage.add(buttons.get(4).getNote());
    myMessage.add(chords.get(chordIndex));
    oscP5.send(myMessage, supercollider);
    oscP5.send(myMessage, python);
  }
}

void keyReleased() {
  for (Button b : buttons) {
    b.unClicked();
  }

  OscMessage myMessage = new OscMessage("/mouseReleased");
  oscP5.send(myMessage, supercollider);
}