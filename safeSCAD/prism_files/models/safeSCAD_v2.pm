dtmc

// probabilities pkk'_z that driver attentiveness changes from level k ∈ {1, 2, 3} to level k' ∈ {1, 2, 3} given alerts z ∈ {0, 1, . . . , 7}
const double p12_0=0.002;
const double p13_0=0.00025;
const double p11_0=1-p12_0-p13_0;
const double p21_0=0.012;
const double p23_0=0.001;
const double p22_0=1-p21_0-p23_0;
const double p31_0=0.004;
const double p32_0=0.002;
const double p33_0=1-p31_0-p32_0;

const double p12_1=0.00025;
const double p13_1=0.0001;
const double p11_1=1-p12_1-p13_1;
const double p21_1=0.05;
const double p23_1=0.0001;
const double p22_1=1-p21_1-p23_1;
const double p31_1=0.03;
const double p32_1=0.025;
const double p33_1=1-p31_1-p32_1;

const double p12_2=0.0004;
const double p13_2=0.0003;
const double p11_2=1-p12_2-p13_2;
const double p21_2=0.035;
const double p23_2=0.0003;
const double p22_2=1-p21_2-p23_2;
const double p31_2=0.018;
const double p32_2=0.015;
const double p33_2=1-p31_2-p32_2;

const double p12_3=0.00015;
const double p13_3=0.00001;
const double p11_3=1-p12_3-p13_3;
const double p21_3=0.06;
const double p23_3=0.00001;
const double p22_3=1-p21_3-p23_3;
const double p31_3=0.045;
const double p32_3=0.035;
const double p33_3=1-p31_3-p32_3;

const double p12_4=0.00005;
const double p13_4=0.0;
const double p11_4=1-p12_4-p13_4;
const double p21_4=0.075;
const double p23_4=0.0;
const double p22_4=1-p21_4-p23_4;
const double p31_4=0.08;
const double p32_4=0.03;
const double p33_4=1-p31_4-p32_4;

const double p12_5=0.0;
const double p13_5=0.0;
const double p11_5=1-p12_5-p13_5;
const double p21_5=0.095;
const double p23_5=0.0;
const double p22_5=1-p21_5-p23_5;
const double p31_5=0.15;
const double p32_5=0.02;
const double p33_5=1-p31_5-p32_5;

const double p12_6=0.00001;
const double p13_6=0.0;
const double p11_6=1-p12_6-p13_6;
const double p21_6=0.08;
const double p23_6=0.0;
const double p22_6=1-p21_6-p23_6;
const double p31_6=0.10;
const double p32_6=0.03;
const double p33_6=1-p31_6-p32_6;

const double p12_7=0.0;
const double p13_7=0.0;
const double p11_7=1-p12_7-p13_7;
const double p21_7=0.2;
const double p23_7=0.0;
const double p22_7=1-p21_7-p23_7;
const double p31_7=0.175;
const double p32_7=0.016;
const double p33_7=1-p31_7-p32_7;

