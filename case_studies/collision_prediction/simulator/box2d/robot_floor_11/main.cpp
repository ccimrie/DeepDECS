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
#include <map>

#define PI 3.14159265

struct Vector2
{
  float x;
  float y;
};

std::vector<b2Vec2> GetBodyVertices(b2Body* body)
{
    std::vector<b2Vec2> vertices;
    for (b2Fixture* f = body->GetFixtureList(); f; f = f->GetNext())
    {

        b2Shape::Type shapeType = f->GetType();
        // if ( shapeType == b2Shape::e_circle )
        // {
        //     b2CircleShape* circleShape = (b2CircleShape*)f->GetShape();
        // }
        if ( shapeType == b2Shape::e_polygon )
        {
            b2PolygonShape* polygonShape = (b2PolygonShape*)f->GetShape();

            // Assuming all objects are boxes (only 4 vertices)
            for (int i=0; i<4; ++i)
            {
                b2Vec2 v;
                v.x=polygonShape->m_vertices[i].x;
                v.y=polygonShape->m_vertices[i].y;
                v+=body->GetPosition();
                // printf("%f  %f\n", v.x, v.y);
                vertices.push_back(v);
                // //Rotate around body center to add body rotation to the vertex
                // v.rotateAround(body.getPosition(),body.getAngle()* MathUtils.radiansToDegrees);
                // vertices.add(v);
            }   
        }
    }
    return vertices;
}

b2Vec2 GetClosestPointInLine(b2Vec2 point,b2Vec2 linePoint1,b2Vec2 linePoint2){
    b2Vec2 closest;//=new Vector2();
    b2Vec2 bVec1;//=new Vector2();
    b2Vec2 bVec2;//=new Vector2();
    bVec1.Set(linePoint2.x, linePoint2.y);
    bVec1-=linePoint1; //LINE FROM POINT 1 to 2
    bVec2.Set(point.x, point.y);
    bVec2-=linePoint1; //LINE FROM VERTEX TO POINT 1

    float av=bVec1.x*bVec1.x+bVec1.y*bVec1.y;
    float bv=bVec2.x*bVec1.x+bVec2.y*bVec1.y;
    float t=bv/av;
    //IF POINT LIES OUTSIDE THE LINE SEGMENT, THEN WE FIX IT TO ONE OF THE END POINTS
    if(t<0) t=0;
    if(t>1) t=1.0f;
    //Closest point = point 1 + line from point 1 to 2 * t
    closest.Set(linePoint1.x, linePoint1.y);
    closest+=b2Vec2(bVec1.x*t,bVec1.y*t);
    return closest;
}

float  BOX_TO_WORLD=100.0f;
float   WORLD_TO_BOX =0.01f; 
float ConvertToBoxCoordinate(float v)
{
    return v*WORLD_TO_BOX;
}

// public static float ConvertToWorldCoordinate(float v){
//     return v*BOX_TO_WORLD;
// }
//THIS HANDLES ONLY POLYGON SHAPES
//AND A CIRCLE SHAPE
float getDistance(b2Body* b, b2Vec2 startPoint){
    b2Vec2 closestPoint;
    //Convert to Box Coordinates
    // float sx=ConvertToBoxCoordinate(startPoint.x);
    // float sy=ConvertToBoxCoordinate(startPoint.y);
    float sx=startPoint.x;
    float sy=startPoint.y;
    b2Vec2 boxPoint(sx,sy);
    float minDis=10e1000;
    std::vector<b2Vec2> vs=GetBodyVertices(b);
    // boolean supportedShape=false;
    for(int i=0;i<vs.size();i++)
    {
        // supportedShape=true;
        b2Vec2 closest=GetClosestPointInLine(boxPoint,vs[i],vs[(i+1)%vs.size()]);
        float d=b2Distance(closest, boxPoint);
        //Loop through edges to find the edge closest to the point
        if(d<minDis) {
            minDis=d;
            closestPoint.Set(closest.x, closest.y);
        }
    }
    return minDis;
}

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

