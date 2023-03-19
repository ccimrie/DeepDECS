# DeepDECS for synthesising safe controllers for travelling robots

Here are the files for investigating the case study of a robot performing a navigation task using a DNN along with runtime verification methods to predict collisions with a collider. 

- **confusion_matrices** is the directory containing the confusion matrices produced given the various verification methods utilised in the DeepDECS framework.
- **dnn_model** contains the model of the trained DNN.
- **prism_files** contains the prism models, properties (as a pctl file), and the formatted confusion matrices to be compatible with the augment tool. The prism models using 0+ verification methods were generated using the augment tool.
- **simulator** contains all the files and code for setting up the simulation to gather datapoints, conducting experiments, and to validate the controllers produced from the DeepDECS process.