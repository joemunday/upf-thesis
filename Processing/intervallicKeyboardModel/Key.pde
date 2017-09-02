class Key {
  PVector location;
  int midinote;
  int keyWidth;
  boolean whiteKey;
  String noteName;
  color colour;


  Key(int x, int y, int noteNum, boolean whiteKey, String noteName, int keyWidth) {
    location = new PVector(x, y);
    midinote = noteNum;
    this.whiteKey = whiteKey;
    this.noteName = noteName;
    this.keyWidth = keyWidth;


    if (whiteKey) {
      colour = color(250);
    } else {
      colour = color(0);
    }
  }

  void update() {
  }

  void display() {
    fill(colour);

    if (whiteKey) {
      stroke(0);
      rect(location.x, location.y, keyWidth, 40);
    } else {
      stroke(255);
      rect(location.x, location.y, keyWidth, 20);
    }
  }

  void setColour(color colour) {
    this.colour = colour;
  }

  void resetColour() {
    if (whiteKey) {
      this.colour = color(250);
    } else {
      this.colour = color(0);
    }
  }

  int getNote() {
    return midinote;
  }

  color getColour() {
    return colour;
  }
}