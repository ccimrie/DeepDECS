# DeepDECS for driver attentiveness management

Here are the files for investigating the case study of an autonomous car monitoring the human driver. The car uses a DNN to predict the driver's response time, and will use alerts to increase the driver's attentiveness levels if predicted to be low. This was part of the [SafeSCAD](https://www.york.ac.uk/assuring-autonomy/demonstrators/autonomous-driving/) project. 

- **confusion_matrices** is the directory containing the confusion matrices produced given the various verification methods utilised in the DeepDECS framework.
- **dnn_model** contains the model of the trained DNN.
- **DTMC_model_files** contains the DTMC models (we used the software [Prism](https://www.prismmodelchecker.org/) for probabilistic model checking), properties (as a pctl file), and the formatted confusion matrices to be compatible with the automated [augment tool](https://github.com/ccimrie/DeepDECS/tree/master/augment_tool) for Stage 2 of DeepDECS. The DTMC models using 0+ verification methods were generated using the augment tool.
- **EvoChecker** contains the [EvoChecker](https://www-users.york.ac.uk/~sg778/EvoChecker/) tool used to generate the pareto optimal controllers.