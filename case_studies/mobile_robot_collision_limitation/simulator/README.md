This directory contains all the files and code to execute the simulations. 

- **box2D** contains the various simulation setups (including data gathering, experimentation, and validation). This requires [box2D](https://box2d.org/).
- **data_buckets** contains the data buckets that was used to validate the results in the paper (for more detail refer to **box2D/robot_data_buckets**). 
- **visualiser** contains python scripts visualise the outcome of simulations.
- **DNN_data** contains the training data used for the DNN. It also contains another dataset, representative test set, which was used for Stage 1 of DeepDECS to acquire the confusion matrices. 