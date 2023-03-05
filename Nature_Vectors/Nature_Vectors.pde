
Mover[] movers = new Mover[20];

void setup() {
  size(640, 480);
  for (int i=0; i<movers.length; i++){
    movers[i] = new Mover();
  }
  
}



void draw(){
  background(#A7C9F7);
  for (int i=0; i<movers.length; i++){
    movers[i].update();
    movers[i].checkEdgesWrap();
    movers[i].display();
  }
}
