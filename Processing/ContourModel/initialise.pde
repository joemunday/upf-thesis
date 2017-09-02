void init() {

  oscP5 = new OscP5(this, 12000);
  supercollider = new NetAddress("127.0.0.1", 57120);
  python = new NetAddress("127.0.0.1", 57125);
  recordButton = new recordingSwitch(width - 110, height - 60);
  buttons = new ArrayList<Button>();
  notes = new ArrayList<Integer>();
  notes.add(55);
  notes.add(59);
  notes.add(60);
  notes.add(62);
  notes.add(69);
  for (int i = 0; i<noSugs; i++) {
    buttons.add(new Button(i, 1+(width/noSugs)*i, 0, (width/noSugs), int(height*0.75), notes.get(i)));
    buttons.get(i).setColour(color(50, 50, 50));
  }

  linePositions = new ArrayList<Integer>();
  noteBuffer = new ArrayList<PVector>();
  for (int i = 1; i <xLimit*2; i++) {
    linePositions.add((i*(height/xLimit/2)));
  }

  for (int i =1; i<800; i++) {
    noteBuffer.add(new PVector(-50, -50));
  }
  noteWidth = (height/xLimit/2);
  chordsInit();

  printBuffer = new ArrayList<String>();
  printBuffer.add("midiNote, chord");
}

void updateBuffers() {
  noteBuffer.remove(0);
  if (mousePressed) {
    if (!recordButton.overButton()) {
      noteBuffer.add(new PVector(width/2, mouseY));
    }
  } else {
    noteBuffer.add(new PVector(-50, -50));
  }
}

void display() {
  recordButton.update();
  recordButton.display();

  stroke(color(235, 235, 235));
  strokeWeight(1);


  rate = width/(((1/(bpm/60))*4)/(1/frameRateVal));
  xPos = (frameCount%(width/rate))*rate;

  line((width-xPos), 0, (width-xPos), height);

  for (int i = 0; i <linePositions.size(); i++) {
    strokeWeight(1);
    if (mousePressed && linePositions.get(i) == closestContour()) {
      strokeWeight(5);
    }
  }




  //CENTRE LINE
  strokeWeight(5);
  line(0, height/2, width, height/2);
  if (xPos < (width/2)+30 && xPos > (width/2)-5) {
    stroke(color(50, 235, 50));
  } else {
    stroke(color(235, 235, 235));
  }

  line(width/2, 0, width/2, height);
  if (mousePressed == true) {
    ellipse(width/2, mouseY, 20, 20);


    if (moving) {
      if (previousContour == closestContour()) {
        sameContourCounter++;
      } else {
        sameContourCounter = 0;
      }
      //NUMBER OF FRAMES FOR NOTE THRESHOLD
      if (sameContourCounter > NOTE_FRAME_THRESHOLD) {
        movementFinished();
      }
    }
  }

  previousContour = closestContour();

  for (PVector v : noteBuffer) {
    strokeWeight(0);
    noStroke();
    color fillColour = lerpColor(color(0, 213, 213), color(11, 255, 171), map(width/2-v.x, 0.0, width/2-100, 0.0, 1.0));
    fill(fillColour, map(width/2-v.x, 0.0, width/2, 250, 150));
    ellipse(v.x, v.y, v.x/18, v.x/18);
    v.x = v.x-(rate/2);
  }
  fill(0);
  if (moving) {
    fill(color(0, 213, 213));
  }

}