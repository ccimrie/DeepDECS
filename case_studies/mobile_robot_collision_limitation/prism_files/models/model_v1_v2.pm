dtmc

const double pcollider = 0.8;
const double pocc = 0.25;

module ManagedComponents
	z : [0..4] init 0; // 0:check collider, 1:collider detected,
	// 2:check wait, 3:no collider, 4:done
	[look] t=1 & z=0 -> pcollider:(z'=1) + (1-pcollider):(z'=3);
	[check] t=1 & z=1 -> 1:(z'=2);
	[retry] t=1 & z=2 & wait -> 1:(z'=0);
	[proceed] t=1 & z=2 & !wait -> 1:(z'=3);
	[travel] t=1 & z=3 -> 1:(z'=4);
	[end] t=1 & z=4 -> 1:(z'=4);
endmodule


const double pVerif0WhenClass0 = 0.3044099679568455;
const double pVerif0WhenClass1 = 0.30510585305105853;
const double pVerif1WhenClass0 = 0.0;
const double pVerif1WhenClass1 = 0.0;
const double pVerif2WhenClass0 = 0.08789967495792896;
const double pVerif2WhenClass1 = 0.25333570539049993;
const double pVerif3WhenClass0 = 0.6076903570852256;
const double pVerif3WhenClass1 = 0.44155844155844154;

const double pClass0AsClass0Verif0 = 0.49102612646724725;
const double pClass0AsClass1Verif0 = 0.5089738735327527;
const double pClass1AsClass0Verif0 = 0.16967930029154518;
const double pClass1AsClass1Verif0 = 0.8303206997084548;

const double pClass0AsClass0Verif1 = 0.0;
const double pClass0AsClass1Verif1 = 0.0;
const double pClass1AsClass0Verif1 = 0.0;
const double pClass1AsClass1Verif1 = 0.0;

const double pClass0AsClass0Verif2 = 0.5473380540257016;
const double pClass0AsClass1Verif2 = 0.45266194597429843;
const double pClass1AsClass0Verif2 = 0.04353932584269663;
const double pClass1AsClass1Verif2 = 0.9564606741573034;

const double pClass0AsClass0Verif3 = 0.9519745077956071;
const double pClass0AsClass1Verif3 = 0.04802549220439285;
const double pClass1AsClass0Verif3 = 0.072522159548751;
const double pClass1AsClass1Verif3 = 0.927477840451249;
module EnvironmentMonitor
  k2 : [1..2] init 1;
  v : [0..3] init 0;
	k : [1..2] init 1; //1:not on collision course (occ), 2:occ
	[monitor] t=2 -> (1-pocc)*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+(1-pocc)*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+pocc*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+pocc*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+(1-pocc)*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+(1-pocc)*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+pocc*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+pocc*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+(1-pocc)*pVerif2WhenClass0*pClass0AsClass0Verif2:(k'=1)&(v'=2)&(k2'=1)+(1-pocc)*pVerif2WhenClass0*pClass0AsClass1Verif2:(k'=1)&(v'=2)&(k2'=2)+pocc*pVerif2WhenClass1*pClass1AsClass0Verif2:(k'=2)&(v'=2)&(k2'=1)+pocc*pVerif2WhenClass1*pClass1AsClass1Verif2:(k'=2)&(v'=2)&(k2'=2)+(1-pocc)*pVerif3WhenClass0*pClass0AsClass0Verif3:(k'=1)&(v'=3)&(k2'=1)+(1-pocc)*pVerif3WhenClass0*pClass0AsClass1Verif3:(k'=1)&(v'=3)&(k2'=2)+pocc*pVerif3WhenClass1*pClass1AsClass0Verif3:(k'=2)&(v'=3)&(k2'=1)+pocc*pVerif3WhenClass1*pClass1AsClass1Verif3:(k'=2)&(v'=3)&(k2'=2);
endmodule



const double x1Verif0;
const double x1Verif1;
const double x1Verif2;
const double x1Verif3;
const double x2Verif0;
const double x2Verif1;
const double x2Verif2;
const double x2Verif3;

module Controller
	wait : bool init false;
	[decide] t=3 & k2=1 & v=0 ->  x1Verif0:(wait'=true) + (1-x1Verif0):(wait'=false);
	[decide] t=3 & k2=1 & v=1 ->  x1Verif1:(wait'=true) + (1-x1Verif1):(wait'=false);
	[decide] t=3 & k2=1 & v=2 ->  x1Verif2:(wait'=true) + (1-x1Verif2):(wait'=false);
	[decide] t=3 & k2=1 & v=3 ->  x1Verif3:(wait'=true) + (1-x1Verif3):(wait'=false);
	[decide] t=3 & k2=2 & v=0 ->  x2Verif0:(wait'=true) + (1-x2Verif0):(wait'=false);
	[decide] t=3 & k2=2 & v=1 ->  x2Verif1:(wait'=true) + (1-x2Verif1):(wait'=false);
	[decide] t=3 & k2=2 & v=2 ->  x2Verif2:(wait'=true) + (1-x2Verif2):(wait'=false);
	[decide] t=3 & k2=2 & v=3 ->  x2Verif3:(wait'=true) + (1-x2Verif3):(wait'=false);
endmodule

module Turn
	t : [1..3] init 1;
	[check] true -> 1:(t'=2);
	[monitor] true -> 1:(t'=3);
	[decide] true -> 1:(t'=1);
endmodule

rewards "time"
	[travel] true : 9.95;
	[proceed] k=2 : 2.57;
	[retry] true : 5;
endrewards

label "collision" = z=3 & k=2;
label "done" = z=4;
