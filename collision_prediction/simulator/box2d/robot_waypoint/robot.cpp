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
#include "robot.h"

#define PI 3.14159265

robot::robot()
{
	// EMPTY CONSTRUCTOR
}

robot::robot(double _radius, double _pos_x, double _pos_y, double _theta)
{
	// Box2D particle parameters
	// body.type=b2_dynamicBody;
  body_def.type=b2_dynamicBody;
	body_def.position.Set(_pos_x, _pos_y);

	// Robot sensor parameters
  radius=_radius;

  // srand48(time(NULL));
  velX=0.0;
	velY=0.0;


  // degrees (convert to radians when required)
  theta=_theta;
}

b2BodyDef robot::getBody()
{
	return body_def;
}

double robot::getVelX()
{
	// return velX;
  return cos(PI*theta/180.0)*vel_mag;
}

double robot::getVelY()
{
	// return velY;
  return sin(PI*theta/180.0)*vel_mag;
}

// void robot::setVelComps(double _vel_x, double _vel_y)
// {
//   velX=_vel_x;
//   velY=_vel_y;
//   vel_mag=sqrt(velX*velX+velY*velY);
//   theta=atan2(velY, velX);
// }

void robot::setVel(double _vel_mag)
{
  vel_mag=_vel_mag;
}

void robot::updateTheta()
{
  // Update using same timestep as in simulator (1/60)
  theta+=(1.0/60.0)*theta_acc;

  // keep theta in bound
  if (theta>360) theta=fmod(theta,360);
  else if (theta<0) theta=360+fmod(theta,360);

}

double robot::goalTheta(double x_pos, double y_pos, double x_targ, double y_targ)
{
  x_targ-=x_pos;
  y_targ-=y_pos;

  double dot=velX*x_targ+velY*y_targ;
  // double dist=sqrt(velX*velX+velY*velY)*sqrt(x_targ*x_targ+y_targ*y_targ);
  double det=velX*y_targ - x_targ*velY;
  // printf("Values %f  %f\n", dot_prod, dist);
  double goal_theta=atan2(det, dot);
  return goal_theta;
}

void robot::updateVel()
{
  velX=cos(PI*theta/180.0)*vel_mag;
  velY=sin(PI*theta/180.0)*vel_mag;
}

void robot::setTheta(double _theta)
{
  theta=_theta;
}

void robot::setThetaAcc(double _theta_acc)
{
  theta_acc=_theta_acc;
}

double robot::getThetaAcc()
{
  return theta_acc;
}

double robot::getTheta()
{
  return theta;
}

double robot::getVelMag()
{
  return vel_mag;
}

void robot::setVelMag(double _vel_mag)
{
  vel_mag=_vel_mag;
  updateVel();
}

void robot::setPOI(std::vector<std::vector<double> > new_poi)
{
  poi=new_poi;
}

std::vector<std::vector<double> > robot::getPOI()
{
  return poi;
}

double robot::getRadius()
{
  return radius;
}