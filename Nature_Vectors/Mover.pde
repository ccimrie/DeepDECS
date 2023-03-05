class Mover{
  PVector location;
  PVector velocity;
  PVector acceleration;
  float topspeed;
  
  Mover(){
    location = new PVector(random(width), random(height));
    velocity = new PVector(random(-2,2), random(-2,2));
    acceleration = new PVector(-0.001, 0.01);
    topspeed = 10;
  }
  
  void update(){
    PVector mouse = new PVector(mouseX, mouseY);
    PVector dir = PVector.sub(mouse, location);
    dir.normalize();
    dir.mult(0.5);
    acceleration = dir;
    
    velocity.add(acceleration);
    velocity.limit(topspeed);
    location.add(velocity);
//    print("velocity "+velocity.x+", " +velocity.y);

  }
  
  void display(){
   // stroke(0);
   // fill(175,0,0,80);
   // ellipse(location.x, location.y,16,16);
    
    // to draw a little Bee
    fill(255,170,0);
    stroke(0);
    ellipse(location.x,location.y,16,16);
    fill(0);
    noStroke();
    rectMode(CENTER);
    rect(location.x,location.y,2,16);
    rect(location.x+4,location.y,2,14);
    rect(location.x-4,location.y,2,14);
    // little wing
    fill(255,250,0,120);
    stroke(0,0,0,120);
    ellipse(location.x,location.y-10,4,8);

    //eye and sting
    fill(0);
    ellipse(location.x+8,location.y-4,3,3);
    line(location.x-8,location.y,location.x-10,location.y);
    
  }
  
  void checkEdgesBounce(){
      if ((location.x> width) || (location.x<0)) {
        velocity.x *= -1;
      }
      
      if ((location.y> height) || (location.y<0)) {
        velocity.y *= -1;
      }
  }
  
  void checkEdgesWrap(){
      if (location.x > width){
        location.x = 0;
      }
      if (location.x < 0){
        location.x = width;
      }
      if (location.y > height){
        location.y = 0;
      }
      if (location.y < 0){
        location.y = height;
      }

  }
}
