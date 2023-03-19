This program generates datapoints used for training the DNN. 

Once compiled the program will be called **robot_data_collection**. To run:

```
./robot_data_collection output_file
```

The program will require the user to indicate how many samples they would like. Initially they will be asked if they would like to either 

1. enter a value for the number of collision datapoints and a value for the number of non-collision datapoints to be recorded
2. enter one value for the total number of datapoints recorded, which will result in a random ratio of collision to non-collision datapoints

The simulations are conducted until the desired number of datapoints are satisifed.

The ```output_file``` is the name of the file to store the datapoints, which will be the setup of the collider and the label (*collision* or *noCollision*).