std::vector<int> dijkstraPath(std::map<int, std::vector<int>> edges, std::vector< std::vector<float>> vertices, int start, int end)
{
    std::map<int, std::vector<float>> dist;

    std::vector<int> Q;

    for(int i=0; i<vertices.size(); ++i)
    {
        std::vector<float> val;
        val.push_back(9999);
        val.push_back(-1);
        dist[int(vertices[i][0])]=val;
        Q.push_back(vertices[i][0]);
    }
    dist[start][0]=0;

    std::vector<int> journey;
    bool found=false;
    while(Q.size()>0 && !found)
    {
        // u ← vertex in Q with min dist[u]
        double min_dist=dist[Q[0]][0];
        int u=Q[0];
        for (int i=1; i<Q.size(); ++i) 
        {
            if(dist[Q[i]][0]<min_dist) u=Q[i], min_dist=dist[Q[i]][0];
        }
        // remove u from Q
        auto it=Q.begin();
        while (it!=Q.end())
        {
            if((*it)==u)
            {
                Q.erase(it);
                break;
            }
            else ++it;
        }
        // for each neighbor v of u still in Q:
        //     alt ← dist[u] + Graph.Edges(u, v)
        //     if alt < dist[v]:              
        //         dist[v] ← alt
        //         prev[v] ← u
        // printf("%li\n\n", edges[u].size());
        for(int i=0; i<edges[u].size(); ++i)
        {
            if(!found)
            {
                // printf("%i  FOUND\n", found);
                int con=edges[u][i];
                if(std::find(Q.begin(), Q.end(),con)!=Q.end())
                {
                    double new_dist=dist[u][0]+10;
                    if(dist[con][0]>new_dist) dist[con][0]=new_dist, dist[con][1]=float(u);//, printf("New u %f  %f\n", float(u), dist[con][1]);
                }
                if (con==end)
                {
                    journey.insert(journey.begin(), con);
                    int v=dist[con][1];
                    journey.insert(journey.begin(), v);
                    while(v!=start)
                    {
                        v=dist[v][1];
                        journey.insert(journey.begin(), v);
                    }
                    found=true;
                }                
            }
            else break;
        }
    }
    return journey;
}

std::vector<std::string> string_split(const std::string& str) {
    std::vector<std::string> result;
    std::istringstream iss(str);
    for (std::string s; iss >> s; )
        result.push_back(s);
    return result;
}

using namespace std;