// Alerts
module ManagedComponets 
 z : [0..7] init 0;

 [warn] t=1 -> 1:(z'=c);
endmodule

// Driver

const double pVerif0WhenClass0 = 0.6490498812351544;
const double pVerif0WhenClass1 = 0.6186163895486936;
const double pVerif0WhenClass2 = 0.40415738678544916;
const double pVerif1WhenClass0 = 0.3509501187648456;
const double pVerif1WhenClass1 = 0.3813836104513064;
const double pVerif1WhenClass2 = 0.5958426132145509;

const double pClass0AsClass0Verif0 = 0.8277676120768527;
const double pClass0AsClass1Verif0 = 0.12236962488563587;
const double pClass0AsClass2Verif0 = 0.049862763037511436;
const double pClass1AsClass0Verif0 = 0.554595632349412;
const double pClass1AsClass1Verif0 = 0.35109191264698825;
const double pClass1AsClass2Verif0 = 0.09431245500359971;
const double pClass2AsClass0Verif0 = 0.440852314474651;
const double pClass2AsClass1Verif0 = 0.27883908890521675;
const double pClass2AsClass2Verif0 = 0.28030859662013224;

const double pClass0AsClass0Verif1 = 0.877326565143824;
const double pClass0AsClass1Verif1 = 0.06810490693739425;
const double pClass0AsClass2Verif1 = 0.05456852791878172;
const double pClass1AsClass0Verif1 = 0.15570260801868432;
const double pClass1AsClass1Verif1 = 0.7244063838069288;
const double pClass1AsClass2Verif1 = 0.11989100817438691;
const double pClass2AsClass0Verif1 = 0.03139795664091702;
const double pClass2AsClass1Verif1 = 0.07326189882880638;
const double pClass2AsClass2Verif1 = 0.8953401445302765;
module EnvironmentMonitor
  // driver status: attentive (k = 0); semi-attentive (k = 1); or inattentive (k = 2) 
  k : [1..3] init 1; 

  k2 : [1..3] init 1;
  v : [0..1] init 0;
 // driver attentiveness changes from level k ∈ {1, 2, 3} to level k' ∈ {1, 2, 3} given alerts z ∈ {0, 1, . . . , 7}
  [monitor] k=1 & z=0 -> p11_0*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p11_0*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p11_0*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p12_0*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p12_0*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p12_0*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p13_0*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p13_0*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p13_0*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p11_0*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p11_0*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p11_0*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p12_0*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p12_0*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p12_0*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p13_0*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p13_0*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p13_0*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=2 & z=0 -> p21_0*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p21_0*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p21_0*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p22_0*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p22_0*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p22_0*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p23_0*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p23_0*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p23_0*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p21_0*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p21_0*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p21_0*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p22_0*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p22_0*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p22_0*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p23_0*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p23_0*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p23_0*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=3 & z=0 -> p31_0*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p31_0*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p31_0*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p32_0*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p32_0*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p32_0*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p33_0*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p33_0*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p33_0*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p31_0*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p31_0*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p31_0*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p32_0*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p32_0*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p32_0*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p33_0*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p33_0*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p33_0*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);

  // driver state transitions for z=1
  [monitor] k=1 & z=1 -> p11_1*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p11_1*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p11_1*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p12_1*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p12_1*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p12_1*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p13_1*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p13_1*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p13_1*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p11_1*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p11_1*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p11_1*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p12_1*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p12_1*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p12_1*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p13_1*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p13_1*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p13_1*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=2 & z=1 -> p21_1*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p21_1*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p21_1*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p22_1*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p22_1*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p22_1*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p23_1*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p23_1*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p23_1*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p21_1*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p21_1*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p21_1*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p22_1*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p22_1*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p22_1*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p23_1*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p23_1*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p23_1*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=3 & z=1 -> p31_1*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p31_1*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p31_1*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p32_1*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p32_1*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p32_1*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p33_1*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p33_1*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p33_1*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p31_1*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p31_1*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p31_1*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p32_1*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p32_1*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p32_1*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p33_1*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p33_1*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p33_1*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);

  // driver state transitions for z=2
  [monitor] k=1 & z=2 -> p11_2*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p11_2*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p11_2*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p12_2*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p12_2*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p12_2*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p13_2*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p13_2*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p13_2*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p11_2*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p11_2*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p11_2*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p12_2*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p12_2*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p12_2*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p13_2*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p13_2*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p13_2*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=2 & z=2 -> p21_2*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p21_2*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p21_2*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p22_2*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p22_2*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p22_2*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p23_2*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p23_2*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p23_2*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p21_2*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p21_2*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p21_2*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p22_2*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p22_2*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p22_2*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p23_2*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p23_2*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p23_2*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=3 & z=2 -> p31_2*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p31_2*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p31_2*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p32_2*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p32_2*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p32_2*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p33_2*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p33_2*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p33_2*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p31_2*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p31_2*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p31_2*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p32_2*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p32_2*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p32_2*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p33_2*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p33_2*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p33_2*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);

  // driver state transitions for z=3
  [monitor] k=1 & z=3 -> p11_3*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p11_3*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p11_3*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p12_3*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p12_3*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p12_3*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p13_3*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p13_3*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p13_3*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p11_3*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p11_3*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p11_3*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p12_3*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p12_3*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p12_3*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p13_3*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p13_3*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p13_3*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=2 & z=3 -> p21_3*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p21_3*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p21_3*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p22_3*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p22_3*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p22_3*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p23_3*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p23_3*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p23_3*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p21_3*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p21_3*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p21_3*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p22_3*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p22_3*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p22_3*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p23_3*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p23_3*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p23_3*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=3 & z=3 -> p31_3*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p31_3*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p31_3*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p32_3*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p32_3*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p32_3*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p33_3*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p33_3*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p33_3*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p31_3*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p31_3*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p31_3*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p32_3*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p32_3*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p32_3*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p33_3*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p33_3*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p33_3*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);

  // driver state transitions for z=4
  [monitor] k=1 & z=4 -> p11_4*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p11_4*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p11_4*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p12_4*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p12_4*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p12_4*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p13_4*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p13_4*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p13_4*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p11_4*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p11_4*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p11_4*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p12_4*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p12_4*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p12_4*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p13_4*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p13_4*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p13_4*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=2 & z=4 -> p21_4*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p21_4*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p21_4*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p22_4*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p22_4*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p22_4*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p23_4*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p23_4*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p23_4*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p21_4*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p21_4*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p21_4*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p22_4*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p22_4*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p22_4*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p23_4*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p23_4*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p23_4*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=3 & z=4 -> p31_4*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p31_4*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p31_4*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p32_4*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p32_4*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p32_4*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p33_4*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p33_4*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p33_4*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p31_4*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p31_4*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p31_4*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p32_4*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p32_4*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p32_4*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p33_4*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p33_4*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p33_4*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);

  // driver state transitions for z=5
  [monitor] k=1 & z=5 -> p11_5*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p11_5*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p11_5*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p12_5*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p12_5*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p12_5*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p13_5*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p13_5*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p13_5*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p11_5*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p11_5*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p11_5*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p12_5*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p12_5*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p12_5*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p13_5*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p13_5*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p13_5*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=2 & z=5 -> p21_5*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p21_5*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p21_5*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p22_5*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p22_5*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p22_5*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p23_5*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p23_5*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p23_5*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p21_5*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p21_5*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p21_5*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p22_5*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p22_5*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p22_5*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p23_5*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p23_5*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p23_5*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=3 & z=5 -> p31_5*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p31_5*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p31_5*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p32_5*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p32_5*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p32_5*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p33_5*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p33_5*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p33_5*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p31_5*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p31_5*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p31_5*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p32_5*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p32_5*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p32_5*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p33_5*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p33_5*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p33_5*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);

  // driver state transitions for z=6
  [monitor] k=1 & z=6 -> p11_6*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p11_6*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p11_6*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p12_6*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p12_6*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p12_6*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p13_6*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p13_6*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p13_6*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p11_6*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p11_6*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p11_6*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p12_6*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p12_6*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p12_6*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p13_6*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p13_6*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p13_6*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=2 & z=6 -> p21_6*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p21_6*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p21_6*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p22_6*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p22_6*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p22_6*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p23_6*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p23_6*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p23_6*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p21_6*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p21_6*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p21_6*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p22_6*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p22_6*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p22_6*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p23_6*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p23_6*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p23_6*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=3 & z=6 -> p31_6*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p31_6*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p31_6*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p32_6*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p32_6*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p32_6*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p33_6*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p33_6*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p33_6*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p31_6*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p31_6*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p31_6*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p32_6*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p32_6*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p32_6*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p33_6*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p33_6*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p33_6*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);

  // driver state transitions for z=7
  [monitor] k=1 & z=7 -> p11_7*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p11_7*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p11_7*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p12_7*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p12_7*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p12_7*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p13_7*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p13_7*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p13_7*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p11_7*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p11_7*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p11_7*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p12_7*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p12_7*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p12_7*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p13_7*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p13_7*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p13_7*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=2 & z=7 -> p21_7*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p21_7*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p21_7*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p22_7*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p22_7*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p22_7*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p23_7*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p23_7*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p23_7*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p21_7*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p21_7*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p21_7*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p22_7*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p22_7*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p22_7*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p23_7*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p23_7*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p23_7*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
  [monitor] k=3 & z=7 -> p31_7*pVerif0WhenClass0*pClass0AsClass0Verif0:(k'=1)&(v'=0)&(k2'=1)+p31_7*pVerif0WhenClass0*pClass0AsClass1Verif0:(k'=1)&(v'=0)&(k2'=2)+p31_7*pVerif0WhenClass0*pClass0AsClass2Verif0:(k'=1)&(v'=0)&(k2'=3)+p32_7*pVerif0WhenClass1*pClass1AsClass0Verif0:(k'=2)&(v'=0)&(k2'=1)+p32_7*pVerif0WhenClass1*pClass1AsClass1Verif0:(k'=2)&(v'=0)&(k2'=2)+p32_7*pVerif0WhenClass1*pClass1AsClass2Verif0:(k'=2)&(v'=0)&(k2'=3)+p33_7*pVerif0WhenClass2*pClass2AsClass0Verif0:(k'=3)&(v'=0)&(k2'=1)+p33_7*pVerif0WhenClass2*pClass2AsClass1Verif0:(k'=3)&(v'=0)&(k2'=2)+p33_7*pVerif0WhenClass2*pClass2AsClass2Verif0:(k'=3)&(v'=0)&(k2'=3)+p31_7*pVerif1WhenClass0*pClass0AsClass0Verif1:(k'=1)&(v'=1)&(k2'=1)+p31_7*pVerif1WhenClass0*pClass0AsClass1Verif1:(k'=1)&(v'=1)&(k2'=2)+p31_7*pVerif1WhenClass0*pClass0AsClass2Verif1:(k'=1)&(v'=1)&(k2'=3)+p32_7*pVerif1WhenClass1*pClass1AsClass0Verif1:(k'=2)&(v'=1)&(k2'=1)+p32_7*pVerif1WhenClass1*pClass1AsClass1Verif1:(k'=2)&(v'=1)&(k2'=2)+p32_7*pVerif1WhenClass1*pClass1AsClass2Verif1:(k'=2)&(v'=1)&(k2'=3)+p33_7*pVerif1WhenClass2*pClass2AsClass0Verif1:(k'=3)&(v'=1)&(k2'=1)+p33_7*pVerif1WhenClass2*pClass2AsClass1Verif1:(k'=3)&(v'=1)&(k2'=2)+p33_7*pVerif1WhenClass2*pClass2AsClass2Verif1:(k'=3)&(v'=1)&(k2'=3);
