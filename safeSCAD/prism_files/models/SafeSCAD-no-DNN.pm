dtmc

// An autonomous agent is monitoring the safety driver of a self-driving car:
// - to identify when the driver attentiveness changes between a small number 
//   of attentiveness levels 
// - to issue (1) acoustic, (2) optical and/or (3) haptic alerts if required to increase their 
//   attentiveness level
// The agent is performing the check and issuing its alerts every X seconds.
// We have two conflicting requirements:
// - We want to minimise the risk due to the driver being insufficiently attentive
// - We want to minimise the nuisance caused by the use of alerts

// Driver transition probabilities: pXY_Z = rate of moving from state X to Y when 
// the alerts a=Z, where a varies from 000=0 (no alert issued) to 111=7 (all 3 alerts 
// issued)

// Assume alerts and effectiveness are:
// * --1 = acoustic (high) 
// * -1- = optical (medium)
// * 1-- = haptic (very high)

const double p01_0=0.002;
const double p02_0=0.00025;
const double p00_0=1-p01_0-p02_0;
const double p10_0=0.012;
const double p12_0=0.001;
const double p11_0=1-p10_0-p12_0;
const double p20_0=0.004;
const double p21_0=0.002;
const double p22_0=1-p20_0-p21_0;

const double p01_1=0.00025;
const double p02_1=0.0001;
const double p00_1=1-p01_1-p02_1;
const double p10_1=0.05;
const double p12_1=0.0001;
const double p11_1=1-p10_1-p12_1;
const double p20_1=0.03;
const double p21_1=0.025;
const double p22_1=1-p20_1-p21_1;

const double p01_2=0.0004;
const double p02_2=0.0003;
const double p00_2=1-p01_2-p02_2;
const double p10_2=0.035;
const double p12_2=0.0003;
const double p11_2=1-p10_2-p12_2;
const double p20_2=0.018;
const double p21_2=0.015;
const double p22_2=1-p20_2-p21_2;

const double p01_3=0.00015;
const double p02_3=0.00001;
const double p00_3=1-p01_3-p02_3;
const double p10_3=0.06;
const double p12_3=0.00001;
const double p11_3=1-p10_3-p12_3;
const double p20_3=0.045;
const double p21_3=0.035;
const double p22_3=1-p20_3-p21_3;

const double p01_4=0.00005;
const double p02_4=0.0;
const double p00_4=1-p01_4-p02_4;
const double p10_4=0.075;
const double p12_4=0.0;
const double p11_4=1-p10_4-p12_4;
const double p20_4=0.08;
const double p21_4=0.03;
const double p22_4=1-p20_4-p21_4;

const double p01_5=0.0;
const double p02_5=0.0;
const double p00_5=1-p01_5-p02_5;
const double p10_5=0.095;
const double p12_5=0.0;
const double p11_5=1-p10_5-p12_5;
const double p20_5=0.15;
const double p21_5=0.02;
const double p22_5=1-p20_5-p21_5;

const double p01_6=0.00001;
const double p02_6=0.0;
const double p00_6=1-p01_6-p02_6;
const double p10_6=0.08;
const double p12_6=0.0;
const double p11_6=1-p10_6-p12_6;
const double p20_6=0.10;
const double p21_6=0.03;
const double p22_6=1-p20_6-p21_6;

const double p01_7=0.0;
const double p02_7=0.0;
const double p00_7=1-p01_7-p02_7;
const double p10_7=0.2;
const double p12_7=0.0;
const double p11_7=1-p10_7-p12_7;
const double p20_7=0.175;
const double p21_7=0.016;
const double p22_7=1-p20_7-p21_7;

