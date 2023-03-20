This program generates the databuckets used for generating the expected distribution of collisions/no collisions in complete simulations. These datapoints are passed through the trained DNN to acquire the prediction as well as which verification methods it satisfies.

Once compiled the program will be called **robot_data_buckets**. To run:

```
./robot_data_buckets outfile_path datasize
```

The ```outfile_path``` determines where the two textfiles (**collisions.txt**, **no_collisions.txt**) are stored. These output files contains the setup which led to either a collision or no collision. ```data_size``` is the number of collision and no collision datapoints to be generated, in total there will be 2\*```data_size```.