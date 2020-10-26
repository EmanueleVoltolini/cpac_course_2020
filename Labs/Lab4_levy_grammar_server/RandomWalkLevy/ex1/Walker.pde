float STEPSCALE=20;

class Walker {
  PVector position;
  PVector prevPosition;
  
  Walker() {
    this.position=new PVector(width/2, height/2);
    this.prevPosition=this.position.copy();    
  }
  void draw() {    
    stroke(255);
    // your code here
    strokeWeight(3);
    line(this.prevPosition.x, this.prevPosition.y,
         this.position.x, this.position.y);
  }

  void update() {    
    PVector step;
    // your code here
    step=new PVector(random(-1,1), random(-1,1));
    step.normalize();
    float stepsize=montecarlo();
    step.mult(stepsize*STEPSCALE);
    this.prevPosition=this.position.copy(); 
    this.position.add(step);
  }
}

float montecarlo() {
  while (true) {
    /* your code here */
    float R1 = random(1);
    float p = random(1);
    float R2 = random(1);
    if(R2<R1){return p;}
    if(R2>=R1){R2 = random(1);}
    }
}
