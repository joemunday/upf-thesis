ArrayList<Key> whiteKeys;
ArrayList<Key> blackKeys;
ArrayList<String> noteNames;
int startNote = 12;
int endNote = 96;


void keyInit() {
  noteNames = new ArrayList<String>();
  noteNames.add("C");
  noteNames.add("C#");
  noteNames.add("D");
  noteNames.add("D#");
  noteNames.add("E");
  noteNames.add("F");
  noteNames.add("F#");
  noteNames.add("G");
  noteNames.add("G#");
  noteNames.add("A");
  noteNames.add("A#");
  noteNames.add("B");

  whiteKeys = new ArrayList<Key>();
  blackKeys = new ArrayList<Key>();
  int keyWidth = (width-20)/(endNote-startNote);
  int startPosition = keyWidth+235;

  for (int i = startNote; i < endNote; i++) {
    String noteName = noteNames.get(i%12);
    boolean whiteNote = true;
    if (noteName.length() > 1) {
      whiteNote = false;
    }
    int index = i-startNote;
    if (whiteNote) {
      whiteKeys.add(new Key(startPosition+10, height-50, i, whiteNote, noteName, keyWidth));
      startPosition+=keyWidth;
    } else {
      blackKeys.add(new Key(startPosition+(keyWidth/2)-5, height-50, i, whiteNote, noteName, keyWidth));
      //startPosition+=keyWidth/2;
    }
  }

}

void keyDraw() {

  for (Key aKey : whiteKeys) {
    aKey.display();
  }
  for (Key aKey : blackKeys) {
    aKey.display();
  }
}