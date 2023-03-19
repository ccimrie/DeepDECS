The python scripts are used to visualise the outcome of the simulations.

- **waypoint.py** is used to visualise the robot journeying only between one set of waypoints. This only requires the robot's and collider's poses, which need to be stored in **rbt_pos.txt** and **collider_pos.txt** respectively. 
- **visualise.py** will visualise the robot completing a journey between two waypoints (refer to **../box2D/robot_XY**, where **XY** can be any combination of 0 or 1, for more detail). The script requires the following files 
	- **wayppints.txt**: the waypoints
	- **rbt_pos.txt**: the robot's pose
	- **collider_pos.txt**: the collider's pose
	- **setup.txt**: the start and goal locations
	- **path.txt**: the waypoints travelled
	- **collisions.txt**: timestamps of when, if any, collisions occurred.
	- **objects.txt**: description of obstacles/walls 
	