int main(int argc, char** argv)
{
    // Path to waypoints and objects
    char const * way_point_path=argv[1];
    char const * objects_path=argv[2];

    // Output files for waypoints, robot and collider positions
    // Output dir for waypoints, robot/collider positions, and setup
    // char const * way_points_final=argv[3];
    // char const * robot_pos_path=argv[4];
    // char const * collider_pos_path=argv[5];
    char const * output_path=argv[3];

    // Path to data buckets
    char const * partStrTempCollisionDataPath=argv[4];
    char const * partStrTempNoCollisionDataPath=argv[5];
    char const * col_pred_path=argv[6];
    char const * no_col_pred_path=argv[7];

    // Controller hyperparameters
    // // For two verify
    double x0=std::stof(argv[8]);
    double x1=std::stof(argv[9]);
    double x2=std::stof(argv[10]);
    double x3=std::stof(argv[11]);
    double x4=std::stof(argv[12]);
    double x5=std::stof(argv[13]);
    double x6=std::stof(argv[14]);
    double x7=std::stof(argv[15]);

    // Create output files
    std::string dir_path = output_path;

    std::ofstream outfile_waypoints;
    outfile_waypoints.open((dir_path+"/waypoints.txt").c_str());

    std::ofstream outfile_robot;
    outfile_robot.open((dir_path+"/rbt_pos.txt").c_str());

    std::ofstream outfile_collider;
    outfile_collider.open((dir_path+"/collider_pos.txt").c_str());

    std::ofstream outfile_setup;
    outfile_setup.open((dir_path+"/setup.txt").c_str());

    std::ofstream outfile_path;
    outfile_path.open((dir_path+"/path.txt").c_str());

    std::ofstream outfile_collisions;
    outfile_collisions.open((dir_path+"/collisions.txt").c_str());

    // Load data buckets
    std::ifstream collision_file(partStrTempCollisionDataPath, std::ios::in);
    // std::istringstream collision_file(partStrTempCollisionDataPath);
    std::ifstream no_collision_file(partStrTempNoCollisionDataPath, std::ios::in);
    std::vector< std::vector< std::vector<double>>> data(2);
    std::string str;
    while (std::getline(collision_file,str))
    {
        if (str.length()>0)
        {
            std::vector<std::string> str_split=string_split(str);
            std::vector<double> point;
            for (int i=0; i<str_split.size(); ++i) point.push_back(std::stof(str_split[i]));
            data[0].push_back(point);
        }
    }

    while (std::getline(no_collision_file,str))
    {
        if (str.length()>0)
        {
            std::vector<std::string> str_split=string_split(str);
            std::vector<double> point;
            for (int i=0; i<str_split.size(); ++i) point.push_back(std::stof(str_split[i]));
            data[1].push_back(point);
        }
    }  

    // Load predictions
    std::ifstream col_pred_file(col_pred_path, std::ios::in);
    std::ifstream no_col_pred_file(no_col_pred_path, std::ios::in);
    std::vector< std::vector< std::vector<int>>> predictions(2);
    while (std::getline(col_pred_file,str))
    {
        if (str.length()>0)
        {
           std::vector<std::string> str_split=string_split(str);
           std::vector<int> pred; 
           pred.push_back(std::stoi(str_split[0]));
           if (str_split[1]=="True") pred.push_back(1);
           else pred.push_back(0);
           if (str_split[2]=="True") pred.push_back(1);
           else pred.push_back(0);
           predictions[0].push_back(pred);
        }
    }
    while (std::getline(no_col_pred_file,str))
    {
        if (str.length()>0)
        {
           std::vector<std::string> str_split=string_split(str);
           std::vector<int> pred; 
           pred.push_back(std::stoi(str_split[0]));
           if (str_split[1]=="True") pred.push_back(1);
           else pred.push_back(0);
           if (str_split[2]=="True") pred.push_back(1);
           else pred.push_back(0);
           predictions[1].push_back(pred);
        }
    }

    double collision_size=data[0].size();
    double no_collision_size=data[1].size();

    // Reading in way points
    map<int, vector<int>> edges = {};
 
    std::ifstream way_point_file(way_point_path, std::ios::in);
    vector< vector<float>> waypoints;
    // std::string str;
    while (std::getline(way_point_file,str))
    {
        if (str.length()>0)
        {
            vector<std::string> str_split=string_split(str);
            vector<float> vertex; 
            vertex.push_back(std::stof(str_split[0]));
            vertex.push_back(std::stof(str_split[1]));
            vertex.push_back(std::stof(str_split[2]));
            waypoints.push_back(vertex);

            vector<int> connections;
            for(int i=3; i<str_split.size(); ++i) connections.push_back(stoi(str_split[i]));//, printf("Value: %i\n", connections.back());
            edges[std::stof(str_split[0])]=connections;
        }
    }

    B2_NOT_USED(argc);
    B2_NOT_USED(argv);
    // Define the gravity vector.
    b2Vec2 gravity(0.0f, 0.0f);
    // Construct a world object, which will hold and simulate the rigid bodies.
    b2World world(gravity);
    // Define the dynamic body. We set its position and call the body factory.

    // creating objects
    std::ifstream objects_file(objects_path, std::ios::in);

    vector<b2Body*> objects;
    while (std::getline(objects_file,str))
    {
        if (str.length()>0)
        {
            vector<std::string> str_split=string_split(str);
            b2BodyDef bodyDef;
         // bodyDef.type = b2_dynamicBody;
            bodyDef.position.Set(stof(str_split[0]), stof(str_split[1]));
            // b2Body* body = world.CreateBody(&bodyDef);
            objects.push_back(world.CreateBody(&bodyDef));
            b2PolygonShape objectBox;
            objectBox.SetAsBox(stof(str_split[2]), stof(str_split[3]));
            objects.back()->CreateFixture(&objectBox,0.0f);
        }
    }    

    // Removing bad waypoints
    double thresh=15;
    auto it = waypoints.begin();
    while (it != waypoints.end())
    {
        b2Vec2 start;
        start.x=(*it)[1];
        start.y=(*it)[2];
        bool bad=false;
        for(int j=0; j<objects.size(); ++j)
        {   
            double dist=getDistance(objects[j], start);
            if (dist<thresh)
            {
                bad=true;  
                break;
            }
        }
        if(bad) it=waypoints.erase(it);
        else
        {
            outfile_waypoints << (*it)[1] << " " << (*it)[2] << endl;
            // edges.erase((*it)[0]);
            ++it;
        }
    }
    outfile_waypoints.close();

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
    double start_theta=0.0;
    robot rbt(r_radius, 0, 0, start_theta);
    b2BodyDef temp_body=rbt.getBody();
    rbt.body=world.CreateBody(&temp_body);
    rbt.body=defineBody(rbt.body, rbt.getRadius(), 40, 0.3);
    rbt.setVel(1.0);
    rbt.updateVel();

    // Creating the collider
    double start_collider_theta=90;
    robot collider(0.5, 1, 1, start_collider_theta);
    temp_body=collider.getBody();
    collider.body=world.CreateBody(&temp_body);
    collider.body=defineBody(collider.body, collider.getRadius(), 40, 0.3);
    collider.setVelMag(0.5);
    collider.setThetaAcc(50);
    double pos_x;
    double pos_y;
    double vel_mag;
    double cldr_theta;
    double cldr_theta_acc;

    // Model setup
    double p_cldr_presence=0.8;
    double p_collision=0.25;

    // Creating mission start/end
    int ind_start=unif_p(rng)*waypoints.size();
    int ind_end=unif_p(rng)*waypoints.size();
   
    int start=waypoints[ind_start][0];
    int end=waypoints[ind_end][0];

    outfile_setup << waypoints[ind_start][1] << " " << waypoints[ind_start][2] << endl;
    outfile_setup << waypoints[ind_end][1] << " " << waypoints[ind_end][2];

    // Initialise robot's starting position
    rbt.body->SetTransform(b2Vec2(waypoints[ind_start][1],waypoints[ind_start][2]),0);

    collider.body->SetTransform(b2Vec2(1000,1000),0);

    // Get path
    vector<int> path=dijkstraPath(edges, waypoints, start, end);

    std::map<int, vector<float>> vertices;
    for (int i=0; i<waypoints.size(); ++i)
    {
        vector<float> point;
        point.push_back(waypoints[i][1]);
        point.push_back(waypoints[i][2]);
        vertices[int(waypoints[i][0])]=point;
    }

    // Prepare for simulation. Typically we use a time step of 1/60 of a
    // second (60Hz) and 10 iterations. This provides a high quality simulation
    // in most game scenarios.
    float_t timeStep = 1.0f / 60.0f;
    int32 velocityIterations = 6;
    int32 positionIterations = 2;

    int c_count=0;
    double risk=100;

    std::vector<double> risk_vec;
    std::vector<double> time_vec;

    // Global time (also includes rotating time)
    int tg=0;

    double wait=5*60;

    b2Vec2 velocity;
    for(int i=1; i<path.size(); ++i)
    {
        outfile_path << vertices[path[i]][0] << " " << vertices[path[i]][1] << endl;

        bool reached=false;
        double x_target=vertices[path[i]][0];
        double y_target=vertices[path[i]][1];
        double epsilon=0.05;

        // Remove collider from view
        pos_x=1000;
        pos_y=1000;
        collider.body->SetTransform(b2Vec2(pos_x,pos_y),0);//collider.body->GetAngle());
        collider.body->SetLinearVelocity(b2Vec2(0,0));
        collider.body->SetAngularVelocity(0);
        collider.setVelMag(0);
        collider.setTheta(0);
        collider.setThetaAcc(0);

        rbt.setVel(0.0);
        rbt.updateVel();
        velocity.Set(rbt.getVelX(), rbt.getVelY());
        rbt.body->SetLinearVelocity(velocity);
        // world.Step(timeStep, velocityIterations, positionIterations);
    
        // Robot turn to face waypoint

        // Need to set a velocity so vector has magnitude, but this is not passed to particle body
        rbt.setVel(1.0);
        rbt.updateVel();
        double goal_theta=(180.0*rbt.goalTheta(rbt.body->GetPosition().x, rbt.body->GetPosition().y, x_target, y_target))/PI;
        while(goal_theta>5 || goal_theta<-5)
        {
            world.Step(timeStep, velocityIterations, positionIterations);
            ++tg;

            // Record robot/collider positions
            outfile_robot << rbt.body->GetPosition().x << " " << rbt.body->GetPosition().y << " " << rbt.getTheta() << " " << start << " " << end << " \n";
            outfile_collider << collider.body->GetPosition().x << " " << collider.body->GetPosition().y << " " << collider.getTheta() << " \n";

            goal_theta=(180.0*rbt.goalTheta(rbt.body->GetPosition().x, rbt.body->GetPosition().y, x_target, y_target))/PI;

            rbt.setThetaAcc(goal_theta*0.5);
            rbt.updateTheta();
            
            // Need to update vel vector, but again this is not passed to particle
            rbt.updateVel();
        }

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

        // Mission time between waypoints
        double t=0;
        int travel=0; // Should the robot travel?

        // reset collider; draw from data buckets
        while (!travel)
        {
            int ind;
            int coll_flag;
            int no_collide; 
            if(unif_p(rng)<p_cldr_presence)
            {
                if (unif_p(rng)<p_collision) no_collide=0, ind=unif_p(rng)*collision_size;
                else no_collide=1, ind=unif_p(rng)*no_collision_size;
                
                double temp_pos_x=data[no_collide][ind][0]*x_lim;
                double temp_pos_y=data[no_collide][ind][1]*y_lim;

                double rotate_theta=rbt.getTheta()-90;
                double rotate_theta_rads=PI*rotate_theta/180.0;

                pos_x=(temp_pos_x*cos(rotate_theta_rads)-temp_pos_y*sin(rotate_theta_rads))+rbt.body->GetPosition().x;
                pos_y=(temp_pos_x*sin(rotate_theta_rads)+temp_pos_y*cos(rotate_theta_rads))+rbt.body->GetPosition().y;
                vel_mag=data[no_collide][ind][2]*v_max;
                cldr_theta=data[no_collide][ind][3]*PI*180.0/PI + rotate_theta;
                cldr_theta_acc=data[no_collide][ind][4]*c2_lim;

                // DNN prediction (no verification)
                //Run a python function(?)       
                int label=predictions[no_collide][ind][0];
                int v1=predictions[no_collide][ind][1];
                int v2=predictions[no_collide][ind][2];

                double p_x;

                // For two verify (NN has flipped labels from model)
                if (label==1 && v2==0 && v1==0) p_x=x0;
                else if (label==1 && v2==0 && v1==1) p_x=x1;
                else if (label==1 && v2==1 && v1==0) p_x=x2;
                else if (label==1 && v2==1 && v1==1) p_x=x3;
                else if (label==0 && v2==0 && v1==0) p_x=x4;
                else if (label==0 && v2==0 && v1==1) p_x=x5;
                else if (label==0 && v2==1 && v1==0) p_x=x6;
                else if (label==0 && v2==1 && v1==1) p_x=x7;

                if (unif_p(rng)<1-p_x) travel=1;

            }
            else
            {
                pos_x=1000;
                pos_y=1000;
                vel_mag=0;
                cldr_theta=90;
                cldr_theta_acc=0;
                travel=1;           
            }
            if (travel==0)
            {   

                collider.body->SetTransform(b2Vec2(pos_x,pos_y),0);
                collider.body->SetLinearVelocity(b2Vec2(0,0));
                collider.body->SetAngularVelocity(0);
                collider.setVelMag(vel_mag);
                collider.setTheta(cldr_theta);
                collider.setThetaAcc(cldr_theta_acc);

                // t+=wait;
                int tt=0;
                rbt.setVel(0.0);
                rbt.updateVel();
                velocity.Set(rbt.getVelX(), rbt.getVelY());
                rbt.body->SetLinearVelocity(velocity);

                b2Fixture* fixture_temp=rbt.body->GetFixtureList();
                fixture_temp->SetDensity(10e5f);
                rbt.body->ResetMassData();

                while (tt<wait) 
                {
                    world.Step(timeStep, velocityIterations, positionIterations);
                    ++tg;
                    ++t;
                    ++tt;

                    // Record robot/collider positions
                    outfile_robot << rbt.body->GetPosition().x << " " << rbt.body->GetPosition().y << " " << rbt.getTheta() << " " << start << " " << end << " \n";
                    outfile_collider << collider.body->GetPosition().x << " " << collider.body->GetPosition().y << " " << collider.getTheta() << " \n";
                    
                    // Update collider's heading
                    collider.updateTheta();
                    collider.updateVel();
                    velocity.Set(collider.getVelX(), collider.getVelY());
                    collider.body->SetLinearVelocity(velocity);
                }
            }
        }
        
        b2Fixture* fixture_temp=rbt.body->GetFixtureList();
        fixture_temp->SetDensity(40);
        rbt.body->ResetMassData();

        collider.body->SetTransform(b2Vec2(pos_x,pos_y),0);//collider.body->GetAngle());
        collider.body->SetLinearVelocity(b2Vec2(0,0));
        collider.body->SetAngularVelocity(0);
        collider.setVelMag(vel_mag);
        collider.setTheta(cldr_theta);
        collider.setThetaAcc(cldr_theta_acc);

        int collision=0; // Flag for checking collision only once
        
        while (!reached)
        {
            // Instruct the world to perform a single step of simulation.
            // It is generally best to keep the time step and iterations fixed.
            world.Step(timeStep, velocityIterations, positionIterations);
            ++tg;
            ++t;

            // Record robot/collider positions
            outfile_robot << rbt.body->GetPosition().x << " " << rbt.body->GetPosition().y << " " << rbt.getTheta() << " " << start << " " << end << " \n";
            outfile_collider << collider.body->GetPosition().x << " " << collider.body->GetPosition().y << " " << collider.getTheta() << " \n";
            
            goal_theta=(180.0*rbt.goalTheta(rbt.body->GetPosition().x, rbt.body->GetPosition().y, x_target, y_target))/PI;
            if (goal_theta>5 || goal_theta<-5) rbt.setVel(0.1);
            else rbt.setVel(1.0);
            rbt.setThetaAcc(goal_theta*0.5);
            rbt.updateTheta();
            rbt.updateVel();
            velocity.Set(rbt.getVelX(), rbt.getVelY());
            rbt.body->SetLinearVelocity(velocity);

            // Update collider's heading
            collider.updateTheta();
            collider.updateVel();
            velocity.Set(collider.getVelX(), collider.getVelY());
            collider.body->SetLinearVelocity(velocity);

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

            // if (numPointsRbt>0 && numPointsCldr>0) break;
            if (numPointsRbt>0 && numPointsCldr>0 && !collision)
            {
                double x_coll=(rbt.body->GetPosition().x+collider.body->GetPosition().x)/2;
                double y_coll=(rbt.body->GetPosition().y+collider.body->GetPosition().y)/2;
                outfile_collisions << x_coll << " " << y_coll << " " << tg << endl;
                collision=1;
            } 


            // Check if robot has reached goal area
            if (rbt.body->GetPosition().y>=y_target-epsilon && rbt.body->GetPosition().y<=y_target+epsilon && rbt.body->GetPosition().x<=x_target+epsilon && rbt.body->GetPosition().x>=x_target-epsilon) reached=true;
        }
        if (collision) risk_vec.push_back(risk);
        else risk_vec.push_back(0);
        time_vec.push_back(t);
    }

    double risk_sum=std::accumulate(std::begin(risk_vec), std::end(risk_vec), 0.0);
    double risk_avg=risk_sum/risk_vec.size();

    double accum=0.0;
    std::for_each (std::begin(risk_vec), std::end(risk_vec), [&](const double d) {
        accum += (d - risk_avg) * (d - risk_avg);
    });

    double risk_stdev = sqrt(accum/(risk_vec.size()-1));

    double time_sum=std::accumulate(std::begin(time_vec), std::end(time_vec), 0.0);
    double time_avg=time_sum/time_vec.size();
    accum=0.0;
    std::for_each (std::begin(time_vec), std::end(time_vec), [&](const double d) {
        accum += (d - time_avg) * (d - time_avg);
    });
    double time_stdev = sqrt(accum/(time_vec.size()-1));

    printf("Average travel time: %f  %f\n", time_avg, time_stdev);
    printf("Average risk: %f  %f\n", risk_avg, risk_stdev);

    return 0;
}