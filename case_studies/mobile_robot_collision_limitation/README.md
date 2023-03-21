# DeepDECS for mobile robot collision limitation

Here are the files for investigating the case study of a robot performing a navigation task using a DNN along with runtime verification methods to predict collisions with a collider. 

- **confusion_matrices** is the directory containing the confusion matrices produced given the various verification methods utilised in the DeepDECS framework.
- **dnn_model** contains the model of the trained DNN.
- **DTMC_model_files** contains the DTMC models (we used the software [Prism](https://www.prismmodelchecker.org/) for probabilistic model checking), properties (as a pctl file), and the formatted confusion matrices to be compatible with the automated [augment tool](https://github.com/ccimrie/DeepDECS/tree/master/augment_tool) for Stage 2 of DeepDECS. The DTMC models using 0+ verification methods were generated using the augment tool.
- **simulator** contains all the files and code for setting up the simulation to gather datapoints, conducting experiments, and to validate the controllers produced from the DeepDECS process. 