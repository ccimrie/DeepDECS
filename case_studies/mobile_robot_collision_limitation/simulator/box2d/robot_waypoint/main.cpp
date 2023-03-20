#include <stdio.h>
#include <math.h>
#include <iostream>
#include <vector>
#include <string.h>
#include <fstream>
#include <sstream>
#include <stdlib.h> 
#include <vector>
#include <python3.8/Python.h>
#include<algorithm>
#include "box2d/box2d.h"
#include "robot.h"
#include <random>
#include <chrono>

#define PI 3.14159265

b2Body* defineBody(b2Body* particle, double radius, double density, double friction)
{
  // Define another box shape for our dynamic body.
  b2CircleShape dynamicCirc;
  dynamicCirc.m_radius=radius;

  // Define the dynamic body fixture.
  b2FixtureDef fixtureDef;
  fixtureDef.shape = &dynamicCirc;

  // Set the box density to be non-zero, so it will be dynamic.
  fixtureDef.density = density;

  // Override the default friction.
  fixtureDef.friction = friction;

  particle->CreateFixture(&fixtureDef);
  return particle;
}

// args: 
// -r_radius: radius of robot
// -maxVel: maximum velocity of robots
// -sns: robots' sensor range
// -rng: robots' communication range
// -TT: time of simulation
// -partStrTempRobot: file name for robot information output

std::vector<std::string> string_split(const std::string& str) {
    std::vector<std::string> result;
    std::istringstream iss(str);
    for (std::string s; iss >> s; )
        result.push_back(s);
    return result;
}

int main(int argc, char** argv)
{
    // Filepath for robot's/collider's positions
    char const * output_path=argv[1];

    std::string dir_path = output_path;

    std::ofstream outfile_robot;
    std::ofstream outfile_collider;
    outfile_robot.open((dir_path+"/robot.txt").c_str());
    outfile_collider.open((dir_path+"/collider.txt").c_str());

    B2_NOT_USED(argc);
    B2_NOT_USED(argv);
    // Define the gravity vector.
    b2Vec2 gravity(0.0f, 0.0f);
    // Construct a world object, which will hold and simulate the rigid bodies.
    b2World world(gravity);
    // Define the dynamic body. We set its position and call the body factory.

    // Initialising probability
    std::mt19937_64 rng;
    // initialize the random number generator with time-dependent seed
    uint64_t timeSeed = std::chrono::high_resolution_clock::now().time_since_epoch().count();
    std::seed_seq ss{uint32_t(timeSeed & 0xffffffff), uint32_t(timeSeed>>32)};
    rng.seed(ss);
    // initialize a uniform distribution between 0 and 1
    std::uniform_real_distribution<double> unif_p(0, 1);

    // Creating the robot
    double r_radius=0.5;
    double start_theta=90;
    robot rbt(r_radius, 0, 0, start_theta);
    b2BodyDef temp_body=rbt.getBody();
    rbt.body=world.CreateBody(&temp_body);
    rbt.body=defineBody(rbt.body, rbt.getRadius(), 40, 0.3);
    rbt.setVel(1.0);

    // Creating the collider
    double start_collider_theta=90;
    robot collider(0.5, 1, 1, start_collider_theta);
    temp_body=collider.getBody();
    collider.body=world.CreateBody(&temp_body);
    collider.body=defineBody(collider.body, collider.getRadius(), 40, 0.3);
    collider.setVelMag(0.5);
    collider.setThetaAcc(50);

    // Experimental setup
    // -- x_lim: Max starting x distance from robot
    // -- y_lim: Max starting y distance from robot
    // -- v_max: Max speed of collider
    // -- c1: rotation speed of robot is always 0 (it will always go in straight line)
    // -- c2_lim: rotation speed of collider is fixed between [-c2_lim, c2_lim]
    double x_lim=10.0;
    double y_lim=10.0;
    double v_max=2.0;
    double c2_lim=90;

    double pos_x=(1-2*unif_p(rng))*x_lim;
    double pos_y=unif_p(rng)*y_lim;
    double vel_mag=unif_p(rng)*v_max;
    double cldr_theta=unif_p(rng)*360.0;
    double cldr_theta_acc=(1-2*unif_p(rng))*c2_lim;
    
    collider.body->SetTransform(b2Vec2(pos_x,pos_y),0);
    collider.body->SetLinearVelocity(b2Vec2(0,0));
    collider.body->SetAngularVelocity(0);
    collider.setVelMag(vel_mag);
    collider.setTheta(cldr_theta);
    collider.setThetaAcc(cldr_theta_acc);

    // Prepare for simulation. Typically we use a time step of 1/60 of a
    // second (60Hz) and 10 iterations. This provides a high quality simulation
    // in most game scenarios.
    float_t timeStep = 1.0f / 60.0f;
    int32 velocityIterations = 6;
    int32 positionIterations = 2;

    b2Vec2 velocity;

    double target=10;

    int collision=0;
    int reached=0;
    while (!reached)
    {
        // Update collider's heading
        collider.updateTheta();
        collider.updateVel();
        velocity.Set(collider.getVelX(), collider.getVelY());
        collider.body->SetLinearVelocity(velocity);

        // Instruct the world to perform a single step of simulation.
        // It is generally best to keep the time step and iterations fixed.
        world.Step(timeStep, velocityIterations, positionIterations);
        
        outfile_robot << rbt.body->GetPosition().x << " " << rbt.body->GetPosition().y << " " << rbt.getTheta() << " \n";
        outfile_collider << collider.body->GetPosition().x << " " << collider.body->GetPosition().y << " " << collider.getTheta() << " \n";
            
        // Check for collision
        int numPointsRbt=0;
        for (b2ContactEdge* edge = rbt.body->GetContactList(); edge; edge = edge->next)
        {
            numPointsRbt = edge->contact->GetManifold()->pointCount;
        }

        int numPointsCldr=0;
        for (b2ContactEdge* edge = collider.body->GetContactList(); edge; edge = edge->next)
        {
            numPointsCldr = edge->contact->GetManifold()->pointCount;
        }

        if (numPointsRbt>0 && numPointsCldr>0) break;      

        double goal_theta=(180.0*rbt.goalTheta(rbt.body->GetPosition().x, rbt.body->GetPosition().y, 0, target))/PI;
        if (goal_theta>5 || goal_theta<-5) rbt.setVel(0.1);
        else rbt.setVel(1.0);
        rbt.setThetaAcc(goal_theta*0.5);
        rbt.updateTheta();
        rbt.updateVel();
        velocity.Set(rbt.getVelX(), rbt.getVelY());
        rbt.body->SetLinearVelocity(velocity);

        // Check if robot has reached goal area
        if (rbt.body->GetPosition().y>=target-0.05 && rbt.body->GetPosition().y<=target+0.05 && rbt.body->GetPosition().x<=0.05 && rbt.body->GetPosition().x>=-0.05) reached=true, printf("No collision\n");
    }
    
    return 0;
}