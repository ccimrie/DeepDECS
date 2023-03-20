dtmc

module ManagedComponents
  z : [0..1] init 0;

  [driveFast] t=1 & z=0 & !slow -> 1.0:(z'=0);
  [driveSlow] t=1 & z=0 & slow -> 1.0:(z'=0);
endmodule

module EnvironmentMonitor
  k : [1..2]; // k=1 - no ice; k=2 - ice

  [monitor] t=2 -> 0.6:(k'=1) + 0.4:(k'=2);
endmodule

const double x1; //prob of not slowing down on non-icy road (k=1)
const double x2; //prob of not slowing down on icy road (k=1)

module Controller
  slow : bool init false;

  [decide] t=3 & k=1 -> x1:(slow'=false) + (1-x1):(slow'=true);
  [decide] t=3 & k=2 -> x2:(slow'=false) + (1-x2):(slow'=true);
endmodule

module Turn
  t : [1..3] init 1;

  [driveFast] true -> 1.0:(t'=2);
  [driveSlow] true -> 1.0:(t'=2);
  [monitor]   true -> 1.0:(t'=3);
  [decide]    true -> 1.0:(t'=1);
endmodule

rewards "risk"
  [driveFast] k=2 : 1;
endrewards

rewards "distance"
  [driveFast] true : 3;
  [driveSlow] true : 1;
endrewards
