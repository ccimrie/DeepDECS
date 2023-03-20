dtmc

module ManagedComponents
  z : [0..1] init 0;

  [driveFast] t=1 & z=0 & !slow -> 1.0:(z'=0);
  [driveSlow] t=1 & z=0 & slow -> 1.0:(z'=0);
endmodule


const double pVerif0WhenClass0 = 0.15;
const double pVerif0WhenClass1 = 0.2;
const double pVerif1WhenClass0 = 0.85;
const double pVerif1WhenClass1 = 0.8;

const double pClass0AsClass0Verif0 = 0.13333333333333333;
const double pClass0AsClass1Verif0 = 0.8666666666666667;
const double pClass1AsClass0Verif0 = 0.85;
const double pClass1AsClass1Verif0 = 0.15;

const double pClass0AsClass0Verif1 = 0.9176470588235294;
const double pClass0AsClass1Verif1 = 0.08235294117647059;
const double pClass1AsClass0Verif1 = 0.1;
const double pClass1AsClass1Verif1 = 0.9;

module EnvironmentMonitor
  k : [1..2]; // k=1 - no ice; k=2 - ice
  k2 : [1..2] init 1;
  v : [0..1] init 0;

  [monitor] t=2 -> 0.6*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+
		               0.6*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+
		               0.4*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+
		               0.4*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+
                   0.6*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+
                   0.6*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+
                   0.4*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+
                   0.4*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2);
endmodule

const double x1Verif0;
const double x1Verif1;
const double x2Verif0;
const double x2Verif1;

module Controller
  slow : bool init false;

  [decide] t=3 & k2=1 & v=0 ->  x1Verif0:(slow'=false) + (1-x1Verif0):(slow'=true);
  [decide] t=3 & k2=1 & v=1 ->  x1Verif1:(slow'=false) + (1-x1Verif1):(slow'=true);
  [decide] t=3 & k2=2 & v=0 ->  x2Verif0:(slow'=false) + (1-x2Verif0):(slow'=true);
  [decide] t=3 & k2=2 & v=1 ->  x2Verif1:(slow'=false) + (1-x2Verif1):(slow'=true);
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

