void chordsInit() {
  chords = new ArrayList<String>();
  //blue moon
  //chords.add("Cmaj7");
  //chords.add("Amin7");
  //chords.add("Dmin7");
  //chords.add("G9");

  //autumn leaves
  //chords.add("Gmin7");
  //chords.add("C7");
  //chords.add("Fmaj7");
  //chords.add("Bbmaj7");
  //chords.add("Emin7");
  //chords.add("A7");
  //chords.add("Dmin7");

  //misty
  chords.add("Cmaj7");
  chords.add("A7");
  chords.add("Dmin7");
  chords.add("G7");
}


void chordDraw() {
  //if (frameCount%80 == 0) {
  if (xPos == width/2) {
    chordIndex=chordIndex+1;
    if (chordIndex >= chords.size()) {
      chordIndex = 0;
    }

    OscMessage myMessage = new OscMessage("/newChord");
    myMessage.add(chords.get(chordIndex));
    oscP5.send(myMessage, supercollider);
    oscP5.send(myMessage, python);
  }
}