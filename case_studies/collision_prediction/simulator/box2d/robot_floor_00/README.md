This program is used to run simulations where the robot has a DNN to predict if a collision will occur if there is a collider. The robot uses 0 verification methods. The collider's parameters are drawn from the databuckets (collisions/no collisions) using the distribution defined in the paper. The robot will have an initial position and a randomly generated goal position, and will travel between the two using the shortest path of waypoints calculated via Dijkstra's algorithm.

Once compiled the program will be called **robot_floor_00**. To run:

```
./robot_floor_00 way_point_path objects_path \\
collision_data_path no_collision_data_path \\
col_pred_path no_col_pred_path \\
visit \\
x0 x1 \\
output_path
```

The following parameters are:

``` way_point_path objects_path``` are the locations of the text files containing the positions of the waypoints and obstacles/walls in the environment.

```collision_data_path no_collision_data_path``` are the locations of the databuckets containing the setups required to most likely result in a collision/no collision respectively.

```col_pred_path no_col_pred_path``` are the locations of the text files containing the predictions and verification methods satisified of the datapoints in the databuckets used above.

```visit``` is the minium number of waypoints to travel before the simulation ends

```x0 x1``` are the controller parameters for deciding the robot's actions.

```output_path``` is the path of where the outcome of the simulation are stored. These are multiple text files containg the waypoint locations, the robot's and collider's poses, the start and goal positions, the waypoint path the robot took, and where, if any, collisions happened. These files are **waypoints.txt**, **rbt_pos.txt**, **collider_pos.txt**, **setup.txt**, **waypoints.txt**, **path.txt**, and **collisions.txt**.