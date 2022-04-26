dtmc

// A mobile robot travels through an environment where it may encounter and potentially collide 
// with another moving autonomous agent. The collisions are not catastrophic, they do inflict 
// damage to the robot, such that expensive maintenance is needed after multiple collisions. 
// To limit the number of collisions, the robot checks, every X seconds,
// - whether the collider is present
// - and, if the collider is present, whether it is on collision course with the robot within 
//   the next X seconds  
// A controller decides, after each check that identifies the presence of the collider,
// whether the robot should move to a new waypoint within the next X seconds, or wait for 
// a short period of time at its current location.
// We have two conflicting requirements:
// - we want to minimise the time required to reach the next waypoint
// - we want to minimise the probability of collision before reaching the next waypoint

const double pColliderPresent = 0.8;
const double pCollision=0.25;

module Robot
  s : [0..3] init 0;    // 0=initial position; 1=collider present; 2=travel; 3=done 
  oncc : [0..1] init 0; // 0=not on collision course; 1=on collision course 

  [check]   !c & s=0 -> pColliderPresent*pCollision:(s'=1)&(oncc'=1) +
                        pColliderPresent*(1-pCollision):(s'=1)&(oncc'=0) +
                        (1-pColliderPresent):(s'=2)&(oncc'=0);

  [retry]   !c & s=1 & wait -> 1:(s'=0);
  [proceed] !c & s=1 & !wait -> 1:(s'=2);

  [travel]  !c & s=2 -> 1:(s'=3);
  [done]    !c & s=3 -> 1:(s'=3);  
endmodule

module Switch
  c : bool init false;

  [check]  !c -> 1:(c'=true);
  [respond] c -> 1:(c'=false);
endmodule

const double x1;
const double x2;

module Controller
  wait : bool init false;

  [respond] c & oncc=0 -> x1:(wait'=true) + (1-x1):(wait'=false);
  [respond] c & oncc=1  -> x2:(wait'=true) + (1-x2):(wait'=false);
endmodule


rewards "risk"
  [proceed] oncc=1 : 100;
endrewards

rewards "time"
  [retry]   true : 5;
//  [proceed] oncc=1: 0.5;
  [proceed] oncc=1 : 2.57;
//  [travel]  true : 2;
  [travel]  true : 9.95;
endrewards

label "collision" = s=2 & oncc=1;