module System
  l : [0..2] init 0; // 0=attentive, 1=semi-attentive, 2=inattentive

  // driver state transitions for a=0
  [check] !c & l=0 & a=0 -> p00_0:(l'=0) + p01_0:(l'=1) + p02_0:(l'=2);
  [check] !c & l=1 & a=0 -> p10_0:(l'=0) + p11_0:(l'=1) + p12_0:(l'=2);
  [check] !c & l=2 & a=0 -> p20_0:(l'=0) + p21_0:(l'=1) + p22_0:(l'=2);

  // driver state transitions for a=1
  [check] !c & l=0 & a=1 -> p00_1:(l'=0) + p01_1:(l'=1) + p02_1:(l'=2);
  [check] !c & l=1 & a=1 -> p10_1:(l'=0) + p11_1:(l'=1) + p12_1:(l'=2);
  [check] !c & l=2 & a=1 -> p20_1:(l'=0) + p21_1:(l'=1) + p22_1:(l'=2);

  // driver state transitions for a=2
  [check] !c & l=0 & a=2 -> p00_2:(l'=0) + p01_2:(l'=1) + p02_2:(l'=2);
  [check] !c & l=1 & a=2 -> p10_2:(l'=0) + p11_2:(l'=1) + p12_2:(l'=2);
  [check] !c & l=2 & a=2 -> p20_2:(l'=0) + p21_2:(l'=1) + p22_2:(l'=2);

  // driver state transitions for a=3
  [check] !c & l=0 & a=3 -> p00_3:(l'=0) + p01_3:(l'=1) + p02_3:(l'=2);
  [check] !c & l=1 & a=3 -> p10_3:(l'=0) + p11_3:(l'=1) + p12_3:(l'=2);
  [check] !c & l=2 & a=3 -> p20_3:(l'=0) + p21_3:(l'=1) + p22_3:(l'=2);

  // driver state transitions for a=4
  [check] !c & l=0 & a=4 -> p00_4:(l'=0) + p01_4:(l'=1) + p02_4:(l'=2);
  [check] !c & l=1 & a=4 -> p10_4:(l'=0) + p11_4:(l'=1) + p12_4:(l'=2);
  [check] !c & l=2 & a=4 -> p20_4:(l'=0) + p21_4:(l'=1) + p22_4:(l'=2);

  // driver state transitions for a=5
  [check] !c & l=0 & a=5 -> p00_5:(l'=0) + p01_5:(l'=1) + p02_5:(l'=2);
  [check] !c & l=1 & a=5 -> p10_5:(l'=0) + p11_5:(l'=1) + p12_5:(l'=2);
  [check] !c & l=2 & a=5 -> p20_5:(l'=0) + p21_5:(l'=1) + p22_5:(l'=2);

  // driver state transitions for a=6
  [check] !c & l=0 & a=6 -> p00_6:(l'=0) + p01_6:(l'=1) + p02_6:(l'=2);
  [check] !c & l=1 & a=6 -> p10_6:(l'=0) + p11_6:(l'=1) + p12_6:(l'=2);
  [check] !c & l=2 & a=6 -> p20_6:(l'=0) + p21_6:(l'=1) + p22_6:(l'=2);

  // driver state transitions for a=7
  [check] !c & l=0 & a=7 -> p00_7:(l'=0) + p01_7:(l'=1) + p02_7:(l'=2);
  [check] !c & l=1 & a=7 -> p10_7:(l'=0) + p11_7:(l'=1) + p12_7:(l'=2);
  [check] !c & l=2 & a=7 -> p20_7:(l'=0) + p21_7:(l'=1) + p22_7:(l'=2);
endmodule

module Switch
  c: bool init false;
  
  [check]   !c -> 1:(c'=true);
  [respond]  c -> 1:(c'=false);
endmodule

// Controller: 1 of 8 options used for each of the 3 driver states 
// (hence, there are 8^3 possible controller configurations) 
const int x0;
const int x1;
const int x2;

module Controller
  a : [0..7] init 0;  // current alerts a and speed level v

  // controller actions when driver is attentive
  [respond] c & l=0 -> 1:(a'=x0);
 
  // controller actions when driver is semiattentive
  [respond] c & l=1 -> 1:(a'=x1);

  // controller actions when driver is inattentive
  [respond] c & l=2 -> 1:(a'=x2);
endmodule

// Risk and nuisance are measured at the points when the regular check
// is performed

rewards "risk"
  [check] l=0 : 0; // no risk
  [check] l=1 : 1; // low risk
  [check] l=2 : 4; // high risk
endrewards

// Assume alerts and nuisance levels are:
// * --1 = acoustic (high nuisance) 
// * -1- = optical (low nuisance)
// * 1-- = haptic (very high nuisance)

rewards "nuisance" 
  [check] a=0 : 0;        // no alert, no nuisance
  [check] a=1 & l=0 : 6;
  [check] a=1 & l>0 : 2;
  [check] a=2 & l=0 : 3;
  [check] a=2 & l>0 : 1;
  [check] a=3 & l=0 : 8;
  [check] a=3 & l>0 : 3;
  [check] a=4 & l=0 : 10;
  [check] a=4 & l>0 : 3;
  [check] a=5 & l=0 : 16;
  [check] a=5 & l>0 : 5;
  [check] a=6 & l=0 : 11;
  [check] a=6 & l>0 : 4;
  [check] a=7 & l=0 : 20;
  [check] a=7 & l>0 : 6;
endrewards