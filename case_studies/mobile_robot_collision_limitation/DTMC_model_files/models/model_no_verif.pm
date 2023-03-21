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

const double pClass0AsClass0=0.7760898130431776;
const double pClass0AsClass1=0.22391018695682244;
const double pClass1AsClass0=0.09482298523394414;
const double pClass1AsClass1=0.9051770147660558;

module EnvironmentMonitor
  k2 : [1..2] init 1;
	k : [1..2] init 1; //1:not on collision course (occ), 2:occ
	[monitor] t=2 -> (1-pocc)*pClass0AsClass0:(k'=1)&(k2'=1)+(1-pocc)*pClass0AsClass1:(k'=1)&(k2'=2)+pocc*pClass1AsClass0:(k'=2)&(k2'=1)+pocc*pClass1AsClass1:(k'=2)&(k2'=2);
endmodule



const double x1; // prob. of waiting when not occ
const double x2; // prob. of waiting when occ

module Controller
	wait : bool init false;
	[decide] t=3 & k2=1 -> x1:(wait'=true) + (1-x1):(wait'=false);
	[decide] t=3 & k2=2 -> x2:(wait'=true) + (1-x2):(wait'=false);
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