endmodule



const int x1Verif0;
const int x1Verif1;
const int x2Verif0;
const int x2Verif1;
const int x3Verif0;
const int x3Verif1;

module Controller
 c : [0..7] init 0;
 [decide] t=3 & k2=1 & v=0 ->  1:(c'=x1Verif0);
 [decide] t=3 & k2=1 & v=1 ->  1:(c'=x1Verif1);
 [decide] t=3 & k2=2 & v=0 ->  1:(c'=x2Verif0);
 [decide] t=3 & k2=2 & v=1 ->  1:(c'=x2Verif1);
 [decide] t=3 & k2=3 & v=0 ->  1:(c'=x3Verif0);
 [decide] t=3 & k2=3 & v=1 ->  1:(c'=x3Verif1);
endmodule

module Turn
 t : [1..3] init 1;

 [warn] true -> 1:(t'=2);
 [monitor] true -> 1:(t'=3);
 [decide] true -> 1:(t'=1);
endmodule

// risk when driver is not attentive
rewards "risk"
  [monitor] k=1 : 0; // no risk
  [monitor] k=2 : 1; // low risk
  [monitor] k=3 : 4; // high risk
endrewards

// driver nuisance caused by alerts
rewards "nuisance"
 [monitor] z=1 : (k=1)?6:2;
 [monitor] z=2 : (k=1)?3:1;
 [monitor] z=3 : (k=1)?8:3;
 [monitor] z=4 : (k=1)?10:3;
 [monitor] z=5 : (k=1)?16:5;
 [monitor] z=6 : (k=1)?11:4;
 [monitor] z=7 : (k=1)?20:6;
endrewards
