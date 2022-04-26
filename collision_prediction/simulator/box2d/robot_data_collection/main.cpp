#include <stdio.h>
#include <math.h>
#include <iostream>
#include <vector>
#include <string.h>
#include <fstream>
#include <stdlib.h> 
#include "box2d/box2d.h"
#include "robot.h"


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
// - outfile_path: path for result files
// - c_datasize: Number of collision instances to be recorded
// - nc_datasize: Number of no-collision instances to be recorded
// - sum: Maximum number of samples determined as c_datasize+nc_datasize

int main(int argc, char** argv)
{
    char const * path=argv[1];

    int c_datasize;
    int nc_datasize;
    int datasize;

    char path_tmp[100];
    strcpy(path_tmp, path);
    std::ofstream outfile_datapoint;
    outfile_datapoint.open(path_tmp);

    std::cout<<"Do you want to define individual sample sizes? (y/n): \n";
    int valid=0;

    std::string choice="";

    while(!valid)
    {
        std::cin>>choice;
        if(choice=="y")
        {
            valid=1;
            std::cout<<"How many collision samples: \n";
            int valid_c=0;
            while(!valid_c)
            {
                std::cin>>c_datasize;
                if(!std::cin || std::cin.fail())
                {
                    // user didn't input a number
                    std::cin.clear(); // reset failbit
                    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //skip bad input
                    // next, request user reinput
                    std::cout<<"Please input a valid number: \n";
                }
            }

            std::cout<<"How many non-collision samples: \n";
            valid_c=0;
            while(!valid_c)
            {
                std::cin>>nc_datasize;
                if(!std::cin || std::cin.fail())
                {
                    // user didn't input a number
                    std::cin.clear(); // reset failbit
                    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //skip bad input
                    // next, request user reinput
                    std::cout<<"Please input a valid number: \n";
                }
            }
            datasize=c_datasize+nc_datasize;
        }
        else if(choice=="n")
        {
            valid=1;
            std::cout<<"How many total samples: \n";
            int val_samp=0;
            while(!val_samp)
            {
                std::cin>>datasize;
                if(!std::cin || std::cin.fail())
                {
                    // user didn't input a number
                    std::cin.clear(); // reset failbit
                    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //skip bad input
                    // next, request user reinput
                    std::cout<<"Please input a valid number: \n";
                }
            }
            c_datasize=datasize;
            nc_datasize=datasize;
        }
    }

    B2_NOT_USED(argc);
    B2_NOT_USED(argv);

    // Define the gravity vector.
    b2Vec2 gravity(0.0f, 0.0f);
    // Construct a world object, which will hold and simulate the rigid bodies.
    b2World world(gravity);

    // Define the dynamic body. We set its position and call the body factory.
    srand48(time(NULL));

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

    // Prepare for simulation. Typically we use a time step of 1/60 of a
    // second (60Hz) and 10 iterations. This provides a high quality simulation
    // in most game scenarios.
    float_t timeStep = 1.0f / 60.0f;
    int32 velocityIterations = 6;
    int32 positionIterations = 2;

    double target=10;

    // Experimental setup
    // -- x_lim: Max starting x distance from robot
    // -- y_lim: Max starting y distance from robot
    // -- v_max: Max speed of collider
    // -- d_start: this can vary between 90-270 (always facing right?)
    // -- c1: rotation speed of robot is always 0 (it will always go in straight line)
    // -- c2_lim: rotation speed of collider is fixed between [-c2_lim, c2_lim]

    double x_lim=10.0;
    double y_lim=10.0;
    double v_max=2.0;

    double d_min=90;
    double d_max=270;

    double c2_lim=90;

    // Output info as data sample
    //
    // -- x: relative x distance (normalised between [-1,1])
    // -- y: relative y distance (normalised between [0,1]) (assumes always above robot?)
    // -- s: speed of collider (normalised between [0,1]) 
    // -- d: starting direction of collider (normalised between [-1,1])
    // -- c2: rotation speed of collider (normalised between [-1,1])

    int c=0;
    int nc=0;

    double nc_time_sum=0;
    double c_time_sum=0;

    int nc_done=0;
    int c_done=0;

    while(c<c_datasize || nc<nc_datasize || (c+nc<datasize))
    {
        // set collider initial position
        double pos_x=(1-2*drand48())*x_lim;
        double pos_y=drand48()*y_lim;
        double vel_mag=drand48()*v_max;
        double cldr_theta=drand48()*360.0;
        double cldr_theta_acc=(1-2*drand48())*c2_lim;

        double rec_theta;

        if (cldr_theta<=180) rec_theta=cldr_theta;
        else rec_theta=cldr_theta-360;

        rbt.body->SetTransform(b2Vec2(0,0),rbt.body->GetAngle());
        rbt.setTheta(90);
        rbt.updateVel();

        collider.body->SetTransform(b2Vec2(pos_x,pos_y),0);
        collider.body->SetLinearVelocity(b2Vec2(0,0));
        collider.body->SetAngularVelocity(0);
        collider.setVelMag(vel_mag);
        collider.setTheta(cldr_theta);
        collider.setThetaAcc(cldr_theta_acc);

        std::string data=std::to_string((collider.body->GetPosition().x-rbt.body->GetPosition().x)/x_lim)+" "+std::to_string((collider.body->GetPosition().y-rbt.body->GetPosition().y)/y_lim) + " "+std::to_string(collider.getVelMag()/v_max)+" "+std::to_string((rec_theta*PI/180.0)/PI)+" "+std::to_string(collider.getThetaAcc()/c2_lim)+" ";

        // reset robot's position and heading
        rbt.body->SetTransform(b2Vec2(0,0),rbt.body->GetAngle());
        rbt.setTheta(90);
        rbt.updateVel();

        // reset collider
        collider.body->SetTransform(b2Vec2(pos_x,pos_y),0);//collider.body->GetAngle());
        collider.body->SetLinearVelocity(b2Vec2(0,0));
        collider.body->SetAngularVelocity(0);
        collider.setVelMag(vel_mag);
        collider.setTheta(cldr_theta);
        collider.setThetaAcc(cldr_theta_acc);

        // flag for when robot reaches it's destination
        bool reached=false;

        // Set velocity
        b2Vec2 velocity;
        velocity.Set(rbt.getVelX(), rbt.getVelY());
        rbt.body->SetLinearVelocity(velocity);

        int t=0;
        int collision=0;
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
            ++t;
            
            // Check for collision
            int numPointsRbt=0;
            for (b2ContactEdge* edge = rbt.body->GetContactList(); edge; edge = edge->next) numPointsRbt = edge->contact->GetManifold()->pointCount;

            int numPointsCldr=0;
            for (b2ContactEdge* edge = collider.body->GetContactList(); edge; edge = edge->next) numPointsCldr = edge->contact->GetManifold()->pointCount;

            if (numPointsRbt>0 && numPointsCldr>0) collision=1;
            if (t>=5000) break;
          
            double goal_theta=(180.0*rbt.goalTheta(rbt.body->GetPosition().x, rbt.body->GetPosition().y, 0, target))/PI;
            if (goal_theta>5 || goal_theta<-5) rbt.setVel(0.1);
            else rbt.setVel(1.0);

            rbt.setThetaAcc(goal_theta*0.5);
            rbt.updateTheta();
            rbt.updateVel();
            velocity.Set(rbt.getVelX(), rbt.getVelY());
            rbt.body->SetLinearVelocity(velocity);

            if (rbt.body->GetPosition().y>=target-0.05 && rbt.body->GetPosition().y<=target+0.05 && rbt.body->GetPosition().x<=0.05 && rbt.body->GetPosition().x>=-0.05) reached=true;//, std::cout << "reached" << std::endl;
        }

        if (collision && nc<nc_datasize)
        {
          ++nc;
          outfile_datapoint << data << "collision" << std::endl;
        }
        else if (!collision && c<c_datasize)
        {
          ++c;  
          outfile_datapoint << data << "noCollision" << std::endl;
        } 

        if (nc%100==0 || c%100==0) printf("Count: %i %i\n", nc, c);
    }

    printf("Finished\n");

    return 0;
}