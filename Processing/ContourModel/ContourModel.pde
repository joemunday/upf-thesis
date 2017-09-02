/*
Joe Munday
Master Thesis
Universitat Pompeu Fabra
Contour Model Interface
An interface maximising the affordances of touch screens, for use with a melody generator.
*/

import oscP5.*;
import netP5.*;


OscP5 oscP5;
NetAddress supercollider;
NetAddress python;
float xPos = 0;
int xLimit = 7;
int noteWidth = 0;
ArrayList<Integer> linePositions;
int startingNote=0;
int startingPosition = 0;
int sameContourCounter = 0;
int previousContour = 0;
int currentNote = 69;
int chordIndex = 0;
boolean moving = false;
ArrayList<PVector> noteBuffer;
ArrayList<String> chords;
ArrayList<Button> buttons;
ArrayList<Integer> notes;
int noSugs = 5;
ArrayList<String> printBuffer;
float bpm = 120;
float rate;
float frameRateVal;
PImage bg;
int NOTE_FRAME_THRESHOLD = 3;
boolean recording = false;
recordingSwitch recordButton;

void setup() {
  size(1280, 800);
  init();
  frameRate(30);
  frameRateVal = 30;


  bg = loadImage("contourBG1.png");
}


void draw() {
  background(bg);

  chordDraw();
  
  updateBuffers();

  display();
}

void mousePressed() {
  newNoteOSC((startingNote-closestContour())/noteWidth);
  startingNote = closestContour();
  startingPosition = mouseY;

}

void mouseDragged() {
  moving = true;
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

void mouseClicked() {
  if (recordButton.overButton()) {
    if (recording) {
      stopRecording();
    } else {
      startRecording();
    }
  }
}


void mouseReleased() {
  moving = false;
  OscMessage myMessage = new OscMessage("/mouseReleased");
  oscP5.send(myMessage, supercollider);
  startingNote = 7*noteWidth;
}

void movementFinished() {
  moving = false;
  int endingNote = closestContour();

  if (endingNote != startingNote) {
    newNoteOSC((startingNote-endingNote)/noteWidth);
  }
  startingNote = closestContour();
}


void newNoteOSC(int movement) {
  OscMessage myMessage = new OscMessage("/newNote");
  int newNote = 0;
  if (movement > 0) {
    if (movement > 1) {
      newNote = buttons.get(4).getNote();
    } else {
      newNote = buttons.get(3).getNote();
    }
  } else if (movement < 0) {
    if (movement < -1) {
      newNote = buttons.get(0).getNote();
    } else {
      newNote = buttons.get(1).getNote();
    }
  } else {
    newNote = buttons.get(2).getNote();
  }
  myMessage.add(newNote);
  myMessage.add(chords.get(chordIndex));
  oscP5.send(myMessage, supercollider);
  oscP5.send(myMessage, python);
  if (recording) {
    newNoteBuffer(newNote, chords.get(chordIndex));
  }
}

int closestContour() {
  int smallestDifference = height;
  int indexOfClosest = 0;
  for (int i = 0; i<linePositions.size(); i++) {
    if (Math.abs(linePositions.get(i)-mouseY) < smallestDifference) {
      indexOfClosest = i;
      smallestDifference = Math.abs(linePositions.get(i)-mouseY);
    }
  }
  return linePositions.get(indexOfClosest);
}

void newNoteBuffer(int note, String chord) {
  String printString = note+", "+chord;
  printBuffer.add(printString);
}

void oscEvent(OscMessage theOscMessage) {
  if (theOscMessage.addrPattern().equals("/newSuggestions")) {
    for (int i = 0; i<5; i++) {
      buttons.get(i).setNote(theOscMessage.get(i).intValue());
      buttons.get(i).setModel(theOscMessage.get(i+5).intValue());
      buttons.get(i).update();
    }
  }
}