class recordingSwitch {
  PVector location;
  int hei = 50;
  int wid = 100;
  boolean overButton = false;

  recordingSwitch(int x, int y) {
    this.location = new PVector(x, y);
  }

  void display() {
    fill(255);
    strokeWeight(1);
    String text = "record";
    if (recording) {
      strokeWeight(3);
      fill(color(255, 0, 0));
      text = "recording";
    }

    rect(location.x, location.y, wid, hei);
    fill(150);
    textAlign(CENTER, CENTER);
    textSize(16);
    text(text, location.x, location.y, wid, hei);
  }

  void update() {
    if (pmouseX > location.x && pmouseX < location.x+wid && 
      pmouseY > location.y && pmouseY < location.y+hei) {
      overButton = true;
    } else {
      overButton = false;
    }
  }

  boolean overButton() {
    return overButton;
  }
}