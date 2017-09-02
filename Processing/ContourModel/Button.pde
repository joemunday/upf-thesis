class Button {
  //Class taken from multi choice model, used to hold suggestion data in processing
  int a, b, c, d;
  boolean overButton = false;
  color colour;
  boolean clicked = false;
  int buttonNum;
  Boolean mini = false;
  int note = 0;
  int model = 0;

  Button(int id, int ax, int bx, int cx, int dx, int note) {
    a = ax;
    b = bx;
    c = cx;
    d = dx;
    colour = color(0, 250, 0);
    buttonNum = id;
    this.note = note;
  }

  void update() {
    if (pmouseX > a && pmouseX < a+c && 
      pmouseY > b && pmouseY < b+d) {
      overButton = true;
    } else {
      overButton = false;
    }

    if (model > 40) {
      setColour(color(0, 250, 0));
    } else if (model > 30 && model < 40) {
      setColour(color(250, 250, 0));
    } else if (model > 20) {
      setColour(color(250, 150, 0));
    } else if (model >10) {
      setColour(color(250, 0, 0));
    } else {
      setColour(200);
    }
  }

  void display() {

    fill(0);
    noStroke();
    rect(a, b, c, d, 0, 0, 25, 25);

    noFill();
    strokeWeight(5);
    for (int r = b; r <= (b+d-100); r+=5) {


      stroke(lerpColor(color(colour, 100), color(0, 100), map(r, b, (b+d-100), 0, 1)));
      line(a, r, a+c, r);
    }

    fill(0, 30);
    stroke(220);
    strokeWeight(2);
    if ( overButton) {
      fill(0, 10);
    }
    if (clicked) {
      stroke(250);
      strokeWeight(3);
    }

    rect(a, b, c, d, 0, 0, 25, 25);

    stroke(color(250));
    fill(250);
    text(Integer.toString(note), a+c/2, b+d-20);
    text(model, a+c/2, b+d-40);
  }

  void setColour( color col) {
    colour = col;
  }

  color getColour() {
    return colour;
  }

  void clicked() {
    clicked = true;
  }

  void unClicked() {
    clicked = false;
  }

  void setMini() {
    mini = true;
  }

  boolean isClicked() {
    return clicked;
  }

  boolean mouseOver() {
    return overButton;
  }

  void setNote(int newNote) {
    note = newNote;
  }

  int getNote() {
    return note;
  }

  void setModel(int newModel) {
    model = newModel;
  }


  int id() {
    return buttonNum;
  }
}