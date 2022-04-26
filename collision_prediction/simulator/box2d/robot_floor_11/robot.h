#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <iostream>
#include <vector>
#include <string.h>
#include <fstream>
#include <random>
#include <chrono>
#include <tuple>
#include "box2d/box2d.h"

class robot
{
  public:
    robot();
    robot(double _radius, double _pos_x, double _pos_y, double _theta);
    b2BodyDef getBody();
    // void setVel(double _vel_x, double _vel_y);
    void setVel(double _vel_mag);
    double getVelMag();
  
    void setVelMag(double _vel_mag);

    void setPOI(std::vector<std::vector<double> > new_poi);
    std::vector<std::vector<double> > getPOI();

    double getVelX();
    double getVelY();

    double getRadius();

    void setTheta(double _theta);
    double getTheta();

    void setThetaAcc(double _theta_acc);
    double getThetaAcc();

    void updateTheta();
    double goalTheta(double x_pos, double y_pos, double x_targ, double y_targ);
    void updateVel();

    b2Body* body;

  private:
  	// Agent definitions
    b2BodyDef body_def;
    double radius;
    double sense;
    double range;


    // POI for RD
    std::vector<std::vector<double> > poi;

    // Velocity rules
    double velX;
    double velY;
    double vel_mag;
    double maxVel;

    // angular information
    double theta;
    double theta_acc;
 
  	std::tuple<double, double> rotate(double theta);

};
